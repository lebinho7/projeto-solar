"""Pacote projeto_solar

Exporta interfaces principais para uso externo.
"""

__all__ = [
	"get_data",
	"clear_cache",
	"calcular_tudo",
	"plotar_dashboard_final",
	"config",
]

__version__ = "0.1.0"

from .geodata import get_data, clear_cache
from .engineering import calcular_tudo
from .viz import plotar_dashboard_final
from . import config