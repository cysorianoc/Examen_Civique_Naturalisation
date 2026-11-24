

# Simulateur Examen Civique (Naturalisation)

Bienvenue sur le dépôt du **Simulateur de l'Examen Civique Français — Spécial Naturalisation** 
Cette application a été conçue pour aider les candidats à préparer le QCM officiel de l'examen civique exigé dans le cadre d'une demande de **naturalisation** ou de **réintégration dans la nationalité française**

##  Fonctionnalités

- **Deux modes d'entraînement :**
  - *Mode Entraînement :* 40 questions de connaissances générales couvrant les 5 grandes thématiques officielles (*Principes et valeurs de la République*, *Système institutionnel et politique*, *Droits et devoirs*, *Histoire, géographie et culture*, et *Vivre dans la société française*)
  - *Mode Examen Réel :* Un tirage aléatoire fidèle à l'examen officiel (28 questions de connaissances + 12 questions de mises en situation).
- **Conditions d'examen :** Chronomètre strict de 45 minutes intégré.
- **Notation officielle :** Seuil de réussite fixé à 32 bonnes réponses sur 40 (80 %).
- **Correction détaillée :** Affichage de vos erreurs et des bonnes réponses à la fin du test pour vous aider à progresser.

##  Structure du projet

- `app.py` : Le cœur de l'application Streamlit.
- `questions_connaissance.json` : La base de données complète des questions théoriques officielles pour la naturalisation (258 questions couvrant les valeurs républicaines, la laïcité, les institutions françaises et européennes, les droits/devoirs, l'histoire-géographie et la vie en société).
- `questions_situation.json` : La base de données des questions pratiques (45 cas concrets de mise en situation de la vie quotidienne et citoyenne).
- `Dockerfile` & `requirements.txt` : Les fichiers de configuration pour faire tourner l'application.

##  Comment s'entraîner ?

L'application est déployée et prête à l'emploi. Il vous suffit de cliquer sur l'onglet **App** en haut de cette page pour lancer le chronomètre et tester vos connaissances. Bonne révision !


<div align="center">
 
<h2 style="color: #1E88E5;">
Application deployed on Streamlit
</h2>
 
<p style="font-size: 24px; font-weight: bold;">
Check out the
<a
href="https://examenciviquenaturalisation.streamlit.app/"
target="_blank"
rel="noopener noreferrer"
style="color: #E63946; text-decoration: underline;"
>
Examen Civique Naturalisation application
</a>
</p>
 
<a
href="https://examenciviquenaturalisation.streamlit.app/"
target="_blank"
rel="noopener noreferrer"
>
<img
src="https://raw.githubusercontent.com/cysorianoc/Examen_Civique_Naturalisation/main/app%20interface.jpg"
alt="Examen Civique Naturalisation application interface"
width="800"
/>
</a>
 
</div>
