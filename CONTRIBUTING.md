# Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! 🎉

## Comment contribuer

### 1. Fork et Clone

```bash
# Forker le projet sur GitHub, puis :
git clone https://github.com/VOTRE-USERNAME/econometric_analysis.git
cd econometric_analysis
```

### 2. Créer une branche

```bash
git checkout -b feature/ma-nouvelle-fonctionnalite
```

### 3. Faire vos modifications

- Suivez le style de code existant
- Ajoutez des tests si nécessaire
- Documentez votre code avec des docstrings
- Mettez à jour le README si nécessaire

### 4. Tester vos modifications

```bash
# Installer les dépendances de développement
pip install pytest pytest-cov

# Lancer les tests
pytest tests/ -v

# Vérifier la couverture
pytest tests/ --cov=src
```

### 5. Commit et Push

```bash
git add .
git commit -m "feat: description de la fonctionnalité"
git push origin feature/ma-nouvelle-fonctionnalite
```

### 6. Créer une Pull Request

- Allez sur GitHub
- Créez une Pull Request vers la branche `main`
- Décrivez vos modifications en détail

## Standards de Code

### Style Python

- Suivre PEP 8
- Utiliser des noms de variables descriptifs
- Limiter les lignes à 100 caractères
- Ajouter des docstrings pour toutes les fonctions/classes

Exemple :
```python
def calculate_statistics(data: pd.DataFrame) -> Dict:
    """
    Calcule les statistiques descriptives.
    
    Args:
        data (pd.DataFrame): DataFrame avec les données
        
    Returns:
        Dict: Dictionnaire avec les statistiques
    """
    return {
        'mean': data.mean(),
        'std': data.std()
    }
```

### Messages de Commit

Utilisez le format Conventional Commits :

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `test:` Tests
- `refactor:` Refactorisation
- `style:` Formatage

Exemples :
```
feat: ajout du test de Jarque-Bera
fix: correction du calcul de la p-value
docs: mise à jour du README avec exemples
test: ajout de tests pour StatisticalAnalyzer
```

## Types de Contributions Bienvenues

### 🐛 Rapporter des Bugs

Ouvrez une issue avec :
- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs réel
- Version de Python et des dépendances

### ✨ Proposer des Fonctionnalités

Ouvrez une issue pour discuter :
- Pourquoi cette fonctionnalité est utile
- Comment elle devrait fonctionner
- Exemples d'utilisation

### 📝 Améliorer la Documentation

- Corriger les fautes
- Ajouter des exemples
- Clarifier les explications
- Traduire en d'autres langues

### 🧪 Ajouter des Tests

- Tests unitaires pour les fonctions
- Tests d'intégration
- Tests de validation de données

## Idées de Contributions

- [ ] Ajouter d'autres indices boursiers (S&P 500, NASDAQ)
- [ ] Implémenter ARIMA/GARCH pour séries temporelles
- [ ] Ajouter des tests de causalité de Granger
- [ ] Créer un dashboard interactif avec Streamlit/Dash
- [ ] Ajouter l'analyse de co-intégration
- [ ] Implémenter des modèles de machine learning
- [ ] Créer une API REST pour les prédictions
- [ ] Ajouter l'export en Excel
- [ ] Internationalisation (i18n)

## Questions ?

N'hésitez pas à ouvrir une issue pour toute question !

## Code de Conduite

- Soyez respectueux
- Acceptez les critiques constructives
- Focalisez sur ce qui est meilleur pour la communauté

---

Merci pour vos contributions ! 🚀
