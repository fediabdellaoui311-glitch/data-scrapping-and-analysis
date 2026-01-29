"""
Module de collecte des données depuis les APIs
"""

import pandas as pd
import yfinance as yf
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class DataCollector:
    """Collecte et prépare les données du Dow Jones et du CO2"""
    
    def __init__(self, start_date: str = "2015-01-01"):
        """
        Initialise le collecteur de données
        
        Args:
            start_date (str): Date de début pour la collecte (format: YYYY-MM-DD)
        """
        self.start_date = start_date
        self.df_merged = None
        
    def collect_dow_jones_data(self) -> pd.DataFrame:
        """
        Collecte les données du Dow Jones depuis Yahoo Finance
        
        Returns:
            pd.DataFrame: DataFrame avec les colonnes Date et DJI_Close
        """
        logger.info("  📥 Téléchargement des données Dow Jones...")
        
        try:
            df = yf.download("^DJI", start=self.start_date, progress=False)[['Close']].reset_index()
            df.columns = ['Date', 'DJI_Close']
            logger.info(f"     ✓ {len(df)} observations Dow Jones récupérées")
            return df
            
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement Dow Jones: {str(e)}")
            raise
    
    def collect_co2_data(self) -> pd.DataFrame:
        """
        Collecte les données de CO2 depuis l'API Global Warming
        
        Returns:
            pd.DataFrame: DataFrame avec les colonnes Date et CO2_Level
        """
        logger.info("  📥 Téléchargement des données CO2...")
        
        try:
            response = requests.get(
                "https://global-warming.org/api/co2-api",
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data['co2'])
            
            # Conversion des dates
            df['Date'] = pd.to_datetime(df[['year', 'month', 'day']])
            df['CO2_Level'] = df['trend'].astype(float)
            
            # Sélection des colonnes pertinentes
            df = df[['Date', 'CO2_Level']]
            
            logger.info(f"     ✓ {len(df)} observations CO2 récupérées")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors du téléchargement CO2: {str(e)}")
            raise
    
    def merge_datasets(self, df_dj: pd.DataFrame, df_co2: pd.DataFrame) -> pd.DataFrame:
        """
        Fusionne les datasets Dow Jones et CO2
        
        Args:
            df_dj (pd.DataFrame): DataFrame Dow Jones
            df_co2 (pd.DataFrame): DataFrame CO2
            
        Returns:
            pd.DataFrame: DataFrame fusionné et nettoyé
        """
        logger.info("  🔗 Fusion des datasets...")
        
        # Fusion sur la date
        df = pd.merge(df_dj, df_co2, on='Date', how='inner')
        
        # Suppression des valeurs manquantes
        initial_len = len(df)
        df = df.dropna()
        removed = initial_len - len(df)
        
        if removed > 0:
            logger.info(f"     ⚠️ {removed} observations avec valeurs manquantes supprimées")
        
        logger.info(f"     ✓ Dataset final: {len(df)} observations")
        
        return df
    
    def save_data(self, df: pd.DataFrame, filepath: str = "data/dow_jones_co2_data.csv"):
        """
        Sauvegarde le dataset au format CSV
        
        Args:
            df (pd.DataFrame): DataFrame à sauvegarder
            filepath (str): Chemin du fichier de sortie
        """
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"  💾 Données sauvegardées: {filepath}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {str(e)}")
            raise
    
    def collect_all_data(self) -> pd.DataFrame:
        """
        Collecte, fusionne et sauvegarde toutes les données
        
        Returns:
            pd.DataFrame: DataFrame complet prêt pour l'analyse
        """
        # Collecte
        df_dj = self.collect_dow_jones_data()
        df_co2 = self.collect_co2_data()
        
        # Fusion
        df_merged = self.merge_datasets(df_dj, df_co2)
        
        # Sauvegarde
        self.save_data(df_merged)
        
        self.df_merged = df_merged
        return df_merged
    
    def get_data_summary(self) -> Dict:
        """
        Retourne un résumé des données collectées
        
        Returns:
            Dict: Dictionnaire avec les informations clés
        """
        if self.df_merged is None:
            raise ValueError("Aucune donnée collectée. Exécutez collect_all_data() d'abord.")
        
        return {
            'n_observations': len(self.df_merged),
            'date_start': self.df_merged['Date'].min(),
            'date_end': self.df_merged['Date'].max(),
            'dji_range': (self.df_merged['DJI_Close'].min(), self.df_merged['DJI_Close'].max()),
            'co2_range': (self.df_merged['CO2_Level'].min(), self.df_merged['CO2_Level'].max())
        }
