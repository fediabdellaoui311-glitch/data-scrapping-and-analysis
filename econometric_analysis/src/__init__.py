"""
Projet d'Analyse Économétrique : Impact du CO2 sur le Dow Jones
Version: 1.0.0
Auteur: ABDELLAOUI FEDI
"""

__version__ = "1.0.0"
__author__ = "ABDELLAOUI FEDI"
__email__ = "votre.email@example.com"

from .data_collector import DataCollector
from .statistical_analysis import StatisticalAnalyzer
from .visualizations import Visualizer
from .report_generator import ReportGenerator

__all__ = [
    'DataCollector',
    'StatisticalAnalyzer',
    'Visualizer',
    'ReportGenerator'
]
