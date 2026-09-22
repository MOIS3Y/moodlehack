import typing as t
from functools import cached_property

from django.conf import settings
from django.core.management import call_command
from django_typer.management import TyperCommand, command
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.table import Table
from rich.text import Text
from typer import Option

from moodlehack.settings.uvicorn import UvicornServerSettings


@t.final
class Command(TyperCommand):
    """Server management commands for running ASGI server with Uvicorn."""

    help = "Run ASGI server using Uvicorn."

    @cached_property
    def console(self) -> Console:
        """Return the console used by this command instance."""
        return Console()

    @command()
    def runserver(
        self,
        host: t.Annotated[
            str | None, Option(help="Host to bind the server to.")
        ] = None,
        port: t.Annotated[
            int | None, Option(help="Port to bind the server to.")
        ] = None,
        migrate: t.Annotated[
            bool, Option(help="Run migrations before starting server.")
        ] = True,
        collectstatic: t.Annotated[
            bool,
            Option(help="Collect static files before starting server."),
        ] = True,
        verbosity: t.Annotated[
            int,
            Option(
                "--verbose",
                "-v",
                help="Verbosity level (0-3). Use multiple -v for more.",
                count=True,
            ),
        ] = 0,
    ) -> None:
        """
        Run ASGI server using Uvicorn with optional pre-startup tasks.

        Args:
            host: Host address to bind the server
            port: Port number to bind the server
            migrate: Whether to run database migrations before startup
            collectstatic: Whether to collect static files before startup
            verbosity: Output verbosity level (0-3)
        """
        from moodlehack.serve import runserver

        debug = t.cast(bool, settings.DEBUG)

        # Pre-startup tasks with spinner
        if collectstatic and not debug:
            try:
                with Status(
                    "Collecting static files...", console=self.console
                ):
                    _ = call_command(
                        "collectstatic",
                        interactive=False,
                        clear=True,
                        verbosity=verbosity,
                    )
                self.console.print(
                    "[bold green]Static files collected![/bold green]"
                )
            except Exception as e:
                self.console.print(
                    f"[bold red]Static files collection failed: {e}[/bold red]"
                )
                return

        if migrate and not debug:
            try:
                with Status("Applying migrations...", console=self.console):
                    _ = call_command(
                        "migrate", interactive=False, verbosity=verbosity
                    )
                self.console.print(
                    "[bold green]Migrations applied![/bold green]"
                )
            except Exception as e:
                self.console.print(
                    f"[bold red]Migrations failed: {e}[/bold red]"
                )
                return

        # Configuration setup
        options = t.cast(dict[str, object], settings.UVICORN)
        original_config = options.copy()

        if host is not None:
            options["host"] = host
        if port is not None:
            options["port"] = port

        try:
            # Server information display
            display_config: dict[str, object] = (
                UvicornServerSettings.model_validate(options).model_dump()
            )
            server_info = Table(show_header=False, box=None)
            server_info.add_column(style="bold cyan")
            server_info.add_column(style="white")

            server_info.add_row("Server", "Uvicorn")
            server_info.add_row("Host", str(display_config["host"]))
            server_info.add_row("Port", str(display_config["port"]))

            # Debug status highlighting
            debug_status = "Enabled" if debug else "Disabled"
            debug_style = "bold red" if debug else "white"
            debug_value = Text(debug_status, style=debug_style)
            server_info.add_row("Debug", debug_value)

            # Security alert:
            # Show ONLY if the key is still the default unsafe one
            if t.cast(bool, settings.SECRET_KEY_IS_UNSAFE):
                # Create a composite text with different colors
                key_warning = Text()
                _ = key_warning.append("UNSAFE ", style="bold red")
                _ = key_warning.append("(Default Value)", style="yellow")

                server_info.add_row("Secret Key", key_warning)

            # Show verbosity level if > 0
            if verbosity > 0:
                server_info.add_row("Verbosity", str(verbosity))

            self.console.print(
                Panel(
                    server_info,
                    title="[bold green]Starting Server[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                )
            )

            runserver()

        finally:
            # Restore original configuration
            settings.UVICORN = original_config
            self.console.print(
                "[bold yellow]Server shutdown completed.[/bold yellow]"
            )
