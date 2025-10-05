# Jinja Static Template

This template is a starting point for building a static website using 
[jinja](https://jinja.palletsprojects.com/en/stable/). 

Start from here and add/remove/adjust files as needed.

## Requirements

- Python 3.9 or later

## Build the static site

To convert the files in the `templates/` directory into a built website:

1. Install the requirements:

```sh
python3 -m pip install -r requirements.txt
```

2. Build the HTML files

```sh
python3 build.py
```

To see all build options: 

```sh
python3 build.py --help
```

## Configuration

Configuration settings can be specified when building the site by specifying the path to one or more configuration files
(as defined by the [configparser](https://docs.python.org/3.13/library/configparser.html) library) using the 
`--config-files` flag when calling `build.py`.

If multiple configuration files are specified, values in later files will overwrite those in earlier files.

Values specified in these configuration files will be passed directly to jinja2's 
[`render`](https://jinja.palletsprojects.com/en/stable/api/#jinja2.Template.render) method when generating template
files.

## Development

This is how the files are arranged in this repo and how to update them in order to develop this website.

- Files in the `static/` directory will be copied to the build directory without modification.
- Files in the `templates/site/` directory will be copied to the build directory after being updated by the template engine (jinja)
- All other directories in the `templates/` directory will not be copied to the build directory but will be used by the templating engine
- Files in the `templates/layouts/` directory contains files that should be extended by other template files
- Files in the `templates/partials/` directory contain files that should be included by other template files
