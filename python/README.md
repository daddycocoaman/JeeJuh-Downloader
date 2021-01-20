<div align="center">
<img src="https://img.shields.io/pypi/v/jeejuh-dl"/>
<img src="https://img.shields.io/pypi/pyversions/jeejuh-dl"/>
<img src="https://img.shields.io/pypi/l/jeejuh-dl"/>
<a href="https://twitter.com/mcohmi"><img src="https://img.shields.io/twitter/follow/mcohmi.svg?style=plastic"/></a><br>

</div>

# jeejuh-dl

JeeJuh.com doesn't have a "download all" button which makes it a little annoying to have to click every stem for every beat, especially if you have multiple beats in one purchase. This CLI tool is written in Python and allows a user to point to their download page and grab all the files.

**THIS TOOL IS NOT ASSOCIATED WITH OR ENDORSED BY JEEJUH.COM.**

## Installation

The recommended method of installation is with [pipx](https://github.com/pipxproject/pipx).

```
pipx install jeejuh-dl
```

However, you can install the normal way from PyPi with `python3 -m pip install jeejuh-dl`.

## Usage

`jeejuh-dl <URL>`

```
Usage: jeejuh-dl [OPTIONS] URL

Arguments:
  URL  URL to jeejuh.com download page  [required]

Options:
  --output DIRECTORY              [default: .]
  -t, --threads INTEGER           Max number of concurrent downloads
                                  [default: 5]

  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```
