"""
Rich terminal dashboard for live simulation metrics.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text

from graviton.constants import C, G, HBAR

console = Console()


class Dashboard:
    """
    Print a formatted terminal dashboard showing key simulation parameters
    and computed results.
    """

    @staticmethod
    def show_alcubierre(
        velocity_c: float,
        radius: float,
        sigma: float,
        exotic_energy: float,
        hawking_temp: float,
        causally_disconnected: bool,
    ):
        """Display Alcubierre warp bubble dashboard."""
        table = Table(title="ALCUBIERRE WARP DRIVE",
                      show_header=True, header_style="bold magenta")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Warp Velocity",
                      f"{velocity_c:.2f} c  ({velocity_c * C:.3e} m/s)")
        table.add_row("Bubble Radius", f"{radius:.1f} m")
        table.add_row("Wall Thickness (sigma)", f"{sigma:.1f}")
        table.add_row("Total Exotic Energy", f"{exotic_energy:.3e} J")
        table.add_row("Hawking-like Temp", f"{hawking_temp:.3e} K")
        table.add_row("Causally Disconnected", str(causally_disconnected))

        console.print(Panel(table, border_style="blue"))

    @staticmethod
    def show_gravitomagnetic(
        mass: float,
        angular_momentum_mag: float,
        precession_rate: float,
    ):
        """Display gravitomagnetic metrics."""
        table = Table(title="GRAVITOMAGNETIC FIELD",
                      show_header=True, header_style="bold magenta")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Central Mass", f"{mass:.3e} kg")
        table.add_row("Angular Momentum |J|",
                      f"{angular_momentum_mag:.3e} kg m^2/s")
        table.add_row("LT Precession Rate", f"{precession_rate:.3e} rad/s")

        console.print(Panel(table, border_style="green"))

    @staticmethod
    def show_casimir(separation: float, force_pa: float, energy_density: float):
        """Display Casimir effect metrics."""
        table = Table(title="CASIMIR EFFECT", show_header=True,
                      header_style="bold magenta")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Plate Separation",
                      f"{separation:.3e} m  ({separation * 1e9:.1f} nm)")
        table.add_row("Force/Area", f"{force_pa:.3e} Pa")
        table.add_row("Energy Density", f"{energy_density:.3e} J/m^3")

        console.print(Panel(table, border_style="red"))

    @staticmethod
    def show_geodesic(
        metric_type: str,
        mass: float,
        r_s: float,
        isco: float,
    ):
        """Display geodesic simulation metrics."""
        table = Table(title=f"GEODESICS — {metric_type.upper()}",
                      show_header=True, header_style="bold magenta")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Central Mass", f"{mass:.3e} kg")
        table.add_row("Schwarzschild Radius", f"{r_s:.3e} m")
        table.add_row("ISCO Radius", f"{isco:.3e} m  ({isco / r_s:.2f} r_s)")

        console.print(Panel(table, border_style="yellow"))

    @staticmethod
    def header():
        """Print the GRAVITON header."""
        banner = Text()
        banner.append("\n  GRAVITON", style="bold white on blue")
        banner.append(
            "  Exotic Propulsion & Spacetime Engineering Simulator\n", style="bold cyan")
        console.print(Panel(banner, border_style="bright_blue"))
