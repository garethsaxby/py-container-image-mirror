#!/usr/bin/env python
"""Container Image Mirror"""
import click
import docker
import structlog

# Establish logger
log = structlog.get_logger()


def docker_client():
    """Instantiate the Docker client object"""
    client = docker.from_env()
    log.info(event="client_init", message="Initialised Docker Client", client=client)
    return client


def pull_image(client, repository, tag):
    """Pulls container image if not present, return instance of image object"""
    image = client.images.pull(repository=repository, tag=tag)
    log.info(
        event="pull",
        message=f"Pulled Container Image {repository}:{tag}",
        image=image,
        client=client,
        repository=repository,
        tag=tag,
    )
    return image


def push_image(client, image, push_repository, push_tag, auth_config):
    """Push container image to registry"""
    image.tag(repository=push_repository, tag=push_tag)
    for line in client.images.push(
        repository=push_repository,
        tag=push_tag,
        stream=True,
        decode=True,
        auth_config=auth_config,
    ):
        try:
            log.info(
                event="push",
                message=line["status"],
                id=line["id"],
                repository=push_repository,
                tag=push_tag,
            )
        except KeyError:
            pass


@click.command()
@click.option(
    "-r",
    "--repository",
    "repository",
    required=True,
    prompt=True,
    help="Source container repository",
)
@click.option(
    "-t",
    "--tag",
    "tag",
    required=True,
    prompt=True,
    help="Source container tag",
)
@click.option(
    "-d",
    "--destination",
    "destination",
    required=True,
    prompt=True,
    help="Destination container repository",
)
@click.option(
    "-T",
    "--destination-tag",
    "destination_tag",
    required=True,
    prompt=True,
    help="Destination container repository tag",
)
@click.option(
    "-u",
    "--user",
    "push_user",
    required=True,
    prompt=True,
    help="Destination registry username",
)
@click.option(
    "-p",
    "--password",
    "push_password",
    required=True,
    prompt=True,
    help="Destination registry password",
    hide_input=True,
)
def main(
    repository, tag, destination, destination_tag, push_user, push_password
):  # pylint: disable=too-many-arguments
    # This function takes a few too many arguments and is a bit messy, so probably needs refactoring
    """Run the task"""
    log.info(
        event="start",
        message=f"Syncing {repository}:{tag} to {destination}:{destination_tag}",
        repository=repository,
        push_user=push_user,
        tag=tag,
        destination=destination,
        destination_tag=destination_tag,
    )

    client = docker_client()

    image = pull_image(client=client, repository=repository, tag=tag)

    push_image(
        client=client,
        image=image,
        push_repository=destination,
        push_tag=destination_tag,
        auth_config={"username": push_user, "password": push_password},
    )

    log.info(
        event="finish",
        message=f"Synced {repository}:{tag} to {destination}:{destination_tag}",
        repository=repository,
        push_user=push_user,
        tag=tag,
        destination=destination,
        destination_tag=destination_tag,
    )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
