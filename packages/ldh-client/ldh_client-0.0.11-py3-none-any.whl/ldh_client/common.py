#!/usr/bin/env python3
# Copyright 2017-2020 Purism SPC
# SPDX-License-Identifier: AGPL-3.0-or-later

import ldh_client
import re

from getpass import getpass

# define strings that use defaults
DATA_FOLDER = ldh_client.DATA_FOLDER
GUI_TITLE = str(ldh_client.DEFAULT["HOST_LABEL"])
ADDRESS_PROMPT = "Enter your " + str(ldh_client.DEFAULT["HOST_LABEL"]) + " address: "
PASSPHRASE_PROMPT = "Enter your passphrase: "


class LdhCredential(object):
    """User credentials for an LDH account."""

    def __init__(self, user, host, passphrase):
        self.user = user
        self.host = host
        self.passphrase = passphrase

    def __str__(self):
        return self.address + " : '" + self.passphrase + "'"

    @property
    def address(self):
        return self.user + "@" + self.host


class LdhError(Exception):
    """Base class for LDH-related errors."""

    def __init__(self, message):
        self.message = message


def text_credential_prompt():
    """Prompts the user until they enter valid credentials. Returns a valid LdhCredential."""

    valid_address = False

    while not valid_address:
        address = input(ADDRESS_PROMPT)
        regex = r"^[A-Za-z][A-Za-z0-9]*@[A-Za-z0-9]+(\.[A-Za-z0-9]+)+$"
        if not re.match(regex, address):
            print(address + " is not a valid email address.")
        else:
            valid_address = True

    (user, host) = address.split("@")
    passphrase = getpass(PASSPHRASE_PROMPT)

    return LdhCredential(user, host, passphrase)


def get_accounts_from_goa():

    try:
        import gi

        gi.require_version("Goa", "1.0")
    except ValueError:
        raise ImportError("GOA library not available")

    from gi.repository import Goa

    client = Goa.Client.new_sync()
    return client.get_accounts()


def count_goa_credentials():

    count = 0

    try:
        accounts = get_accounts_from_goa()
        for objprx in accounts:
            accprx = objprx.get_account()
            if accprx.props.provider_type == "librem_one":
                count += 1
    except Exception:
        count = -1

    return count


def get_single_goa_credential():
    """Query GOA for valid credentials."""

    user = None
    host = None
    passphrase = None

    accounts = get_accounts_from_goa()
    count = 0
    for objprx in accounts:
        accprx = objprx.get_account()
        if accprx.props.provider_type == "librem_one":
            count += 1

            # FIXME: GOA should store a full address not just a name
            # see below for suggested logic
            user = accprx.props.identity
            host = ldh_client.DEFAULT["HOST_DOMAIN"]

            # address = accprx.props.identity  # probably need perform minimal validation here
            # (user, host) = address.split("@")

            pbobj = objprx.get_password_based()
            passphrase = pbobj.call_get_password_sync("password")

    if count == 0:
        raise ValueError(
            "No GOA credentials found. Please open 'Online accounts' and add your "
            + GUI_TITLE
            + " address and passphrase."
        )
    elif count > 1:
        raise ValueError(
            "Too many GOA credentials found. Please open 'Online accounts' and disable unused accounts. Alternatively, try again from the command line."
        )

    return LdhCredential(user, host, passphrase)


def get_rclone_version():
    """Extract version number from rclone, if it is available."""

    try:

        import sh
        from sh import rclone
        from io import StringIO

        buffer = StringIO()

        try:
            rclone("--version", _out=buffer)
        except sh.ErrorReturnCode_252:
            pass  # ignore exit code

        return buffer.getvalue()
    except Exception:
        return "None"


def get_yad_version():
    """Extract version number from yad, if it is available."""

    try:

        import sh
        from sh import yad
        from io import StringIO

        buffer = StringIO()

        try:
            yad("--version", _out=buffer)
        except sh.ErrorReturnCode_252:
            pass  # ignore exit code

        return buffer.getvalue()
    except Exception:
        return "None"


