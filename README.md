# 🕌 Plateforme d'Intelligence Boursière Éthique (BVMT)

Application interactive d'aide à l'investissement sur la **Bourse des Valeurs Mobilières de Tunis (BVMT)** combinant un **Screener Sharia automatisé** et un **moteur de prédiction IA**.

## 🎯 Objectif du projet
Démocratiser l'investissement éthique en Tunisie en offrant aux particuliers un outil transparent permettant de :
1. Filtrer automatiquement les entreprises cotées selon les normes de la finance islamique (**AAOIFI**).
2. Anticiper les tendances de cours à court terme uniquement sur les actifs validés.
3. Calculer automatiquement le montant de purification des dividendes (*Tathir*).

## ✨ Fonctionnalités principales
* **📊 Screener Éthique (AAOIFI) :** Exclusion automatique des secteurs non conformes (banques et assurances conventionnelles) et vérification des ratios financiers (Dette totale < 33 % de la capitalisation boursière).
* **🔮 Prédictions IA & Analyse Technique :** Calcul de la Moyenne Mobile 20 jours (MA20), modélisation prédictive des cours à J+1, génération de signaux d'achat et visualisation graphique SVG interactive.
* **💰 Simulateur & Purification (*Tathir*) :** Estimation des dividendes annuels et calcul au millime près du prorata des revenus impurs (< 5 %) à reverser aux œuvres caritatives.

## 🛠️ Technologies utilisées
* **Langage :** Python 3
* **Manipulation de données :** Pandas, NumPy
* **Interface Web & Visualisation :** Streamlit, SVG / HTML5

## 🚀 Installation et exécution locale

1. Cloner ce dépôt :
   ```bash
   git clone https://github.com
   cd BVMT-Sharia-IA
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancer l'application :
   ```bash
   streamlit run app.py
   ```
