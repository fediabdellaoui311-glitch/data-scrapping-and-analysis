"""
Module de génération du rapport PDF
"""

from fpdf import FPDF
import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class PDFReport(FPDF):
    """Classe personnalisée pour le rapport PDF"""
    
    def header(self):
        """En-tête de chaque page"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Analyse Économétrique - Impact du CO2 sur le Dow Jones', 0, 1, 'C')
        self.ln(3)
        
    def footer(self):
        """Pied de page avec numéro"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title: str):
        """Titre de chapitre"""
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(46, 134, 171)  # Bleu
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(4)
    
    def section_title(self, title: str):
        """Titre de section"""
        self.set_font('Arial', 'B', 12)
        self.set_text_color(162, 59, 114)  # Violet
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(2)
    
    def add_text(self, text: str):
        """Ajoute du texte normal"""
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(2)


class ReportGenerator:
    """Génère le rapport PDF complet"""
    
    def __init__(self, data, stats: Dict, models: Dict):
        """
        Initialise le générateur de rapport
        
        Args:
            data: DataFrame avec les données
            stats (Dict): Statistiques calculées
            models (Dict): Modèles de régression
        """
        self.data = data
        self.stats = stats
        self.models = models
        self.pdf = PDFReport()
        
    def _add_cover_page(self):
        """Ajoute la page de garde"""
        self.pdf.add_page()
        
        # Titre principal
        self.pdf.ln(40)
        self.pdf.set_font('Arial', 'B', 24)
        self.pdf.cell(0, 15, "L'IMPACT DU CHANGEMENT CLIMATIQUE", 0, 1, 'C')
        self.pdf.cell(0, 15, "SUR LE DOW JONES", 0, 1, 'C')
        
        # Sous-titre
        self.pdf.ln(20)
        self.pdf.set_font('Arial', 'I', 14)
        self.pdf.cell(0, 10, "Analyse Econometrique Approfondie", 0, 1, 'C')
        
        # Auteur et date
        self.pdf.ln(30)
        self.pdf.set_font('Arial', '', 12)
        self.pdf.cell(0, 10, "Auteur: ABDELLAOUI FEDI", 0, 1, 'C')
        self.pdf.cell(0, 10, "Encadrant: MR. TIEN MOREL", 0, 1, 'C')
        
        # Informations sur les données
        self.pdf.ln(20)
        self.pdf.set_font('Arial', 'I', 10)
        date_start = self.data['Date'].min().strftime('%d/%m/%Y')
        date_end = self.data['Date'].max().strftime('%d/%m/%Y')
        self.pdf.cell(0, 8, f"Periode analysee: {date_start} - {date_end}", 0, 1, 'C')
        self.pdf.cell(0, 8, f"Nombre d'observations: {len(self.data)}", 0, 1, 'C')
        
        # Date de génération
        self.pdf.ln(10)
        self.pdf.set_font('Arial', 'I', 9)
        today = datetime.now().strftime('%d/%m/%Y')
        self.pdf.cell(0, 8, f"Rapport genere le: {today}", 0, 1, 'C')
    
    def _add_introduction(self):
        """Ajoute l'introduction"""
        self.pdf.add_page()
        self.pdf.chapter_title("INTRODUCTION")
        
        intro_text = (
            "Au cours du XXIe siecle, une prise de conscience grandissante s'est presentee "
            "face aux defis lies au changement climatique. Cette recherche vise a analyser "
            "le lien entre les emissions de CO2 et les performances du Dow Jones Industrial "
            "Average (DJIA), l'un des indices boursiers les plus influents.\n\n"
            "Le DJIA represente un indicateur essentiel de l'economie americaine, refletant "
            "la sante generale des marches financiers. Cette etude examine comment les "
            "emissions de CO2, principal marqueur du changement climatique, peuvent influencer "
            "la performance de cet indice boursier."
        )
        self.pdf.add_text(intro_text)
        
        self.pdf.ln(5)
        self.pdf.section_title("Problematique")
        self.pdf.add_text(
            "De quelle maniere le changement climatique, mesure par les emissions de CO2, "
            "influence-t-il la performance du Dow Jones en Amerique ?"
        )
    
    def _add_data_collection(self):
        """Ajoute la section collecte de données"""
        self.pdf.add_page()
        self.pdf.chapter_title("I. COLLECTE DES DONNEES")
        
        self.pdf.section_title("1. Sources des donnees")
        self.pdf.add_text(
            "Les donnees ont ete collectees via scraping web a partir de deux sources principales:\n"
            "- Dow Jones Industrial Average: Yahoo Finance (API yfinance)\n"
            "- Emissions de CO2 atmospheriques: Global Warming API\n\n"
            f"Nombre total d'observations: {len(self.data)}\n"
            f"Periode: {self.data['Date'].min().strftime('%d/%m/%Y')} - "
            f"{self.data['Date'].max().strftime('%d/%m/%Y')}"
        )
        
        self.pdf.section_title("2. Variables etudiees")
        self.pdf.add_text(
            "Variable expliquee (Y): Indice du Dow Jones (DJI_Close)\n"
            "Variable explicative (X): Niveau de CO2 atmospherique (en ppm)\n\n"
            "Modele estime: Y = alpha + beta*X + epsilon\n\n"
            "Hypothese: Une augmentation des emissions de CO2 est associee a une variation "
            "de l'indice Dow Jones."
        )
    
    def _add_descriptive_stats(self):
        """Ajoute les statistiques descriptives"""
        self.pdf.add_page()
        self.pdf.chapter_title("II. STATISTIQUES DESCRIPTIVES")
        
        desc = self.stats['descriptive']
        
        # Dow Jones
        self.pdf.section_title("1. Dow Jones Industrial Average")
        dji_text = (
            f"Moyenne: {desc['DJI']['mean']:.2f}\n"
            f"Ecart-type: {desc['DJI']['std']:.2f}\n"
            f"Variance: {desc['DJI']['var']:.2f}\n"
            f"Minimum: {desc['DJI']['min']:.2f}\n"
            f"Maximum: {desc['DJI']['max']:.2f}\n"
            f"Mediane: {desc['DJI']['median']:.2f}\n"
            f"1er quartile (Q1): {desc['DJI']['q1']:.2f}\n"
            f"3e quartile (Q3): {desc['DJI']['q3']:.2f}"
        )
        self.pdf.add_text(dji_text)
        
        # CO2
        self.pdf.ln(5)
        self.pdf.section_title("2. Emissions de CO2")
        co2_text = (
            f"Moyenne: {desc['CO2']['mean']:.2f} ppm\n"
            f"Ecart-type: {desc['CO2']['std']:.2f}\n"
            f"Variance: {desc['CO2']['var']:.2f}\n"
            f"Minimum: {desc['CO2']['min']:.2f} ppm\n"
            f"Maximum: {desc['CO2']['max']:.2f} ppm\n"
            f"Mediane: {desc['CO2']['median']:.2f} ppm\n"
            f"1er quartile (Q1): {desc['CO2']['q1']:.2f} ppm\n"
            f"3e quartile (Q3): {desc['CO2']['q3']:.2f} ppm"
        )
        self.pdf.add_text(co2_text)
        
        self.pdf.ln(5)
        self.pdf.section_title("3. Interpretation")
        self.pdf.add_text(
            f"Les donnees montrent que le CO2 atmospherique varie entre "
            f"{desc['CO2']['min']:.2f} et {desc['CO2']['max']:.2f} ppm, avec une moyenne de "
            f"{desc['CO2']['mean']:.2f} ppm. L'ecart-type de {desc['CO2']['std']:.2f} indique "
            f"une dispersion moderee des valeurs autour de la moyenne.\n\n"
            f"L'indice Dow Jones presente une plus grande variabilite, avec des valeurs allant de "
            f"{desc['DJI']['min']:.2f} a {desc['DJI']['max']:.2f}, refletant les fluctuations "
            f"normales du marche boursier."
        )
    
    def _add_statistical_tests(self):
        """Ajoute les tests statistiques"""
        self.pdf.add_page()
        self.pdf.chapter_title("III. TESTS STATISTIQUES")
        
        # Test de normalité
        self.pdf.section_title("1. Test de Normalite (Shapiro-Wilk)")
        norm = self.stats['normality']
        norm_text = (
            f"Dow Jones:\n"
            f"  - Statistique: {norm['DJI']['statistic']:.4f}\n"
            f"  - P-value: {norm['DJI']['p_value']:.4f}\n"
            f"  - Distribution normale: {'Oui' if norm['DJI']['is_normal'] else 'Non'}\n\n"
            f"CO2:\n"
            f"  - Statistique: {norm['CO2']['statistic']:.4f}\n"
            f"  - P-value: {norm['CO2']['p_value']:.4f}\n"
            f"  - Distribution normale: {'Oui' if norm['CO2']['is_normal'] else 'Non'}\n\n"
            f"Interpretation: p-value < 0.05 indique un rejet de l'hypothese de normalite."
        )
        self.pdf.add_text(norm_text)
        
        # Test de stationnarité
        self.pdf.ln(5)
        self.pdf.section_title("2. Test de Stationnarite (ADF)")
        stat = self.stats['stationarity']
        stat_text = (
            f"Dow Jones:\n"
            f"  - Statistique ADF: {stat['DJI']['adf_statistic']:.4f}\n"
            f"  - P-value: {stat['DJI']['p_value']:.4f}\n"
            f"  - Serie stationnaire: {'Oui' if stat['DJI']['is_stationary'] else 'Non'}\n\n"
            f"CO2:\n"
            f"  - Statistique ADF: {stat['CO2']['adf_statistic']:.4f}\n"
            f"  - P-value: {stat['CO2']['p_value']:.4f}\n"
            f"  - Serie stationnaire: {'Oui' if stat['CO2']['is_stationary'] else 'Non'}\n\n"
            f"Interpretation: p-value < 0.05 indique une serie stationnaire (absence de racine unitaire)."
        )
        self.pdf.add_text(stat_text)
        
        # Corrélation
        self.pdf.ln(5)
        self.pdf.section_title("3. Correlation de Pearson")
        corr = self.stats['correlation']
        self.pdf.add_text(
            f"Coefficient de correlation: {corr:.4f}\n\n"
            f"Interpretation: Une correlation de {corr:.4f} indique une relation "
            f"{'positive' if corr > 0 else 'negative'} {'forte' if abs(corr) > 0.7 else 'moderee' if abs(corr) > 0.3 else 'faible'} "
            f"entre les emissions de CO2 et l'indice Dow Jones."
        )
    
    def _add_heteroscedasticity_tests(self):
        """Ajoute les tests d'hétéroscédasticité"""
        self.pdf.add_page()
        self.pdf.chapter_title("IV. TESTS D'HETEROSCEDASTICITE")
        
        het = self.stats['heteroscedasticity']
        
        # Breusch-Pagan
        self.pdf.section_title("1. Test de Breusch-Pagan")
        bp_text = (
            f"Statistique LM: {het['breusch_pagan']['lm_statistic']:.4f}\n"
            f"P-value (LM): {het['breusch_pagan']['lm_p_value']:.4e}\n"
            f"Statistique F: {het['breusch_pagan']['f_statistic']:.4f}\n"
            f"P-value (F): {het['breusch_pagan']['f_p_value']:.4e}\n\n"
            f"Conclusion: {'Presence' if het['breusch_pagan']['has_heteroscedasticity'] else 'Absence'} "
            f"d'heteroscedasticite (seuil 5%)"
        )
        self.pdf.add_text(bp_text)
        
        # White
        self.pdf.ln(5)
        self.pdf.section_title("2. Test de White")
        white_text = (
            f"Statistique LM: {het['white']['lm_statistic']:.4f}\n"
            f"P-value (LM): {het['white']['lm_p_value']:.4e}\n"
            f"Statistique F: {het['white']['f_statistic']:.4f}\n"
            f"P-value (F): {het['white']['f_p_value']:.4e}\n\n"
            f"Conclusion: {'Presence' if het['white']['has_heteroscedasticity'] else 'Absence'} "
            f"d'heteroscedasticite (seuil 5%)"
        )
        self.pdf.add_text(white_text)
        
        # Conclusion générale
        self.pdf.ln(5)
        self.pdf.section_title("3. Conclusion generale")
        if het['has_heteroscedasticity']:
            self.pdf.add_text(
                "Les tests revelent la presence d'heteroscedasticite dans les residus du modele. "
                "Cela indique que la variance des erreurs n'est pas constante. Une regression "
                "ponderee (WLS) sera appliquee pour corriger ce probleme."
            )
        else:
            self.pdf.add_text(
                "Les tests ne revelent pas d'heteroscedasticite significative dans les residus. "
                "L'hypothese d'homoscedasticite est respectee."
            )
    
    def _add_autocorrelation_tests(self):
        """Ajoute les tests d'autocorrélation"""
        self.pdf.add_page()
        self.pdf.chapter_title("V. TESTS D'AUTOCORRELATION")
        
        auto = self.stats['autocorrelation']
        
        # Durbin-Watson
        self.pdf.section_title("1. Test de Durbin-Watson")
        dw_text = (
            f"Statistique de Durbin-Watson: {auto['durbin_watson']['statistic']:.4f}\n\n"
            f"Interpretation:\n"
            f"  - Valeur proche de 2: absence d'autocorrelation\n"
            f"  - Valeur < 1.5: autocorrelation positive\n"
            f"  - Valeur > 2.5: autocorrelation negative\n\n"
            f"Conclusion: {'Presence' if auto['durbin_watson']['has_autocorrelation'] else 'Absence'} "
            f"d'autocorrelation"
        )
        self.pdf.add_text(dw_text)
        
        # Breusch-Godfrey
        self.pdf.ln(5)
        self.pdf.section_title("2. Test de Breusch-Godfrey")
        bg_text = (
            f"Statistique LM: {auto['breusch_godfrey']['lm_statistic']:.4f}\n"
            f"P-value (LM): {auto['breusch_godfrey']['lm_p_value']:.4e}\n"
            f"Statistique F: {auto['breusch_godfrey']['f_statistic']:.4f}\n"
            f"P-value (F): {auto['breusch_godfrey']['f_p_value']:.4e}\n\n"
            f"Conclusion: {'Presence' if auto['breusch_godfrey']['has_autocorrelation'] else 'Absence'} "
            f"d'autocorrelation (seuil 5%)"
        )
        self.pdf.add_text(bg_text)
        
        # Conclusion
        self.pdf.ln(5)
        self.pdf.section_title("3. Interpretation")
        if auto['has_autocorrelation']:
            self.pdf.add_text(
                "Les tests revelent la presence d'autocorrelation dans les residus. Cela suggere "
                "que les erreurs successives sont correlees, violant l'hypothese d'independance "
                "des residus. Des modeles de series temporelles plus sophistiques pourraient etre "
                "necessaires."
            )
        else:
            self.pdf.add_text(
                "Les tests ne revelent pas d'autocorrelation significative. L'hypothese "
                "d'independance des residus est respectee."
            )
    
    def _add_regression_results(self):
        """Ajoute les résultats de régression"""
        self.pdf.add_page()
        self.pdf.chapter_title("VI. REGRESSION LINEAIRE")
        
        ols_model = self.models['ols']
        
        # Résultats OLS
        self.pdf.section_title("1. Regression OLS (Moindres Carres Ordinaires)")
        
        const = ols_model.params[0]
        beta = ols_model.params[1]
        
        ols_text = (
            f"Equation de regression:\n"
            f"DJI_Close = {const:.2f} + {beta:.2f} * CO2_Level + epsilon\n\n"
            f"Resultats:\n"
            f"  - Coefficient (beta): {beta:.4f}\n"
            f"  - P-value du coefficient: {ols_model.pvalues[1]:.4e}\n"
            f"  - R-carre: {ols_model.rsquared:.4f}\n"
            f"  - R-carre ajuste: {ols_model.rsquared_adj:.4f}\n"
            f"  - F-statistique: {ols_model.fvalue:.2f}\n"
            f"  - P-value (F): {ols_model.f_pvalue:.4e}\n\n"
            f"Interpretation:\n"
            f"  - Le coefficient {beta:.2f} indique qu'une augmentation de 1 ppm de CO2 "
            f"est associee a une variation de {beta:.2f} points de l'indice Dow Jones.\n"
            f"  - Le R² de {ols_model.rsquared:.4f} signifie que {ols_model.rsquared*100:.2f}% "
            f"de la variance du Dow Jones est expliquee par les emissions de CO2."
        )
        self.pdf.add_text(ols_text)
        
        # WLS si disponible
        if 'wls' in self.models:
            self.pdf.ln(5)
            self.pdf.section_title("2. Regression WLS (Moindres Carres Ponderes)")
            
            wls_model = self.models['wls']
            const_wls = wls_model.params[0]
            beta_wls = wls_model.params[1]
            
            wls_text = (
                f"Suite a la detection d'heteroscedasticite, une regression WLS a ete effectuee.\n\n"
                f"Equation de regression WLS:\n"
                f"DJI_Close = {const_wls:.2f} + {beta_wls:.2f} * CO2_Level + epsilon\n\n"
                f"Resultats:\n"
                f"  - Coefficient (beta): {beta_wls:.4f}\n"
                f"  - P-value du coefficient: {wls_model.pvalues[1]:.4e}\n"
                f"  - R-carre: {wls_model.rsquared:.4f}\n\n"
                f"Amelioration: Le modele WLS corrige l'heteroscedasticite et fournit des "
                f"estimateurs plus robustes."
            )
            self.pdf.add_text(wls_text)
    
    def _add_visualizations(self):
        """Ajoute les visualisations"""
        self.pdf.add_page()
        self.pdf.chapter_title("VII. VISUALISATIONS")
        
        # Evolution temporelle
        self.pdf.section_title("1. Evolution temporelle des variables")
        self.pdf.add_text(
            "Le graphique suivant presente l'evolution du Dow Jones et des emissions de CO2 "
            "sur la periode etudiee."
        )
        self.pdf.ln(3)
        
        try:
            self.pdf.image('output/evolution_temporelle.png', x=10, w=190)
        except:
            logger.warning("Image evolution_temporelle.png non trouvée")
        
        # Régression
        self.pdf.add_page()
        self.pdf.section_title("2. Diagramme de regression")
        self.pdf.add_text(
            "Le nuage de points avec la droite de regression illustre la relation entre "
            "les deux variables."
        )
        self.pdf.ln(3)
        
        try:
            self.pdf.image('output/regression_plot.png', x=10, w=190)
        except:
            logger.warning("Image regression_plot.png non trouvée")
        
        # Résidus
        self.pdf.add_page()
        self.pdf.section_title("3. Analyse des residus")
        self.pdf.add_text(
            "L'analyse des residus permet de verifier les hypotheses du modele de regression."
        )
        self.pdf.ln(3)
        
        try:
            self.pdf.image('output/residuals_analysis.png', x=10, w=190)
        except:
            logger.warning("Image residuals_analysis.png non trouvée")
    
    def _add_conclusion(self):
        """Ajoute la conclusion"""
        self.pdf.add_page()
        self.pdf.chapter_title("CONCLUSION")
        
        ols_model = self.models['ols']
        corr = self.stats['correlation']
        
        conclusion_text = (
            f"Cette etude avait pour objectif d'analyser l'impact des emissions de CO2 sur "
            f"la performance du Dow Jones Industrial Average.\n\n"
            f"Les principaux resultats sont les suivants:\n\n"
            f"1. CORRELATION: Une correlation de {corr:.4f} a ete observee entre les emissions "
            f"de CO2 et l'indice Dow Jones, indiquant une relation "
            f"{'positive' if corr > 0 else 'negative'} entre ces variables.\n\n"
            f"2. POUVOIR EXPLICATIF: Le modele de regression montre que {ols_model.rsquared*100:.2f}% "
            f"de la variance du Dow Jones est expliquee par les emissions de CO2. Cela suggere "
            f"que d'autres facteurs economiques, politiques et financiers jouent egalement un "
            f"role important.\n\n"
            f"3. SIGNIFICATIVITE STATISTIQUE: Le coefficient de regression est statistiquement "
            f"{'significatif' if ols_model.pvalues[1] < 0.05 else 'non significatif'} au seuil de 5%, "
            f"avec une p-value de {ols_model.pvalues[1]:.4e}.\n\n"
            f"4. PROBLEMES DETECTES: "
        )
        
        issues = []
        if self.stats['heteroscedasticity']['has_heteroscedasticity']:
            issues.append("heteroscedasticite")
        if self.stats['autocorrelation']['has_autocorrelation']:
            issues.append("autocorrelation")
        
        if issues:
            conclusion_text += f"La presence de {' et '.join(issues)} a ete detectee, "
            conclusion_text += "ce qui a necessite l'application de corrections.\n\n"
        else:
            conclusion_text += "Aucun probleme majeur n'a ete detecte dans les residus.\n\n"
        
        conclusion_text += (
            f"PERSPECTIVES:\n"
            f"- Integrer d'autres variables explicatives (politiques monetaires, crises "
            f"economiques, innovations technologiques)\n"
            f"- Utiliser des modeles de series temporelles plus sophistiques (ARIMA, VAR)\n"
            f"- Analyser les effets de causalite avec des tests de Granger\n"
            f"- Etudier les effets de seuil et non-linearites potentielles"
        )
        
        self.pdf.add_text(conclusion_text)
    
    def _add_bibliography(self):
        """Ajoute la bibliographie"""
        self.pdf.add_page()
        self.pdf.chapter_title("BIBLIOGRAPHIE")
        
        biblio = [
            "Yahoo Finance API - Donnees financieres du Dow Jones",
            "Global Warming API - Donnees atmospheriques de CO2",
            "Wooldridge, J. M. (2015). Introductory Econometrics: A Modern Approach",
            "Greene, W. H. (2018). Econometric Analysis",
            "Hamilton, J. D. (1994). Time Series Analysis",
            "Statsmodels Documentation - Python Statistical Library"
        ]
        
        self.pdf.set_font('Arial', '', 10)
        for i, ref in enumerate(biblio, 1):
            self.pdf.multi_cell(0, 6, f"[{i}] {ref}")
            self.pdf.ln(2)
    
    def generate_full_report(self, filepath: str = "output/Rapport_Econometrique_Complet.pdf"):
        """
        Génère le rapport PDF complet
        
        Args:
            filepath (str): Chemin de sauvegarde du PDF
        """
        logger.info("  📄 Génération du rapport PDF...")
        
        try:
            # Ajouter toutes les sections
            self._add_cover_page()
            self._add_introduction()
            self._add_data_collection()
            self._add_descriptive_stats()
            self._add_statistical_tests()
            self._add_heteroscedasticity_tests()
            self._add_autocorrelation_tests()
            self._add_regression_results()
            self._add_visualizations()
            self._add_conclusion()
            self._add_bibliography()
            
            # Sauvegarder
            self.pdf.output(filepath)
            logger.info(f"     ✓ Rapport sauvegarde: {filepath}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la generation du rapport: {str(e)}")
            raise
