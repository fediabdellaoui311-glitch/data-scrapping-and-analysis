"""
Module de génération des visualisations
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Configuration du style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class Visualizer:
    """Classe pour générer toutes les visualisations"""
    
    def __init__(self, data: pd.DataFrame, model=None):
        """
        Initialise le visualiseur
        
        Args:
            data (pd.DataFrame): DataFrame avec les données
            model: Modèle de régression (optionnel)
        """
        self.data = data
        self.model = model
        
    def plot_time_series(self, filepath: str = "output/evolution_temporelle.png"):
        """
        Génère le graphique d'évolution temporelle
        
        Args:
            filepath (str): Chemin de sauvegarde
        """
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Dow Jones
        axes[0].plot(self.data['Date'], self.data['DJI_Close'], 
                    color='#2E86AB', linewidth=1.5, alpha=0.8)
        axes[0].fill_between(self.data['Date'], self.data['DJI_Close'], 
                            alpha=0.3, color='#2E86AB')
        axes[0].set_title('Évolution du Dow Jones Industrial Average', 
                         fontsize=16, fontweight='bold', pad=20)
        axes[0].set_ylabel('Indice DJI', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3, linestyle='--')
        axes[0].tick_params(axis='both', which='major', labelsize=10)
        
        # Calculer et afficher la tendance
        z = np.polyfit(range(len(self.data)), self.data['DJI_Close'], 1)
        p = np.poly1d(z)
        axes[0].plot(self.data['Date'], p(range(len(self.data))), 
                    "r--", alpha=0.6, linewidth=2, label='Tendance')
        axes[0].legend(loc='upper left', fontsize=10)
        
        # CO2
        axes[1].plot(self.data['Date'], self.data['CO2_Level'], 
                    color='#A23B72', linewidth=1.5, alpha=0.8)
        axes[1].fill_between(self.data['Date'], self.data['CO2_Level'], 
                            alpha=0.3, color='#A23B72')
        axes[1].set_title('Évolution des Émissions de CO2 Atmosphériques', 
                         fontsize=16, fontweight='bold', pad=20)
        axes[1].set_ylabel('CO2 (ppm)', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Date', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3, linestyle='--')
        axes[1].tick_params(axis='both', which='major', labelsize=10)
        
        # Calculer et afficher la tendance CO2
        z = np.polyfit(range(len(self.data)), self.data['CO2_Level'], 1)
        p = np.poly1d(z)
        axes[1].plot(self.data['Date'], p(range(len(self.data))), 
                    "r--", alpha=0.6, linewidth=2, label='Tendance')
        axes[1].legend(loc='upper left', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
    def plot_regression(self, filepath: str = "output/regression_plot.png"):
        """
        Génère le graphique de régression
        
        Args:
            filepath (str): Chemin de sauvegarde
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Nuage de points et régression
        sns.regplot(x='CO2_Level', y='DJI_Close', data=self.data,
                   scatter_kws={'alpha': 0.4, 's': 30, 'color': '#2E86AB'},
                   line_kws={'color': '#A23B72', 'linewidth': 2.5})
        
        # Titre et labels
        if self.model:
            r2 = self.model.rsquared
            title = f'Régression Linéaire: Dow Jones vs CO2\nR² = {r2:.4f}'
        else:
            title = 'Régression Linéaire: Dow Jones vs CO2'
            
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Niveau de CO2 (ppm)', fontsize=13, fontweight='bold')
        ax.set_ylabel('Indice Dow Jones', fontsize=13, fontweight='bold')
        
        # Grille
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Ajouter l'équation de régression si modèle disponible
        if self.model:
            const = self.model.params[0]
            slope = self.model.params[1]
            equation = f'y = {slope:.2f}x + {const:.2f}'
            ax.text(0.05, 0.95, equation, transform=ax.transAxes,
                   fontsize=12, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def plot_residuals_analysis(self, filepath: str = "output/residuals_analysis.png"):
        """
        Génère l'analyse des résidus
        
        Args:
            filepath (str): Chemin de sauvegarde
        """
        if self.model is None:
            logger.warning("Pas de modèle disponible pour l'analyse des résidus")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        residuals = self.model.resid
        fitted = self.model.fittedvalues
        
        # 1. Résidus vs Valeurs ajustées
        axes[0, 0].scatter(fitted, residuals, alpha=0.5, s=20, color='#2E86AB')
        axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
        axes[0, 0].set_xlabel('Valeurs Ajustées', fontweight='bold')
        axes[0, 0].set_ylabel('Résidus', fontweight='bold')
        axes[0, 0].set_title('Résidus vs Valeurs Ajustées', fontweight='bold', pad=10)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Q-Q Plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Q-Q Plot (Normalité des Résidus)', fontweight='bold', pad=10)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Histogramme des résidus
        axes[1, 0].hist(residuals, bins=50, alpha=0.7, color='#A23B72', edgecolor='black')
        axes[1, 0].set_xlabel('Résidus', fontweight='bold')
        axes[1, 0].set_ylabel('Fréquence', fontweight='bold')
        axes[1, 0].set_title('Distribution des Résidus', fontweight='bold', pad=10)
        axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 4. Résidus vs Ordre
        axes[1, 1].plot(residuals, alpha=0.7, color='#2E86AB', linewidth=1)
        axes[1, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
        axes[1, 1].set_xlabel('Ordre des observations', fontweight='bold')
        axes[1, 1].set_ylabel('Résidus', fontweight='bold')
        axes[1, 1].set_title('Résidus vs Ordre (Autocorrélation)', fontweight='bold', pad=10)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
    
    def plot_correlation_heatmap(self, filepath: str = "output/correlation_matrix.png"):
        """
        Génère une heatmap de corrélation
        
        Args:
            filepath (str): Chemin de sauvegarde
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Calculer la matrice de corrélation
        corr_matrix = self.data[['DJI_Close', 'CO2_Level']].corr()
        
        # Heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.4f', cmap='coolwarm',
                   center=0, square=True, linewidths=2, cbar_kws={"shrink": 0.8},
                   vmin=-1, vmax=1, ax=ax)
        
        ax.set_title('Matrice de Corrélation', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
