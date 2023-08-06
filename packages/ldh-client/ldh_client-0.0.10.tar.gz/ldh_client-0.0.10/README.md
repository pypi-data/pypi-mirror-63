# Liberty CLI

[project] | [code] | [tracker] | [pypi]

*Liberty CLI* is a user-facing command-line client for interacting
with Librem One or another Liberty Deckplan Host (LDH).

Dive into <https://liberty.one> for LDH design and development.

## Installation

The preferred way to install Liberty CLI is with your package
manager. The recommended package name is `ldh-client`. For example:

```bash
sudo apt install ldh-client  # Debian-based
```

or

```bash
pipx install ldh-client  # Python-based
```

## Usage

The following commands are available:

```
# INFO
liberty show info

# TUNNEL
liberty setup tunnel
```

For instructions and options add `--help`, for example:

```bash
liberty setup tunnel --help
```

## Prototype quickstart

To install prototype components on PureOS or another Debian-based
system from scratch:

```bash
sudo apt install pipx
pipx ensurepath
pipx install ldh-client
liberty setup dependencies  # triggers sudo prompt
liberty setup prototype
```

To update the prototype:

```bash
pipx upgrade ldh-client  # or pipx upgrade-all
liberty setup dependencies  # triggers sudo prompt
liberty setup prototype
```

To remove the prototype:

```bash
liberty remove dependencies  # optional, triggers sudo prompt
liberty remove prototype
pipx uninstall ldh-client
sudo apt remove pipx  # optional
```

## Installation (from source)

If you'd prefer to run from source...

1. Install Python 3.x and pipenv. (See
   <https://docs.pipenv.org/install/> for a tutorial.)

2. Install prerequisites:

        sudo apt install libcairo2-dev libgirepository1.0-dev libssl-dev python3-dev

3. Install optional prerequisites:

        sudo apt install rclone yad

4. Get source:

        git clone https://source.puri.sm/liberty/tool/client.git ldh_client

5. Install with pipenv:

        cd ldh_client
        pipenv install --dev -e .

## Usage (from source)

```bash
cd ldh_client
pipenv run liberty show info
```

## Prototype quickstart (from source)

Ensure that `~/.local/bin` is on your `$PATH`:

```bash
sudo apt install pipx
pipx ensurepath
# pipx is used only to set the path
# you may prefer to modify your .bashrc or some other method
```

Follow the from-source instructions, then create the `liberty-dev`
executable as follows:

```bash
cd ldh_client/liberty-dev
./bootstrap
# creates ~/.local/bin/liberty-dev and associated symlinks
# re-run this any time you move the ldh_client folder
```

Now install prototype components:

```bash
liberty-dev setup dependencies
liberty-dev setup prototype --dev
```

Note that `setup prototype` always overrides existing prototype
components. This means you can point to either `liberty` or
`liberty-dev`, never both.

To remove the prototype components and `liberty-dev`:

```bash
liberty-dev remove dependencies  # optional, triggers sudo prompt
liberty-dev remove prototype
cd ldh_client/liberty-dev
./remove
```

## Troubleshooting

When debugging, troubleshooting or asking for help please include the
output of:

```bash
liberty show info
```

or

```bash
liberty show info --gui
# the same information in a graphical window (supports copy-and-paste)
```

Replace `liberty` with `pipenv run liberty` or `liberty-dev` as
appropriate.

## Build wheel package (and optionally upload)

Follow these instructions to build Liberty CLI as a Python package:

```bash
git clone https://source.puri.sm/liberty/tool/client.git ldh_client
cd ldh_client
pipenv install --dev
pipenv shell
# optionally edit default.strict.yaml
python setup.py sdist bdist_wheel
```

If everything works as expected you should end up with the files:

* `dist/ldh_client-<version>-py3-none-any.whl`
* `dist/ldh_client-<version>.tar.gz`

You can now optionally upload the created Python package to PyPI using
twine:

```bash
twine upload dist/*
```

## Sharing and contributions

Liberty CLI (LDH client)  
<https://source.puri.sm/liberty/tool/client>  
Copyright 2018-2020 Purism SPC  
SPDX-License-Identifier: AGPL-3.0-or-later  

Shared under AGPL-3.0-or-later. We adhere to the Community Covenant
1.0 without modification, and certify origin per DCO 1.1 with a
signed-off-by line. Contributions under the same terms are welcome.

For details see:

* [COPYING.AGPL.md], full license text
* [CODE_OF_CONDUCT.md], full conduct text
* [CONTRIBUTING.DCO.md], full origin text (`git -s`)

<!-- Links -->

[project]: https://source.puri.sm/liberty/tool/client
[code]: https://source.puri.sm/liberty/tool/client/tree/master
[tracker]: https://source.puri.sm/liberty/tool/client/issues
[pypi]: https://pypi.org/project/ldh-client/
[SETUP.md]: SETUP.md
[COPYING.AGPL.md]: COPYING.AGPL.md
[CODE_OF_CONDUCT.md]: CODE_OF_CONDUCT.md
[CONTRIBUTING.DCO.md]: CONTRIBUTING.DCO.md
[COPYING.md]: COPYING.md
[CONTRIBUTING.md]: CONTRIBUTING.md
