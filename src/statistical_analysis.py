"""
Module d'analyse statistique et économétrique
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, acorr_breusch_godfrey
from statsmodels.stats.stattools import durbin_watson
from scipy.stats import shapiro
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Classe pour effectuer toutes les analyses statistiques"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialise l'analyseur statistique
        
        Args:
            data (pd.DataFrame): DataFrame avec colonnes DJI_Close et CO2_Level
        """
        self.data = data
        self.X = None
        self.y = None
        self._prepare_regression_data()
        
    def _prepare_regression_data(self):
        """Prépare les données pour la régression"""
        self.y = self.data['DJI_Close']
        self.X = sm.add_constant(self.data['CO2_Level'])
    
    def compute_descriptive_stats(self) -> Dict:
        """
        Calcule les statistiques descriptives
        
        Returns:
            Dict: Statistiques pour DJI et CO2
        """
        stats = {
            'DJI': {
                'mean': self.data['DJI_Close'].mean(),
                'std': self.data['DJI_Close'].std(),
                'var': self.data['DJI_Close'].var(),
                'min': self.data['DJI_Close'].min(),
                'max': self.data['DJI_Close'].max(),
                'median': self.data['DJI_Close'].median(),
                'q1': self.data['DJI_Close'].quantile(0.25),
                'q3': self.data['DJI_Close'].quantile(0.75)
            },
            'CO2': {
                'mean': self.data['CO2_Level'].mean(),
                'std': self.data['CO2_Level'].std(),
                'var': self.data['CO2_Level'].var(),
                'min': self.data['CO2_Level'].min(),
                'max': self.data['CO2_Level'].max(),
                'median': self.data['CO2_Level'].median(),
                'q1': self.data['CO2_Level'].quantile(0.25),
                'q3': self.data['CO2_Level'].quantile(0.75)
            }
        }
        
        return stats
    
    def test_normality(self, sample_size: int = 5000) -> Dict:
        """
        Teste la normalité avec Shapiro-Wilk
        
        Args:
            sample_size (int): Taille de l'échantillon pour le test
            
        Returns:
            Dict: Résultats des tests de normalité
        """
        n = min(sample_size, len(self.data))
        
        # Test pour DJI
        sample_dji = self.data['DJI_Close'].sample(n, random_state=42)
        stat_dji, p_dji = shapiro(sample_dji)
        
        # Test pour CO2
        sample_co2 = self.data['CO2_Level'].sample(n, random_state=42)
        stat_co2, p_co2 = shapiro(sample_co2)
        
        return {
            'DJI': {
                'statistic': stat_dji,
                'p_value': p_dji,
                'is_normal': p_dji > 0.05
            },
            'CO2': {
                'statistic': stat_co2,
                'p_value': p_co2,
                'is_normal': p_co2 > 0.05
            }
        }
    
    def test_stationarity(self) -> Dict:
        """
        Teste la stationnarité avec ADF (Augmented Dickey-Fuller)
        
        Returns:
            Dict: Résultats des tests ADF
        """
        # Test pour DJI
        adf_dji = adfuller(self.data['DJI_Close'])
        
        # Test pour CO2
        adf_co2 = adfuller(self.data['CO2_Level'])
        
        return {
            'DJI': {
                'adf_statistic': adf_dji[0],
                'p_value': adf_dji[1],
                'critical_values': adf_dji[4],
                'is_stationary': adf_dji[1] < 0.05
            },
            'CO2': {
                'adf_statistic': adf_co2[0],
                'p_value': adf_co2[1],
                'critical_values': adf_co2[4],
                'is_stationary': adf_co2[1] < 0.05
            }
        }
    
    def compute_correlation(self) -> float:
        """
        Calcule la corrélation de Pearson
        
        Returns:
            float: Coefficient de corrélation
        """
        return self.data['DJI_Close'].corr(self.data['CO2_Level'])
    
    def run_ols_regression(self):
        """
        Effectue une régression OLS (Moindres Carrés Ordinaires)
        
        Returns:
            RegressionResults: Résultats de la régression
        """
        model = sm.OLS(self.y, self.X).fit()
        return model
    
    def test_heteroscedasticity(self) -> Dict:
        """
        Teste l'hétéroscédasticité (Breusch-Pagan et White)
        
        Returns:
            Dict: Résultats des tests
        """
        model = self.run_ols_regression()
        
        # Test de Breusch-Pagan
        bp_test = het_breuschpagan(model.resid, self.X)
        
        # Test de White
        white_test = het_white(model.resid, self.X)
        
        return {
            'breusch_pagan': {
                'lm_statistic': bp_test[0],
                'lm_p_value': bp_test[1],
                'f_statistic': bp_test[2],
                'f_p_value': bp_test[3],
                'has_heteroscedasticity': bp_test[1] < 0.05
            },
            'white': {
                'lm_statistic': white_test[0],
                'lm_p_value': white_test[1],
                'f_statistic': white_test[2],
                'f_p_value': white_test[3],
                'has_heteroscedasticity': white_test[1] < 0.05
            },
            'has_heteroscedasticity': bp_test[1] < 0.05 or white_test[1] < 0.05
        }
    
    def test_autocorrelation(self) -> Dict:
        """
        Teste l'autocorrélation (Durbin-Watson et Breusch-Godfrey)
        
        Returns:
            Dict: Résultats des tests
        """
        model = self.run_ols_regression()
        
        # Test de Durbin-Watson
        dw_stat = durbin_watson(model.resid)
        
        # Test de Breusch-Godfrey
        bg_test = acorr_breusch_godfrey(model, nlags=10)
        
        return {
            'durbin_watson': {
                'statistic': dw_stat,
                'has_autocorrelation': dw_stat < 1.5 or dw_stat > 2.5
            },
            'breusch_godfrey': {
                'lm_statistic': bg_test[0],
                'lm_p_value': bg_test[1],
                'f_statistic': bg_test[2],
                'f_p_value': bg_test[3],
                'has_autocorrelation': bg_test[1] < 0.05
            },
            'has_autocorrelation': dw_stat < 1.5 or dw_stat > 2.5 or bg_test[1] < 0.05
        }
    
    def run_wls_regression(self):
        """
        Effectue une régression WLS (Weighted Least Squares) pour corriger l'hétéroscédasticité
        
        Returns:
            RegressionResults: Résultats de la régression WLS
        """
        # Calculer les poids basés sur les résidus OLS
        ols_model = self.run_ols_regression()
        weights = 1 / (ols_model.resid ** 2)
        
        # Régression WLS
        wls_model = sm.WLS(self.y, self.X, weights=weights).fit()
        
        return wls_model
    
    def get_analysis_summary(self) -> Dict:
        """
        Retourne un résumé complet de toutes les analyses
        
        Returns:
            Dict: Résumé complet
        """
        return {
            'descriptive': self.compute_descriptive_stats(),
            'normality': self.test_normality(),
            'stationarity': self.test_stationarity(),
            'correlation': self.compute_correlation(),
            'heteroscedasticity': self.test_heteroscedasticity(),
            'autocorrelation': self.test_autocorrelation()
        }
