#!/usr/bin/env python
import click

import click


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """kubernaut: easy kubernetes clusters for painless development and testing"""


@cli.command("claim", help="claim your Kubernetes cluster")
def cli_claim():
    pass


@cli.command("release", help="release your Kubernetes cluster")
def cli_release():
    pass


@cli.command("login", help="login to access the kubernaut.io service")
def cli_login():
    pass


@cli.command("register", help="register with the kubernaut.io service")
def cli_register():
    pass
