# Ganzo

Creates new project from templates stored in git repositories.

## How to use?

Ganzo assumes the existence of a folder `$HOME/.ganzo` containing the configuration.

```
/$HOME
    /.ganzo
        configuration.json
```

Example `configuration.json`:

```
{
    "gcs_bucket_name": "<gcs_bucket_name>" // Google Cloud Storage bucket where the template list is stored.
}
```

Then check how to use ganzo in from commandline.

```
$ ganzo -h
```

## Templates

Templates are store in a directory containing a `templates.list` file which contains a template entry per line.

The `templates.list` file for the previous directory should list all the templates available.

```
# Content of templates.list
<template_name> <template_git_url> <template_git_branch>
app git@github.com:organozation/project_app.git main
list https://github.com/organozation/project_list.git dev
```

### Variable resolution

Files with extension `.nzo` are candidates for variable resolution,
which will replace variables within the files with project specific values.

```
# Content of README.md.nzo

This projects name is ${PROJECT_NAME}.
```

Currently the only available variable for resolution is `PROJECT_NAME`.


## Legacy Templates (version <= 0.5.0)

Templates are store in a directory containing a `templates.list` file,
which contains a template name per line.

```
/path/to/templates
    templates.list
    /app
        /code
        pyproject.toml
        ...
    /lib
        /scripts
        README.md.nzo
        ...
```

The `templates.list` file for the previous directory should list all the templates available.

```
# Content of templates.list
<template_name>
app
list
```

Each templates directory will be fully copied as part of loading the template for a new project.

## Development

### Python virtual environment

Create and load a virtual environement.

```
python -m venv .venv
source .venv/bin/activate
```

### Install

Install all dependencies in editable mode.

```
make install
```

### Misc

Check what other shortcuts are available.

```
make help
```

## Areas of improvement

- Support for custom variables.
- Directory structure changes based on variables.
- Improve coverage of core and resolvers.
- Improve error handling and messages
