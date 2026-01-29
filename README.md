# 📊 Analyse Économétrique: Impact du CO2 sur le Dow Jones

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Projet d'analyse économétrique étudiant la relation entre les émissions de CO2 atmosphériques et la performance du Dow Jones Industrial Average.

## 🎯 Objectif

Ce projet analyse l'impact du changement climatique, mesuré par les émissions de CO2, sur la performance du marché boursier américain (Dow Jones). Il utilise des techniques économétriques avancées pour identifier et quantifier cette relation.

## 📁 Structure du Projet

```
econometric_analysis/
│
├── src/                          # Code source
│   ├── main.py                   # Point d'entrée principal
│   ├── data_collector.py         # Module de collecte de données
│   ├── statistical_analysis.py   # Module d'analyse statistique
│   ├── visualizations.py         # Module de visualisation
│   └── report_generator.py       # Module de génération de rapport PDF
│
├── data/                         # Données collectées (généré)
│   └── dow_jones_co2_data.csv
│
├── output/                       # Résultats de l'analyse (généré)
│   ├── evolution_temporelle.png
│   ├── regression_plot.png
│   ├── residuals_analysis.png
│   ├── Rapport_Econometrique_Complet.pdf
│   └── analysis.log
│
├── tests/                        # Tests unitaires
│
├── docs/                         # Documentation
│
├── requirements.txt              # Dépendances Python
└── README.md                     # Ce fichier
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**

```bash
git clone https://github.com/votre-username/econometric_analysis.git
cd econometric_analysis
```

2. **Créer un environnement virtuel (recommandé)**

```bash
python -m venv venv

# Sur Windows
venv\Scripts\activate

# Sur macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Lancement de l'analyse complète

```bash
cd src
python main.py
```

Le programme va :
1. 📥 Collecter les données du Dow Jones et du CO2
2. 📊 Calculer les statistiques descriptives
3. 🔬 Effectuer tous les tests économétriques
4. 📈 Générer les visualisations
5. 📄 Créer un rapport PDF complet

### Utilisation modulaire

Vous pouvez également utiliser les modules individuellement :

```python
from data_collector import DataCollector
from statistical_analysis import StatisticalAnalyzer
from visualizations import Visualizer

# Collecter les données
collector = DataCollector(start_date="2015-01-01")
data = collector.collect_all_data()

# Analyser
analyzer = StatisticalAnalyzer(data)
stats = analyzer.compute_descriptive_stats()
model = analyzer.run_ols_regression()

# Visualiser
viz = Visualizer(data, model)
viz.plot_regression()
```

## 📊 Méthodologie

### 1. Collecte des Données

- **Dow Jones**: Données quotidiennes depuis Yahoo Finance (API `yfinance`)
- **CO2**: Mesures atmosphériques depuis Global Warming API
- **Période**: 2015 - présent

### 2. Analyses Statistiques

#### Tests Effectués

- ✅ **Statistiques descriptives** (moyenne, écart-type, variance, quartiles)
- ✅ **Test de normalité** (Shapiro-Wilk)
- ✅ **Test de stationnarité** (Augmented Dickey-Fuller)
- ✅ **Corrélation de Pearson**
- ✅ **Régression linéaire simple** (OLS)
- ✅ **Tests d'hétéroscédasticité** (Breusch-Pagan, White)
- ✅ **Tests d'autocorrélation** (Durbin-Watson, Breusch-Godfrey)
- ✅ **Régression robuste** (WLS si nécessaire)

#### Modèle Économétrique

```
DJI_Close = α + β × CO2_Level + ε
```

Où :
- `DJI_Close` = Indice de clôture du Dow Jones
- `CO2_Level` = Niveau de CO2 atmosphérique (ppm)
- `α` = Constante
- `β` = Coefficient de régression
- `ε` = Terme d'erreur

### 3. Visualisations

Le projet génère plusieurs graphiques :

1. **Évolution temporelle** : Tendances du DJI et CO2
2. **Régression linéaire** : Nuage de points avec droite de régression
3. **Analyse des résidus** : Diagnostic du modèle (4 graphiques)

### 4. Rapport PDF

Un rapport complet au format PDF est généré automatiquement, incluant :

- 📋 Introduction et problématique
- 📊 Statistiques descriptives détaillées
- 🔬 Résultats de tous les tests
- 📈 Visualisations
- 📝 Interprétation et conclusion
- 📚 Bibliographie

## 📈 Résultats Attendus

Le projet permet de :

- Quantifier la relation entre CO2 et Dow Jones
- Déterminer la significativité statistique de cette relation
- Identifier les problèmes économétriques (hétéroscédasticité, autocorrélation)
- Produire un rapport professionnel pour présentation académique ou professionnelle

## 🛠️ Technologies Utilisées

| Technologie | Usage |
|-------------|-------|
| **pandas** | Manipulation de données |
| **yfinance** | Collecte données financières |
| **statsmodels** | Analyses économétriques |
| **matplotlib/seaborn** | Visualisations |
| **scipy** | Tests statistiques |
| **FPDF** | Génération de rapports PDF |

## 📝 Logs et Débogage

Les logs sont enregistrés dans `output/analysis.log` et affichés dans la console :

```
2025-01-27 10:30:15 - INFO - DÉBUT DE L'ANALYSE ÉCONOMÉTRIQUE
2025-01-27 10:30:16 - INFO - 📊 ÉTAPE 1: COLLECTE DES DONNÉES
2025-01-27 10:30:20 - INFO - ✅ 2847 observations collectées
...
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**ABDELLAOUI FEDI**

- GitHub: (https://github.com/fediabdellaoui311-glitch)
- Email: fediabdellaoui311@gmail.com



## 📚 Références

- Wooldridge, J. M. (2015). *Introductory Econometrics: A Modern Approach*
- Greene, W. H. (2018). *Econometric Analysis*
- Hamilton, J. D. (1994). *Time Series Analysis*

---

⭐️ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile sur GitHub !
