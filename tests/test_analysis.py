"""
Tests unitaires pour le module d'analyse économétrique
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from statistical_analysis import StatisticalAnalyzer


class TestStatisticalAnalyzer(unittest.TestCase):
    """Tests pour la classe StatisticalAnalyzer"""
    
    def setUp(self):
        """Prépare des données de test"""
        # Créer des données fictives
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        self.test_data = pd.DataFrame({
            'Date': dates,
            'DJI_Close': np.random.randn(100) * 1000 + 30000,
            'CO2_Level': np.random.randn(100) * 10 + 400
        })
        
        self.analyzer = StatisticalAnalyzer(self.test_data)
    
    def test_compute_descriptive_stats(self):
        """Test du calcul des statistiques descriptives"""
        stats = self.analyzer.compute_descriptive_stats()
        
        # Vérifier la structure
        self.assertIn('DJI', stats)
        self.assertIn('CO2', stats)
        
        # Vérifier les clés
        expected_keys = ['mean', 'std', 'var', 'min', 'max', 'median', 'q1', 'q3']
        for key in expected_keys:
            self.assertIn(key, stats['DJI'])
            self.assertIn(key, stats['CO2'])
        
        # Vérifier que les valeurs sont des nombres
        self.assertIsInstance(stats['DJI']['mean'], (int, float))
        self.assertIsInstance(stats['CO2']['std'], (int, float))
    
    def test_compute_correlation(self):
        """Test du calcul de corrélation"""
        corr = self.analyzer.compute_correlation()
        
        # Vérifier que c'est un float
        self.assertIsInstance(corr, (int, float))
        
        # Vérifier que c'est dans [-1, 1]
        self.assertGreaterEqual(corr, -1)
        self.assertLessEqual(corr, 1)
    
    def test_test_normality(self):
        """Test du test de normalité"""
        norm_results = self.analyzer.test_normality()
        
        # Vérifier la structure
        self.assertIn('DJI', norm_results)
        self.assertIn('CO2', norm_results)
        
        # Vérifier les clés
        self.assertIn('statistic', norm_results['DJI'])
        self.assertIn('p_value', norm_results['DJI'])
        self.assertIn('is_normal', norm_results['DJI'])
        
        # Vérifier les types
        self.assertIsInstance(norm_results['DJI']['is_normal'], bool)
    
    def test_test_stationarity(self):
        """Test du test de stationnarité"""
        stat_results = self.analyzer.test_stationarity()
        
        # Vérifier la structure
        self.assertIn('DJI', stat_results)
        self.assertIn('CO2', stat_results)
        
        # Vérifier les clés
        self.assertIn('adf_statistic', stat_results['DJI'])
        self.assertIn('p_value', stat_results['DJI'])
        self.assertIn('is_stationary', stat_results['DJI'])
    
    def test_run_ols_regression(self):
        """Test de la régression OLS"""
        model = self.analyzer.run_ols_regression()
        
        # Vérifier que le modèle a les attributs nécessaires
        self.assertTrue(hasattr(model, 'rsquared'))
        self.assertTrue(hasattr(model, 'params'))
        self.assertTrue(hasattr(model, 'pvalues'))
        
        # Vérifier que R² est dans [0, 1]
        self.assertGreaterEqual(model.rsquared, 0)
        self.assertLessEqual(model.rsquared, 1)
        
        # Vérifier qu'il y a 2 paramètres (constante + coefficient)
        self.assertEqual(len(model.params), 2)


class TestDataValidation(unittest.TestCase):
    """Tests de validation des données"""
    
    def test_missing_values(self):
        """Test de détection des valeurs manquantes"""
        # Créer des données avec des NaN
        data_with_nan = pd.DataFrame({
            'Date': pd.date_range(start='2020-01-01', periods=10, freq='D'),
            'DJI_Close': [100, np.nan, 200, 300, 400, 500, 600, 700, 800, 900],
            'CO2_Level': [400, 401, np.nan, 403, 404, 405, 406, 407, 408, 409]
        })
        
        # Vérifier qu'il y a bien des NaN
        self.assertTrue(data_with_nan.isnull().any().any())
        
        # Après suppression des NaN
        data_clean = data_with_nan.dropna()
        self.assertFalse(data_clean.isnull().any().any())
        self.assertEqual(len(data_clean), 8)


if __name__ == '__main__':
    unittest.main()
