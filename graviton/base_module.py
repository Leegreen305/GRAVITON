"""
Abstract base class for all GRAVITON physics modules.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np


class PhysicsModule(ABC):
    """
    Base class that every GRAVITON physics module must inherit.

    Provides a consistent interface for parameter management, computation,
    and result retrieval across all simulation modules.
    """

    def __init__(self, name: str, **params):
        self.name = name
        self.params: Dict[str, Any] = params
        self._results: Dict[str, Any] = {}

    @abstractmethod
    def compute(self) -> Dict[str, Any]:
        """
        Run the core physics computation.
        Returns a dict of named result arrays / scalars.
        """
        ...

    def get_results(self) -> Dict[str, Any]:
        """Return the last computed results."""
        return self._results

    def update_params(self, **kwargs) -> None:
        """Update simulation parameters."""
        self.params.update(kwargs)

    def summary(self) -> str:
        """Human-readable summary of module state."""
        lines = [f"=== {self.name} ==="]
        for k, v in self.params.items():
            lines.append(f"  {k}: {v}")
        if self._results:
            lines.append("  Results keys: " + ", ".join(self._results.keys()))
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.name})>"
