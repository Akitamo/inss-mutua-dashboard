"""
Módulo SRC - Dashboard INSS vs Mutua
===================================

Módulo principal que contiene la lógica de procesamiento y visualización
del Dashboard INSS vs Mutua.

Módulos incluidos:
- data_processor: Procesamiento y limpieza de datos
- visualizations: Creación de gráficos y visualizaciones
"""

from .data_processor import DataProcessor
from .visualizations import VisualizationManager

__all__ = ['DataProcessor', 'VisualizationManager']
__version__ = '1.0.0'
