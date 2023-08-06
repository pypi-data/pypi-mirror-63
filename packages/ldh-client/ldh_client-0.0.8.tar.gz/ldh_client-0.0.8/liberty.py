#!/usr/bin/env python3
# Copyright 2017-2020 Purism SPC
# SPDX-License-Identifier: AGPL-3.0-or-later

import click
from ldh_client.nm_tunnel_setup import nm_tunnel_setup
from ldh_client.nautilus_files_setup import nautilus_files_setup


@click.group()
@click.pass_context
def cli(ctx):
    """Liberty CLI is a user-facing command-line client for interacting with
    Librem One or another Liberty Deckplan Host (LDH)."""
    pass


@cli.command()
def debug():
    """Display debug info, useful in bug reports."""

    import pkg_resources
    import sys
    import platform
    import distro
    import os
    import ldh_client.common

    package_version = pkg_resources.require("ldh_client")[0]
    python_version = "Python " + sys.version.replace("\n", " ").replace("  ", " ")
    platform_version = "Platform " + platform.platform()
    distro_version = "Distribution " + distro.name(pretty=True)
    rclone_version = "rclone " + ldh_client.common.get_rclone_version().replace("\n", " ").replace("  ", " ").replace("rclone ", "")
    yad_version = "YAD " + ldh_client.common.get_yad_version().replace("\n", " ").replace("  ", " ")
    path = "$PATH " + os.environ["PATH"].replace(os.environ["HOME"], "~")
    goa_accounts = "GOA accounts " + str(ldh_client.common.count_goa_credentials())

    print(package_version)
    print(python_version)
    print(platform_version)
    print(distro_version)
    print(rclone_version)
    print(yad_version)
    print(path)
    print(goa_accounts)


@cli.command(name="tunnel_setup")
def old_tunnel_setup():
    """This command is deprecated. Please use `liberty setup tunnel` instead."""
    print("This command is deprecated. Please use `liberty setup tunnel` instead.")


@cli.group()
def setup():
    """Configure or reconfigure services on an XDG desktop."""
    pass


@setup.command(name="tunnel")
def tunnel_setup():
    """Download tunnel config and add to NetworkManager."""
    nm_tunnel_setup()


@setup.command(name="files")
def files_setup():
    """Create mountpoint for files."""
    nautilus_files_setup()


# @set.command(name="default")
# def default_get():
#     ...
#
#
# @set.command(name="default")
# def default_set():
#     ...
#
#
# @set.command(name="passphrase")
# def passphrase_set():
#     ...
#
#
# @get.command(name="passphrase")
# def passphrase_get():
#     ...
