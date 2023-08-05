Pączek filler
============

This tool tries to fill in a space next to `cookiecutter`, giving the user ability to
reuse functionality stored in a single file across different projects.

Setup a folder with files you reuse in your project.
Set the `PACZEK_FILLINGS` environment variable to point that folder.
Run `paczek` - will display list of files from which you can choose a file
that will be put in your current directory. 
If the file ends with `.tpl` you will be asked for values that will be put inside
the template.
 
Please remember, redundancy can be removed and files can me merged
using git. 

Requirements
------------

- [fzf](https://github.com/junegunn/fzf Fuzzy Search for command line

Usage
-----

There are two commands:
- `paczek`
- `paczekfiller <template_filepath> <target_filepath>`

### paczek

`paczek` is a script that uses `fzf` to fill out a template, from your template's folder and save it in your current folder.

If a template file ends with `.tpl`, then it is passed to `paczekfiller`, with the output filename without the `.tpl` extension.

If template file is without `.tpl`, then it's copied to your current folder, using `cp`


### paczekfiller

`paczekfiller` fills out a jinja2 template file and saves it under given target filepath.

`<template_filepath>` is an absolute path.

### config

Environment variables used by command `paczek`:

* `PACZEK_FILLINGS`    stores path to folder with template files 
* `PACZEK_GIT_SAFE`  set to `1` or whatever, when in folder with enabled git, paczek will checkout current branch and then place file 

### templates

Variables are extracted from templates. Variables names are
used in user prompt. The "_" are changed into spaces (" ").

So, for a variable `{{Some_variable}}`, script will prompt user with
this: `Some variable: `

Installation
------------

`pip install paczekfiller`

Licence
-------
MIT type.


Authors
-------

`paczekfiller` was written by `Kris Urbanski <kris@whereibend.space>`_.
