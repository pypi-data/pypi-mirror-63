#!/usr/bin/env python3
# Copyright 2017-2020 Purism SPC
# SPDX-License-Identifier: AGPL-3.0-or-later

import click
from ldh_client.nm_tunnel_setup import nm_tunnel_setup
from ldh_client.nautilus_files_setup import nautilus_files_setup
from ldh_client import common


@click.group()
@click.pass_context
def cli(ctx):
    """Liberty CLI is a user-facing command-line client for interacting with
    Librem One or another Liberty Deckplan Host (LDH)."""
    pass


# TOP-LEVEL COMMANDS (VERBS)

# liberty show ...
@cli.group()
def show():
    """Display useful service information."""
    pass


# liberty remove ...
@cli.group()
def remove():
    """Remove configuration and desktop files (does not affect online data)."""
    pass


# liberty setup ...
@cli.group()
def setup():
    """Configure or reconfigure desktop components."""
    pass


# liberty delete ...
@cli.group()
def delete():
    """Permanently delete data from online services. This command is not yet implemented."""
    print("This command is not yet implemented.")


# liberty tunnel_setup ...
@cli.command(name="tunnel_setup")
def old_tunnel_setup():
    """This command is deprecated. Please use `liberty setup tunnel` instead."""
    print("This command is deprecated. Please use `liberty setup tunnel` instead.")


# FILES COMMANDS

# liberty setup files
@setup.command(name="files")
def files_setup():
    """Create mountpoint for files."""
    nautilus_files_setup()


# INFO COMMANDS

# liberty show info
@show.command(name="info")
@click.option(
    "--gui", is_flag=True, help="Use graphical interface rather than text prompts."
)
def show_info(gui):
    """Display debug info, useful in bug reports."""

    info_message = common.generate_info_message()

    if gui:
        common.yad_prompt("Debug information, useful in bug reports:", info_message)
    else:
        print("Debug information, useful in bug reports:")
        print(info_message)


# TUNNEL COMMANDS

# liberty setup tunnel
@setup.command(name="tunnel")
@click.option(
    "--gui", is_flag=True, help="Use graphical interface rather than text prompts."
)
@click.option("--goa", is_flag=True, help="Get credentials from GOA.")
def tunnel_setup(gui, goa):
    """Download tunnel config and add to NetworkManager."""

    if gui:
        try:
            credentials = common.get_single_goa_credential()
            nm_tunnel_setup(credentials)
            common.yad_prompt(
                "Tunnel is ready to activate.", message=None, title="Tunnel"
            )
        except Exception as e:
            common.yad_prompt("There was a problem.", str(e), "Tunnel")
    else:
        try:
            if goa:
                credentials = common.get_single_goa_credential()
            else:
                credentials = common.text_credential_prompt()
            nm_tunnel_setup(credentials)
            print("Tunnel is ready to activate.")
        except Exception as e:
            print("There was a problem.\n" + str(e))


# PROTOTYPE AND DEPENDENCY COMMANDS

# liberty setup dependencies
@setup.command(name="dependencies")
@click.confirmation_option(
    prompt="Are you sure you want to add prototype dependencies?"
)
def dependencies_setup():
    """Create prototype."""

    common.control_prototype_dependencies(True)


# liberty remove dependencies
@remove.command(name="dependencies")
@click.confirmation_option(
    prompt="Are you sure you want to remove prototype dependencies?"
)
def dependencies_remove():
    """Create prototype."""

    common.control_prototype_dependencies(False)


# liberty setup prototype
@setup.command(name="prototype")
@click.confirmation_option(
    prompt="Are you sure you want to add untested prototype components?"
)
@click.option(
    "--dev",
    is_flag=True,
    help="Point prototype components to the liberty-dev executable.",
)
def prototype_setup(dev):
    """Create prototype components in local folders."""

    common.create_prototype_files(dev)


# liberty remove prototype
@remove.command(name="prototype")
@click.confirmation_option(
    prompt="Are you sure you want to remove all prototype components?"
)
def prototype_remove():
    """Remove all prototype components."""

    common.remove_prototype_files()
