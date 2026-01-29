"""
Projet d'Analyse Économétrique : Impact du CO2 sur le Dow Jones
Auteur: ABDELLAOUI FEDI
Description: Analyse de la relation entre les émissions de CO2 et la performance du Dow Jones
"""

import sys
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output/analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import des modules du projet
from data_collector import DataCollector
from statistical_analysis import StatisticalAnalyzer
from visualizations import Visualizer
from report_generator import ReportGenerator


class EconometricAnalysis:
    """Classe principale pour orchestrer l'analyse économétrique"""
    
    def __init__(self, start_date="2015-01-01"):
        """
        Initialise l'analyse économétrique
        
        Args:
            start_date (str): Date de début pour la collecte des données
        """
        self.start_date = start_date
        self.data = None
        self.stats = {}
        self.models = {}
        
        # Créer les dossiers de sortie
        Path("output").mkdir(exist_ok=True)
        Path("data").mkdir(exist_ok=True)
        
    def run_analysis(self):
        """Exécute l'analyse complète"""
        try:
            logger.info("=" * 80)
            logger.info("DÉBUT DE L'ANALYSE ÉCONOMÉTRIQUE")
            logger.info("=" * 80)
            
            # 1. Collecte des données
            self._collect_data()
            
            # 2. Analyse statistique
            self._perform_statistical_analysis()
            
            # 3. Génération des visualisations
            self._generate_visualizations()
            
            # 4. Génération du rapport
            self._generate_report()
            
            logger.info("=" * 80)
            logger.info("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
            logger.info("=" * 80)
            logger.info("Fichiers générés:")
            logger.info("  📊 data/dow_jones_co2_data.csv")
            logger.info("  📈 output/evolution_temporelle.png")
            logger.info("  📉 output/regression_plot.png")
            logger.info("  📉 output/residuals_analysis.png")
            logger.info("  📄 output/Rapport_Econometrique_Complet.pdf")
            logger.info("  📝 output/analysis.log")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse: {str(e)}", exc_info=True)
            raise
    
    def _collect_data(self):
        """Collecte et prépare les données"""
        logger.info("\n📊 ÉTAPE 1: COLLECTE DES DONNÉES")
        logger.info("-" * 80)
        
        collector = DataCollector(self.start_date)
        self.data = collector.collect_all_data()
        
        logger.info(f"✅ {len(self.data)} observations collectées")
        logger.info(f"   Période: {self.data['Date'].min()} à {self.data['Date'].max()}")
        
    def _perform_statistical_analysis(self):
        """Effectue l'analyse statistique complète"""
        logger.info("\n🔬 ÉTAPE 2: ANALYSE STATISTIQUE")
        logger.info("-" * 80)
        
        analyzer = StatisticalAnalyzer(self.data)
        
        # Statistiques descriptives
        self.stats['descriptive'] = analyzer.compute_descriptive_stats()
        logger.info("✅ Statistiques descriptives calculées")
        
        # Tests de normalité
        self.stats['normality'] = analyzer.test_normality()
        logger.info("✅ Tests de normalité effectués")
        
        # Tests de stationnarité
        self.stats['stationarity'] = analyzer.test_stationarity()
        logger.info("✅ Tests de stationnarité effectués")
        
        # Corrélation
        self.stats['correlation'] = analyzer.compute_correlation()
        logger.info(f"✅ Corrélation calculée: {self.stats['correlation']:.4f}")
        
        # Régression OLS
        self.models['ols'] = analyzer.run_ols_regression()
        logger.info(f"✅ Régression OLS: R² = {self.models['ols'].rsquared:.4f}")
        
        # Tests d'hétéroscédasticité
        self.stats['heteroscedasticity'] = analyzer.test_heteroscedasticity()
        logger.info("✅ Tests d'hétéroscédasticité effectués")
        
        # Tests d'autocorrélation
        self.stats['autocorrelation'] = analyzer.test_autocorrelation()
        logger.info("✅ Tests d'autocorrélation effectués")
        
        # Régression WLS (si hétéroscédasticité détectée)
        if self.stats['heteroscedasticity']['has_heteroscedasticity']:
            self.models['wls'] = analyzer.run_wls_regression()
            logger.info(f"✅ Régression WLS: R² = {self.models['wls'].rsquared:.4f}")
        
    def _generate_visualizations(self):
        """Génère toutes les visualisations"""
        logger.info("\n🎨 ÉTAPE 3: GÉNÉRATION DES VISUALISATIONS")
        logger.info("-" * 80)
        
        viz = Visualizer(self.data, self.models.get('ols'))
        
        viz.plot_time_series()
        logger.info("✅ Graphique d'évolution temporelle créé")
        
        viz.plot_regression()
        logger.info("✅ Graphique de régression créé")
        
        viz.plot_residuals_analysis()
        logger.info("✅ Analyse des résidus créée")
        
    def _generate_report(self):
        """Génère le rapport PDF complet"""
        logger.info("\n📄 ÉTAPE 4: GÉNÉRATION DU RAPPORT PDF")
        logger.info("-" * 80)
        
        report = ReportGenerator(
            data=self.data,
            stats=self.stats,
            models=self.models
        )
        report.generate_full_report()
        
        logger.info("✅ Rapport PDF généré")


def main():
    """Point d'entrée principal du programme"""
    try:
        # Créer et exécuter l'analyse
        analysis = EconometricAnalysis(start_date="2015-01-01")
        analysis.run_analysis()
        
        print("\n" + "=" * 80)
        print("🎉 ANALYSE COMPLÈTE RÉUSSIE !")
        print("=" * 80)
        print("\nConsultez les fichiers dans le dossier 'output/'")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Analyse interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Erreur fatale: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
