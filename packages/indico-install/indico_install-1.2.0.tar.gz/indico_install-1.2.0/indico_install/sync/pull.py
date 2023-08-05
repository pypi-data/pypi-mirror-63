import json
import re

import click
from click import confirm, secho

from indico_install.config import ConfigsHolder
from indico_install.utils import options_wrapper, get_non_matching_images, get_nginx_conf


@click.group("pull")
@click.pass_context
def pull(ctx):
    """Pull the latest information from the cluster into services yaml file"""
    pass


@pull.command("all")
@click.pass_context
@options_wrapper(check_services=True)
def pull_all(ctx, **kwargs):
    """Pull both backend images and frontend hashes to your services yaml"""
    ctx.invoke(pull_images, **kwargs)
    ctx.invoke(pull_frontend_hashes, **kwargs)


@pull.command("images")
@click.pass_context
@options_wrapper(check_services=True)
def pull_images(ctx, *, services_yaml, yes, **kwargs):
    """Pull images from cluster"""
    configs = ConfigsHolder(config=services_yaml)

    for app, _, _, saved_image, cluster_image in get_non_matching_images(
        configs, only_first=True
    ):
        secho(f"{app}:\nOn Cluster: {cluster_image}\nOn Disk: {saved_image}")
        if yes or confirm("Save these changes to disk?"):
            secho(f"Saving changes for {app}", fg="green")
            configs["images"][app] = cluster_image
            configs.save()
        else:
            secho(f"Skipping changes for {app}", fg="yellow")


@pull.command("clients")
@click.pass_context
@options_wrapper(check_services=True)
def pull_frontend_hashes(ctx, *, services_yaml, yes, **kwargs):
    """Pull frontend hashes from cluster"""
    configs = ConfigsHolder(config=services_yaml)
    output = get_nginx_conf()
    output_string = json.loads(output)

    for app, _hash in configs["frontend"]["hash"].items():
        try:
            cluster_hash = re.search(fr"/{app}/(\w+);", output_string).group(1)
        except Exception:
            secho(f"Could not find {app} in cluster app-edge nginx.conf", fg="red")
        else:
            if cluster_hash != _hash.strip():
                secho(
                    f"{app} frontend hash\nOn Cluster: {cluster_hash}\nOn Disk: {_hash}"
                )
                if yes or confirm("Save these changes to disk?"):
                    secho(f"Saving changes for frontend {app}", fg="green")
                    configs["frontend"]["hash"][app] = cluster_hash
                    configs.save()
                else:
                    secho(f"Skipping changes for {app}", fg="yellow")

    secho("Done syncing changes", fg="green")


@pull.command("client")
@click.pass_context
@options_wrapper(check_services=True)
def pull_frontend_hash(ctx, *, services_yaml, yes, **kwargs):
    """Pull frontend hash from cluster"""
    configs = ConfigsHolder(config=services_yaml)
    output = get_nginx_conf()
    output_string = json.loads(output)
    app_hash = configs["frontend"]["hash"]

    try:
        cluster_hash = (
            re.search(rf"set \$clientversion [^;]*", output_string)
            .group(0)
            .split(" ")[-1]
        )
    except Exception:
        secho(f"Could not find client version in cluster app-edge nginx.conf", fg="red")
    else:
        if cluster_hash != app_hash.strip():
            secho(f"Frontend hash\nOn Cluster: {cluster_hash}\nOn Disk: {app_hash}")
            if yes or confirm("Save these changes to disk?"):
                secho(f"Saving changes for frontend", fg="green")
                configs["frontend"]["hash"] = cluster_hash
                configs.save()
            else:
                secho(f"Skipping frontend changes", fg="yellow")

    secho("Done syncing changes", fg="green")
