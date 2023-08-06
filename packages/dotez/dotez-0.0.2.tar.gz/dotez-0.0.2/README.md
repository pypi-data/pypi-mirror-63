Dotfiles made easy with Python and Git

# Prerequisite
- Git
- Python3 (not and not going to be tested on python2)
- For more go check [requirements.txt](requirements.txt)

# Installation

```bash
pip install dotez
```

# Quick Start

Go to anywhere in your system, run:

```bash
dotez
```

and `dotez` will create a directory called `dotez` (we will call this the data dir)
under your home directory, and a git repository is created under the data dir. Also, the files specified in
the [configuration file](#configuration) will be added and committed through `git`.

By default, `dotez` doesn't print anything, so to see the results you can go to the data dir and run:

```bash
git log
```

and it will show something like this:

    commit  ... (HEAD -> master)
    Author: ...
    Date:   ...
    
        Update 9 files
    
        File list: ['~/.config/nvim', '~/.config/scripts', '~/.bashrc', '~/.Xresources', '~/.ideavimrc', '~/.profile', '~/.xprofile', '~/.xinitrc', '~/.xsessionrc']


# Configuration

## Overview

The configuration of `dotez` is written in `json`. And `dotez` loads the first configuration file that
exists in the following path and order.

- `~/.config/dotez.conf`
- `~/.dotez.conf`

By default the configuration is:

```json
{
  "includes": [
    ".config/nvim",
    ".Xresources",
    ".profile",
    ".xprofile",
    ".*rc",
    "*rc"
  ],
  "ignores": [
    "*.tmp",
    "*.swap",
    "*.o"
  ],
  "remotes": [
    {
      "name": "github",
      "url": "https://github.com/example/example",
      "push": true
    },
    {
      "name": "gitlab-read",
      "url": "https://gitlab.com/example/example",
      "push": false
    }
  ]
}
```

## `includes` and `ignores`

The most important parts of the file are `includes` and `ignores`. `includes` specifies which files to be added
into the git repository, and `ignores` specifies which files to exclude/ignore.

Both of them supporting filename globbing. More info on globbing [here](http://www.tldp.org/LDP/abs/html/globbingref.html).

In addition to globbing, you can use environment variables, such as `$HOME`, `$CONDA_PREFIX` etc.

NOTE there are several things to notice:

- the rules in `ignores` ALWAYS OVERRIDE `includes` if a files/dir matches both of them.
- no errors or warnings are reported if nothing matches either of the rules.

One useful way to test your configuration is:

```bash
dotez --test
```

And the output is like:

    Files to be added:  ['~/dotez/.config/nvim', '~/dotez/.config/scripts', '~/dotez/.bashrc', '~/dotez/.Xresources',
    '~/dotez/.ideavimrc', '~/dotez/.profile', '~/dotez/.xprofile', '~/dotez/.xinitrc', '~/dotez/.xsessionrc',
    '~/dotez/.dotez.conf', '~/dotez/.tmux.conf', '~/dotez/.dotez.conf', '~/dotez/.xinputrc', '~/dotez/.monitrc',
    '~/dotez/.netrc', '~/dotez/.gemrc', '~/dotez/.condarc', '~/dotez/.nvidia-settings-rc', '~/dotez/.xsessionrc',
    '~/dotez/.xinitrc', '~/dotez/.npmrc', '~/dotez/.ideavimrc', '~/dotez/.dmrc', '~/dotez/.bashrc', '~/dotez/.yarnrc',
    '~/dotez/.jackdrc', '~/dotez/.xbindkeysrc']
    
## `remotes`

