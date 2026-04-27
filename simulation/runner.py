"""
Unified simulation runner for all GRAVITON modules.
"""

import time
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table

console = Console()


class SimulationRunner:
    """
    Unified entry-point to run any GRAVITON physics module with
    parameter sweeps and result collection.
    """

    MODULES = {
        "alcubierre": "alcubierre.metric.AlcubierreMetric",
        "energy": "alcubierre.energy.ExoticEnergyCalculator",
        "bubble": "alcubierre.bubble.WarpBubble",
        "gem": "gravitomagnetic.gem_equations.GravitoElectroMagneticField",
        "frame_dragging": "gravitomagnetic.frame_dragging.FrameDragging",
        "casimir": "zpe.casimir.CasimirEffect",
        "vacuum": "zpe.quantum_vacuum.QuantumVacuumField",
        "schwarzschild": "geodesic.schwarzschild.SchwarzschildGeodesic",
        "kerr": "geodesic.kerr.KerrGeodesic",
    }

    def __init__(self):
        self.results: Dict[str, Any] = {}

    @staticmethod
    def _import_class(dotted_path: str):
        """Dynamically import a class from a dotted module path."""
        parts = dotted_path.rsplit(".", 1)
        module_path, class_name = parts
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, class_name)

    def run(self, module_name: str, params: Dict[str, Any] = None) -> Any:
        """
        Instantiate and run a GRAVITON module.

        Parameters
        ----------
        module_name : str
            Key from MODULES dict (e.g. 'alcubierre', 'casimir').
        params : dict
            Keyword arguments passed to the module constructor.

        Returns the instantiated module object.
        """
        if module_name not in self.MODULES:
            raise ValueError(
                f"Unknown module '{module_name}'. Available: {list(self.MODULES.keys())}"
            )

        params = params or {}
        cls = self._import_class(self.MODULES[module_name])
        console.print(
            f"[bold cyan]Running {module_name}[/bold cyan] with params: {params}")

        t0 = time.time()
        instance = cls(**params)
        elapsed = time.time() - t0

        self.results[module_name] = {
            "instance": instance,
            "params": params,
            "init_time_s": elapsed,
        }

        console.print(f"  Initialised in {elapsed:.4f}s")
        return instance

    def list_modules(self):
        """Print available modules."""
        table = Table(title="GRAVITON Modules")
        table.add_column("Name", style="cyan")
        table.add_column("Class Path", style="green")
        for name, path in self.MODULES.items():
            table.add_row(name, path)
        console.print(table)

    def summary(self):
        """Print a summary of all runs."""
        if not self.results:
            console.print("[yellow]No simulations run yet.[/yellow]")
            return

        table = Table(title="Simulation Results")
        table.add_column("Module", style="cyan")
        table.add_column("Params")
        table.add_column("Init Time", style="green")
        for name, data in self.results.items():
            table.add_row(name, str(data["params"]),
                          f"{data['init_time_s']:.4f}s")
        console.print(table)
