import pathlib
import os

import pytest
from click.testing import CliRunner
from unittest.mock import patch

import src.devtools.devtools as app


def test_init():
    with patch.object(app, "cli", return_value=None) as cli:
        with patch.object(app, "__name__", "__main__"):
            __import__("src.devtools.devtools")
            assert cli.called_once

def test_help():
    """
    Test that CLI when called with help options
    """
    runner = CliRunner()
    result = runner.invoke(app.cli, ["--help"])
    assert result.exit_code == 0

def test_createproj():
    """
    Test that createproj calls the createproj command
    """
    with patch("src.devtools.devtools.createproj") as createproj:
        runner = CliRunner()
        result = runner.invoke(app.cli, ["createproj"])
        assert result.exit_code == 0
        assert createproj.called_once


@pytest.fixture()
def temp_projdir(tmp_path) -> pathlib.Path:
    """Make a project directory, and return a Path() to it."""
    dummy_projname = tmp_path / "dummy_projname"
    dummy_projname.mkdir()
    return dummy_projname

def test_createproj_with_default_projname(temp_projdir):
    """
    Test that createproj creates project file with module name
    """
    os.chdir(temp_projdir)
    with patch("src.devtools.devtools.createproj") as createproj:
        runner = CliRunner()
        result = runner.invoke(app.cli, ["createproj"])
        assert result.exit_code == 0
        assert createproj.called_once

        files = list(temp_projdir.iterdir())
        assert len(files) == 1
        assert files[0].name == 'dummy_projname.sublime-project'

        expected_output = f"Created project:dummy_projname at {temp_projdir}"
        assert expected_output in result.output


def test_createproj_with_custom_projname(temp_projdir):
    """
    Test that createproj creates project file with custom name
    """
    os.chdir(temp_projdir)
    with patch("src.devtools.devtools.createproj") as createproj:
        runner = CliRunner()
        result = runner.invoke(app.cli, ["createproj", "custom_name"])
        assert result.exit_code == 0
        assert createproj.called_once

        files = list(temp_projdir.iterdir())
        assert len(files) == 1
        assert files[0].name == 'custom_name.sublime-project'

        expected_output = f"Created project:custom_name at {temp_projdir}"
        assert expected_output in result.output

def test_createproj_that_already_exists(temp_projdir):
    """
    Test that createproj exits with an error if project file with name already exists
    """
    os.chdir(temp_projdir)
    existing_projfile = temp_projdir / 'dummy_projname.sublime-project'
    existing_projfile.touch()

    with patch("src.devtools.devtools.createproj") as createproj:
        runner = CliRunner()
        result = runner.invoke(app.cli, ["createproj"])
        assert result.exit_code == 0
        assert createproj.called_once

        files = list(temp_projdir.iterdir())
        assert len(files) == 1
        assert files[0].name == 'dummy_projname.sublime-project'

        expected_output = f"Path already exists {existing_projfile}\n"
        assert expected_output == result.output