def yad_prompt(text, message=None, title=GUI_TITLE):
    """Display a message with YAD."""

    import sh
    from sh import yad

    title_option = "--title=" + title
    text_option = "--text=" + text

    try:
        if message is None:
            yad(
                title_option,
                text_option,
                "--no-buttons",
                "--maximized",
                "--wrap",
                "--window-icon=info",
            )
        else:
            # Print the message to echo. Pipe the output to YAD. Piped text appears in text-info box.
            yad(
                sh.echo(str(message)),
                title_option,
                text_option,
                "--no-buttons",
                "--maximized",
                "--wrap",
                "--window-icon=info",
                "--text-info",
            )
    except sh.ErrorReturnCode_252:
        pass  # ignore exit code


def remove_prototype_files():
    """Delete all prototype files."""

    import os

    empty = True

    friendly_list = generate_prototype_list(friendly=True)

    for path in generate_prototype_list():
        empty = False
        os.remove(path)

    if empty:
        print(friendly_list)
    else:
        print("Removed " + friendly_list)


def control_prototype_dependencies(install):
    """Add or remove dependencies with apt."""

    import sh

    dependencies = [
        "gir1.2-goa-1.0",
        "libcairo2-dev",
        "libgirepository1.0-dev",
        "libssl-dev",
        "network-manager-openvpn-gnome",
        "python3-dev",
        "yad",
        "rclone",
    ]

    dependency_string = ", ".join(dependencies)

    if install:
        print("Installing " + dependency_string)
        sh.contrib.sudo.apt.install(dependencies)
    else:
        print("Uninstalling " + dependency_string)
        sh.contrib.sudo.apt.remove(dependencies)


def create_prototype_files(development_flag=False):
    """Create all prototype files."""

    import glob
    import os
    import shutil

    # remove any existing prototype files
    remove_prototype_files()

    # (re)create prototype files
    pattern = DATA_FOLDER + "/*.desktop"
    destination = os.path.expanduser("~/.local/share/applications/")
    for path in glob.glob(pattern):
        shutil.copy(path, destination)

    if development_flag:
        for path in generate_prototype_list():
            if path.endswith(".desktop"):
                with open(path, "r+") as f:

                    # correct the contents
                    contents = f.read()
                    contents = contents.replace("Exec=liberty", "Exec=liberty-dev")

                    # to rewrite an open file: seek to the front, write contents, then truncate
                    f.seek(0)
                    f.write(contents)
                    f.truncate()

    friendly_list = generate_prototype_list(friendly=True)
    print("Created " + friendly_list)


def generate_prototype_list(friendly=False):
    """Generate a list of all prototype files."""

    import glob
    import os

    folder = os.path.expanduser("~/.local/share/applications/")
    pattern = folder + "one.liberty.*"
    result = glob.glob(pattern)

    if not friendly:
        # for non-friendly result, return raw list
        return result
    elif len(result) == 0:
        # for empty friendly result, return friendly string
        return "No prototype files found."
    else:
        # for non-zero friendly result, return comma-separated list
        return ", ".join(result).replace(os.environ["HOME"], "~")


def clean_multiline_string(multiline_string):
    """Make a multiline string suitable for single-line output."""

    return multiline_string.replace("\n", " ").replace("  ", " ")


def generate_info_message():
    """Generate a summary of debug data."""

    import pkg_resources
    import sys
    import platform
    import distro
    import os

    package_version = str(pkg_resources.require("ldh_client")[0])
    data_folder = "Data folder " + str(DATA_FOLDER).replace(os.environ["HOME"], "~")
    python_version = "Python " + clean_multiline_string(sys.version)
    platform_version = "Platform " + platform.platform()
    distro_version = "Distribution " + distro.name(pretty=True)
    rclone_version = "rclone " + clean_multiline_string(get_rclone_version()).replace(
        "rclone ", ""
    )
    yad_version = "YAD " + clean_multiline_string(get_yad_version())
    path = "$PATH " + os.environ["PATH"].replace(os.environ["HOME"], "~")
    goa_accounts = "GOA accounts " + str(count_goa_credentials())
    prototype_files = "Prototype files " + generate_prototype_list(friendly=True)

    info_list = [
        package_version,
        data_folder,
        python_version,
        platform_version,
        distro_version,
        rclone_version,
        yad_version,
        path,
        goa_accounts,
        prototype_files,
    ]

    return "\n".join(info_list)
