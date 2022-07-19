# Ganzo

Project generator from templates.

## How to use?

Ganzo assumes the existence of a folder `~/.ganzo` containing the configuration.

```
/~
    /.ganzo
        configuration.json
```

Example `configuration.json`:

```
{
    "requirements":
}
```

Then check how to use ganzo in from commandline.

```
$ ganzo -h
```

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
