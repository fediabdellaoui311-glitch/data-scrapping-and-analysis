# 🚀 Guide de Démarrage Rapide

## Installation en 3 étapes

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/econometric_analysis.git
cd econometric_analysis
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'analyse
```bash
cd src
python main.py
```

## ✅ Vérification de l'installation

Pour vérifier que tout fonctionne :

```bash
python -c "import pandas, yfinance, statsmodels, matplotlib, seaborn, fpdf; print('✅ Toutes les dépendances sont installées !')"
```

## 📊 Résultats

Après l'exécution, vous trouverez :

### Dans `data/`
- `dow_jones_co2_data.csv` - Dataset complet

### Dans `output/`
- `evolution_temporelle.png` - Graphique d'évolution
- `regression_plot.png` - Régression linéaire
- `residuals_analysis.png` - Analyse des résidus
- `Rapport_Econometrique_Complet.pdf` - **Rapport final**
- `analysis.log` - Journal d'exécution

## 🎯 Personnalisation

### Changer la période d'analyse

Dans `src/main.py`, ligne 107 :
```python
analysis = EconometricAnalysis(start_date="2015-01-01")  # Modifier ici
```

### Analyser d'autres indices

Dans `src/data_collector.py`, ligne 30 :
```python
df = yf.download("^DJI", ...)  # Remplacer par ^GSPC (S&P 500), ^IXIC (NASDAQ), etc.
```

## 🧪 Lancer les tests

```bash
cd tests
python test_analysis.py
```

## 🆘 Problèmes courants

### Erreur d'installation de `yfinance`
```bash
pip install --upgrade yfinance
```

### Erreur avec `fpdf`
```bash
pip install fpdf
```

### Timeout lors du téléchargement des données
- Vérifiez votre connexion Internet
- Augmentez le timeout dans `data_collector.py`

## 📞 Support

En cas de problème :
1. Consultez les logs dans `output/analysis.log`
2. Vérifiez la section "Issues" sur GitHub
3. Contactez : votre.email@example.com

---

**Temps d'exécution moyen** : 1-2 minutes  
**Python minimum** : 3.8
