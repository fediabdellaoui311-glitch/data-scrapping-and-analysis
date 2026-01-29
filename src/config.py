"""
Fichier de configuration pour l'analyse économétrique
"""

# Configuration des données
DATA_CONFIG = {
    'dow_jones_ticker': '^DJI',  # Symbole Yahoo Finance pour le Dow Jones
    'start_date': '2015-01-01',
    'co2_api_url': 'https://global-warming.org/api/co2-api',
    'data_output_path': 'data/dow_jones_co2_data.csv'
}

# Configuration de l'analyse statistique
ANALYSIS_CONFIG = {
    'significance_level': 0.05,  # Niveau de significativité (5%)
    'normality_test_sample_size': 5000,  # Taille de l'échantillon pour Shapiro-Wilk
    'autocorrelation_lags': 10  # Nombre de retards pour Breusch-Godfrey
}

# Configuration des visualisations
VISUALIZATION_CONFIG = {
    'figure_dpi': 300,
    'style': 'whitegrid',
    'color_primary': '#2E86AB',  # Bleu
    'color_secondary': '#A23B72',  # Violet
    'figure_size': (12, 8)
}

# Configuration du rapport PDF
REPORT_CONFIG = {
    'output_path': 'output/Rapport_Econometrique_Complet.pdf',
    'font_family': 'Arial',
    'title_size': 24,
    'chapter_size': 14,
    'section_size': 12,
    'text_size': 11,
    'include_visualizations': True,
    'include_bibliography': True
}

# Configuration du logging
LOGGING_CONFIG = {
    'log_file': 'output/analysis.log',
    'log_level': 'INFO',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s'
}

# Chemins des fichiers de sortie
OUTPUT_PATHS = {
    'time_series': 'output/evolution_temporelle.png',
    'regression': 'output/regression_plot.png',
    'residuals': 'output/residuals_analysis.png',
    'correlation': 'output/correlation_matrix.png',
    'report': 'output/Rapport_Econometrique_Complet.pdf'
}

# Messages personnalisés
MESSAGES = {
    'start': '='*80 + '\nDÉBUT DE L\'ANALYSE ÉCONOMÉTRIQUE\n' + '='*80,
    'end': '='*80 + '\n✅ ANALYSE TERMINÉE AVEC SUCCÈS\n' + '='*80,
    'data_collection': '\n📊 ÉTAPE 1: COLLECTE DES DONNÉES\n' + '-'*80,
    'statistical_analysis': '\n🔬 ÉTAPE 2: ANALYSE STATISTIQUE\n' + '-'*80,
    'visualization': '\n🎨 ÉTAPE 3: GÉNÉRATION DES VISUALISATIONS\n' + '-'*80,
    'report_generation': '\n📄 ÉTAPE 4: GÉNÉRATION DU RAPPORT PDF\n' + '-'*80
}
