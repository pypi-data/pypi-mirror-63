#!/usr/bin/env python

"""Tests for `sgipupdate` package."""

from click.testing import CliRunner

from sgipupdate import cli


class TestSgipupdate():
    """Tests for `sgipupdate` package."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Usage: ' in help_result.output
