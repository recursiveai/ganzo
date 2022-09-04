# Ganzo

Project creator (from templates).

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
    "gcs_bucket_name": "<gcs_bucket_name>" // Google Cloud Storage bucket where the templates are stored.
}
```

Then check how to use ganzo in from commandline.

```
$ ganzo -h
```
## Templates

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
app
list
```

Each templates directory will be fully copied as part of loading the template for a new project.

### Variable resolution

Files with extension `.nzo` are candidates for variable resolution,
which will replace variables within the files with project specific values.

```
# Content of README.md.nzo

This projects name is ${PROJECT_NAME}.
```

Currently the only available variable for resolution is `PROJECT_NAME`.

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

- Add/Test Support for older/newer Python versions.
- Support for custom variables.
- Directory structure changes based on variables.
- Improve coverage of core and resolvers.
- Improve error handling and messages
