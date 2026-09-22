"""Regression tests for dynamically derived Uvicorn configuration."""

import os
from inspect import signature
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast, override
from unittest.mock import patch

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from pydantic import ValidationError
from uvicorn import run

from moodlehack.serve.management.commands.serve import Command
from moodlehack.serve.runner import runserver
from moodlehack.settings.base import AppSettings
from moodlehack.settings.uvicorn import UvicornServerSettings


class UvicornSettingsTests(SimpleTestCase):
    """Check configuration sources, validation and server integration."""

    @override
    def setUp(self) -> None:
        super().setUp()
        self.enterContext(patch.dict(os.environ, {}, clear=True))

    def load_settings(self, toml: str = "") -> UvicornServerSettings:
        """Load isolated TOML settings with the current environment."""
        directory = self.enterContext(TemporaryDirectory())
        config = Path(directory) / "settings.toml"
        _ = config.write_text(toml, encoding="utf-8")
        with patch.dict(AppSettings.model_config, {"toml_file": config}):
            return AppSettings().uvicorn

    def test_unspecified_options_use_upstream_defaults(self) -> None:
        config = self.load_settings()
        self.assertEqual(config.as_dict, {})
        parameters = signature(run).parameters
        self.assertEqual(
            config.model_dump()["host"],
            cast(object, parameters["host"].default),
        )
        self.assertEqual(
            config.model_dump()["port"],
            cast(object, parameters["port"].default),
        )

    def test_toml_and_environment_values_are_merged_and_typed(self) -> None:
        os.environ.update(
            {
                "MOODLEHACK_UVICORN__PORT": "9000",
                "MOODLEHACK_UVICORN__ACCESS_LOG": "false",
                "MOODLEHACK_UVICORN__RELOAD_DELAY": "0.5",
                "MOODLEHACK_UVICORN__RELOAD_DIRS": '["src", "templates"]',
            }
        )
        options = self.load_settings(
            """[uvicorn]
host = "0.0.0.0"
port = 8001
access_log = true
timeout_keep_alive = 12
"""
        ).as_dict
        self.assertEqual(
            options,
            {
                "host": "0.0.0.0",
                "port": 9000,
                "access_log": False,
                "timeout_keep_alive": 12,
                "reload_delay": 0.5,
                "reload_dirs": ["src", "templates"],
            },
        )
        self.assertIs(type(options["port"]), int)
        self.assertIs(options["access_log"], False)

    def test_new_upstream_option_is_available(self) -> None:
        os.environ["MOODLEHACK_UVICORN__HTTP2"] = "true"
        self.assertEqual(self.load_settings().as_dict, {"http2": True})

    def test_invalid_environment_value_is_rejected(self) -> None:
        os.environ["MOODLEHACK_UVICORN__PORT"] = "not-a-port"
        with self.assertRaises(ValidationError):
            _ = self.load_settings()

    def test_unknown_reserved_and_old_grouped_options_are_rejected(
        self,
    ) -> None:
        for option in (
            {"porrt": 9000},
            {"app": "another.application"},
            {"logging": {"access_log": False}},
        ):
            with (
                self.subTest(option=option),
                self.assertRaises(ValidationError),
            ):
                _ = UvicornServerSettings.model_validate(option)

    def test_unknown_environment_option_is_rejected(self) -> None:
        os.environ["MOODLEHACK_UVICORN__PORRT"] = "9000"
        with self.assertRaises(ValidationError):
            _ = self.load_settings()

    def test_explicit_null_and_false_reach_uvicorn(self) -> None:
        options = UvicornServerSettings.model_validate(
            {"log_config": None, "access_log": False}
        ).as_dict
        with (
            override_settings(UVICORN=options),
            patch("moodlehack.serve.runner.uvicorn.run") as start,
        ):
            runserver()
        start.assert_called_once_with(
            app="moodlehack.serve.asgi:application",
            log_config=None,
            access_log=False,
        )

    @override_settings(UVICORN={}, SECRET_KEY_IS_UNSAFE=False)
    def test_cli_without_options_does_not_forward_defaults(self) -> None:
        command = Command()
        with (
            patch("moodlehack.serve.runserver") as start,
            patch.object(command.console, "print"),
        ):
            start.side_effect = lambda: self.assertEqual(
                cast(dict[str, object], settings.UVICORN), {}
            )
            command.runserver(migrate=False, collectstatic=False)
        start.assert_called_once_with()

    @override_settings(
        UVICORN={"port": 8001, "access_log": False},
        SECRET_KEY_IS_UNSAFE=False,
    )
    def test_cli_overrides_and_restores_configuration_on_failure(self) -> None:
        command = Command()

        def fail_after_checking_options() -> None:
            self.assertEqual(
                cast(dict[str, object], settings.UVICORN),
                {
                    "host": "0.0.0.0",
                    "port": 0,
                    "access_log": False,
                },
            )
            raise RuntimeError("Server failed")

        with (
            patch(
                "moodlehack.serve.runserver",
                side_effect=fail_after_checking_options,
            ),
            patch.object(command.console, "print"),
            self.assertRaisesRegex(RuntimeError, "Server failed"),
        ):
            command.runserver(
                host="0.0.0.0",
                port=0,
                migrate=False,
                collectstatic=False,
            )
        self.assertEqual(
            cast(dict[str, object], settings.UVICORN),
            {"port": 8001, "access_log": False},
        )
