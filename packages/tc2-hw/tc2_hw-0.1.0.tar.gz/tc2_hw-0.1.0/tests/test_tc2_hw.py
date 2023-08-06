#!/usr/bin/env python

"""Tests for `tc2_hw` package."""


import unittest
from click.testing import CliRunner

from tc2_hw import tc2_hw
from tc2_hw import cli


class TestTc2_hw(unittest.TestCase):
    """Tests for `tc2_hw` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'tc2_hw.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
