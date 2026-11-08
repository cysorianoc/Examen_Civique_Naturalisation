---
title: Simulateur Examen Civique
emoji: 🎓
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
tags:
  - streamlit
  - education
pinned: false
short_description: Simulateur de l'examen civique (CSP)
---

# 🇫🇷 Simulateur Examen Civique (CSP)

Bienvenue sur le dépôt du **Simulateur de l'Examen Civique Français**. 
Cette application a été conçue pour aider les candidats à préparer l'examen de la formation civique, exigé pour certains titres de séjour et l'accès à la nationalité.

## 🌟 Fonctionnalités

- **Deux modes d'entraînement :**
  - *Mode Entraînement :* 40 questions de connaissances générales sur la France.
  - *Mode Examen Réel :* Un tirage aléatoire fidèle à l'examen officiel (28 questions de connaissances + 12 questions de mises en situation).
- **Conditions d'examen :** Chronomètre strict de 45 minutes intégré.
- **Notation officielle :** Seuil de réussite fixé à 32 bonnes réponses sur 40 (80%).
- **Correction détaillée :** Affichage de vos erreurs et des bonnes réponses à la fin du test pour vous aider à progresser.

## 🛠️ Structure du projet

- `app.py` : Le cœur de l'application Streamlit.
- `questions_connaissance.json` : La base de données des questions théoriques (Histoire, géographie, institutions, valeurs).
- `questions_situation.json` : La base de données des questions pratiques (cas concrets de la vie quotidienne).
- `Dockerfile` & `requirements.txt` : Les fichiers de configuration pour faire tourner l'application.

## 🚀 Comment s'entraîner ?

L'application est déployée et prête à l'emploi. Il vous suffit de cliquer sur l'onglet **App** en haut de cette page pour lancer le chronomètre et tester vos connaissances. Bonne révision !