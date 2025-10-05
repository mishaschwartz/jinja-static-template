import configparser
import os
import shutil
import argparse

from jinja2 import FileSystemLoader, Environment, select_autoescape


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(THIS_DIR, "templates")
SITE_PATH = os.path.join(TEMPLATE_PATH, "site")


def filter_site_templates(template, extensions=("js", "html", "css")):
    abs_filepath = os.path.join(TEMPLATE_PATH, template)
    basename = os.path.basename(template)
    return (
        SITE_PATH == os.path.commonpath((abs_filepath, SITE_PATH))
        and "." in basename
        and basename.rsplit(".", 1)[1] in extensions
    )


def build(build_directory, config_files, clean=False):
    if clean:
        shutil.rmtree(build_directory, ignore_errors=True)
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_PATH),
        autoescape=select_autoescape(enabled_extensions=("html", "js", "css")),
    )

    shutil.copytree(
        os.path.join(THIS_DIR, "static"), build_directory, dirs_exist_ok=True
    )

    configs = configparser.ConfigParser()
    ok_files = configs.read(config_files)
    if ok_files != config_files:
        raise FileNotFoundError(
            f"These config files could not be found: {set(config_files) - set(ok_files)}"
        )

    for template in env.list_templates(filter_func=filter_site_templates):
        build_destination = os.path.join(
            build_directory,
            os.path.relpath(os.path.join(TEMPLATE_PATH, template), SITE_PATH),
        )
        os.makedirs(os.path.dirname(build_destination), exist_ok=True)

        with open(build_destination, "w") as f:
            f.write(env.get_template(template).render(**configs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b",
        "--build-directory",
        default=os.path.join(THIS_DIR, "build"),
        help="location on disk to write built templates to.",
    )

    parser.add_argument(
        "-g",
        "--config-files",
        action="append",
        help="TOML config file",
    )

    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="clean build directories before building.",
    )
    args = parser.parse_args()
    build(args.build_directory, args.config_files, args.clean)
