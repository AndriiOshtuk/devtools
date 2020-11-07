"""
Devtools a set of tools to automate common development tasks
"""

import logging
import sys
import textwrap
from pathlib import Path, PurePath

import click

# import click_log

logger = logging.getLogger()
# click_log.basic_config(logger)


@click.group()
def cli() -> None:
    """Devtools a set of tools to automate common development tasks."""
    pass


@cli.command()
# @click.option('proj_name', '-p', default=False, type=click.STRING)
@click.argument("proj_name", default=False, type=click.STRING)
def createproj(proj_name: str) -> None:
    """Create a SublimeText project files"""
    current_dir = Path.cwd()

    if not proj_name:
        proj_name = PurePath(current_dir).parts[-1]

    proj_file_path = current_dir / f"{proj_name}.sublime-project"
    proj_file = Path(proj_file_path)
    if proj_file.exists():
        logger.error(f"Path already exists {proj_file_path}")
        click.echo(f"Path already exists {proj_file_path}")
        sys.exit()

    SUBLIME_PROJECT_TEMPLATE = """\
    {
        "folders":
        [
            {
                "path": "."
            }
        ]
    }"""
    text = textwrap.dedent(SUBLIME_PROJECT_TEMPLATE)
    proj_file.write_text(text)

    logger.info(f"Created project:{proj_name} at {current_dir}")
    click.echo(f"Created project:{proj_name} at {current_dir}")


if __name__ == "__main__":
    cli()
