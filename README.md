![Jam Logo](logo.png)

## Overview
Tool to ease development with [rez](https://github.com/AcademySoftwareFoundation/rez).

## Install Guide

Jam requires two environment variables to be set to work:

Variable Name     | Description
----------------- |:--------------:
`JAM_CONFIG_PATH` | Directory to store Jam configs.
`JAM_BUILD_PATH`  | Directory to store installed temp packages.


```bash
python setup.py --install
```

## User Guide

Creating new config.
```bash
jam new <config name>
```

Editing existing config.
```bash
jam edit <config name>
```

Adding packages to config.
```bash
# Adding remote package.
jam edit <config name>
jam add "package-2.0.0"

# Adding local package.
jam add /path/to/package.py

# You don't need to enter edit mode to add a package.
jam add "python-2.7+<4" --config <config name>
```

Running config
```bash
jam edit <config name>
jam run 

jam run -c <alias or executable>

# Example
jam run --config maya2020 -c maya

```