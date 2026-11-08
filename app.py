import streamlit as st
import random
import json
import time

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Examen Civique France - Naturalisation",
    page_icon="🇫🇷",
    layout="centered"
)

# ==========================================
# 2. STYLE CSS PERSONNALISÉ (THÈME RÉPUBLIQUE FRANÇAISE)
# ==========================================
custom_css = """
<style>
    /* Cacher les éléments par défaut de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Bannière supérieure tricolore */
    .tricolore-bar {
        height: 8px;
        width: 100%;
        background: linear-gradient(90deg, #002395 0%, #002395 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #ED2939 66.6%, #ED2939 100%);
        border-radius: 4px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
        margin-bottom: 1.2rem;
    }

    /* En-tête officiel avec drapeau */
    .rep-header {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 35, 149, 0.06);
    }
    .rep-motto {
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #475569;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }
    .rep-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0.2rem 0;
    }
    .rep-subtitle {
        font-size: 0.98rem;
        color: #334155;
        font-weight: 500;
        margin-top: 0.2rem;
    }

    /* Cartes de sélection de mode */
    .mode-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 5px solid #002395;
        border-radius: 14px;
        padding: 1.4rem;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 0.8rem;
    }
    .mode-card.exam-real {
        border-top: 5px solid #ED2939;
    }
    .mode-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.09);
    }
    .mode-badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .badge-blue {
        background-color: #dbeafe;
        color: #1e40af;
    }
    .badge-red {
        background-color: #fee2e2;
        color: #991b1b;
    }

    /* Carte de question */
    .question-box {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 6px solid #002395;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .question-box.situation {
        border-left: 6px solid #ED2939;
    }
    .q-category {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.45rem;
    }
    .q-text {
        font-size: 1.18rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.45;
    }

    /* Badges de statut (Chrono & Progression) */
    .status-pill {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 0.55rem 0.9rem;
        font-weight: 700;
        font-size: 0.95rem;
        color: #1e293b;
        text-align: center;
    }
    .timer-ok {
        background: #eff6ff;
        border-color: #93c5fd;
        color: #1e3a8a;
    }
    .timer-warn {
        background: #fef3c7;
        border-color: #fcd34d;
        color: #92400e;
    }
    .timer-danger {
        background: #fee2e2;
        border-color: #fca5a5;
        color: #991b1b;
    }

    /* Amélioration visuelle des boutons radio dans les formulaires */
    div[role="radiogroup"] > label {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.15s ease-in-out;
        width: 100%;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #eff6ff;
        border-color: #3b82f6;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# 3. CONSTANTES & CHARGEMENT DES DONNÉES
# ==========================================
TEMPS_MAX_SECONDES = 45 * 60  # 45 minutes
SCORE_REQUIS = 32             # 32 / 40 (80 %)


@st.cache_data
def load_questions(file):
    """Charge les questions depuis un fichier JSON."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            q_type = "situation" if "situation" in file else "connaissance"
            for item in data:
                item["type"] = q_type
            return data
    except FileNotFoundError:
        st.error(f"Attention : Le fichier {file} est introuvable.")
        return []


questions_connaissance = load_questions("questions_connaissance.json")
questions_situation = load_questions("questions_situation.json")


# ==========================================
# 4. INITIALISATION DE LA SESSION
# ==========================================
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.questions = []
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.errors = []
    st.session_state.start_time = 0


# ==========================================
# 5. EN-TÊTE VISUEL (DRAPEAU FRANÇAIS SVG)
# ==========================================
header_html = """
<div class="tricolore-bar"></div>
<div class="rep-header">
    <svg width="72" height="48" viewBox="0 0 3 2" style="border-radius: 6px; box-shadow: 0 3px 8px rgba(0,0,0,0.18);">
        <rect width="1" height="2" x="0" fill="#002395"/>
        <rect width="1" height="2" x="1" fill="#FFFFFF"/>
        <rect width="1" height="2" x="2" fill="#ED2939"/>
    </svg>
    <div class="rep-motto">Liberté • Égalité • Fraternité</div>
    <div class="rep-title">Simulateur de l'Examen Civique</div>
    <div class="rep-subtitle">Préparation officielle au QCM de <b>Naturalisation Française</b></div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)


# ==========================================
# 6. ÉCRAN 1 : SÉLECTION DU MODE
# ==========================================
if not st.session_state.started:
    # Bandeau d'informations clés sur l'examen
    info_col1, info_col2, info_col3 = st.columns(3)
    info_col1.metric("📋 Questions", "40 QCM", "1 seule bonne réponse")
    info_col2.metric("⏱️ Durée maximale", "45 min", "Chronométré")
    info_col3.metric("🎯 Seuil de réussite", "32 / 40", "80 % minimum")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown(f"""
        <div class="mode-card">
            <span class="mode-badge badge-blue">📚 Révision Thématique</span>
            <h3 style="margin: 0.2rem 0 0.5rem 0; color: #0f172a;">Mode Entraînement</h3>
            <p style="color: #475569; font-size: 0.92rem; margin-bottom: 0.8rem;">
                Testez vos connaissances sur l'histoire, la géographie, la laïcité, les institutions et les valeurs de la République.
            </p>
            <ul style="color: #334155; font-size: 0.88rem; padding-left: 1.2rem; margin-bottom: 0;">
                <li><b>40 questions</b> de connaissances</li>
                <li>Tirage aléatoire parmi <b>{len(questions_connaissance)} questions</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Lancer l'entraînement", use_container_width=True, type="primary"):
            q_choisies = random.sample(questions_connaissance, min(40, len(questions_connaissance)))
            st.session_state.questions = q_choisies
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card exam-real">
            <span class="mode-badge badge-red">🏛️ Conditions Officielles</span>
            <h3 style="margin: 0.2rem 0 0.5rem 0; color: #0f172a;">Mode Examen Réel</h3>
            <p style="color: #475569; font-size: 0.92rem; margin-bottom: 0.8rem;">
                Simulation fidèle à l'épreuve officielle mêlant questions théoriques et cas pratiques de la vie quotidienne.
            </p>
            <ul style="color: #334155; font-size: 0.88rem; padding-left: 1.2rem; margin-bottom: 0;">
                <li><b>28 questions</b> de connaissances</li>
                <li><b>12 questions</b> de mises en situation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎓 Lancer l'examen réel", use_container_width=True, type="primary"):
            q_con = random.sample(questions_connaissance, min(28, len(questions_connaissance)))
            q_sit = random.sample(questions_situation, min(12, len(questions_situation)))
            q_choisies = q_con + q_sit
            random.shuffle(q_choisies)

            st.session_state.questions = q_choisies
            st.session_state.start_time = time.time()
            st.session_state.started = True
            st.rerun()


# ==========================================
# 7. ÉCRAN 2 : EXAMEN EN COURS OU RÉSULTATS
# ==========================================
else:
    temps_ecoule = time.time() - st.session_state.start_time
    temps_restant = max(0, TEMPS_MAX_SECONDES - temps_ecoule)

    minutes = int(temps_restant // 60)
    secondes = int(temps_restant % 60)

    total_q = len(st.session_state.questions)

    # ---------------------------------------------------------
    # A. ÉCRAN DE FIN D'EXAMEN (RÉSULTATS)
    # ---------------------------------------------------------
    if st.session_state.index >= total_q or temps_restant <= 0:
        duree_totale = int(min(temps_ecoule, TEMPS_MAX_SECONDES))
        min_passees = duree_totale // 60
        sec_passees = duree_totale % 60

        score40 = int((st.session_state.score / total_q) * 40) if total_q > 0 else 0
        pourcentage = int((st.session_state.score / total_q) * 100) if total_q > 0 else 0
        reussi = score40 >= SCORE_REQUIS

        if temps_restant <= 0 and st.session_state.index < total_q:
            st.warning("⏰ **Le temps réglementaire de 45 minutes est écoulé !**")

        if reussi:
            st.balloons()
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 2px solid #10b981; border-radius: 14px; padding: 1.5rem; text-align: center; margin-bottom: 1.2rem;">
                <h2 style="color: #065f46; margin: 0;">🎉 Félicitations ! Examen Réussi</h2>
                <p style="color: #047857; font-size: 1.05rem; margin-top: 0.4rem;">
                    Vous avez atteint ou dépassé le seuil officiel de 32/40 requis pour la naturalisation.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 2px solid #ef4444; border-radius: 14px; padding: 1.5rem; text-align: center; margin-bottom: 1.2rem;">
                <h2 style="color: #991b1b; margin: 0;">❌ Résultat insuffisant</h2>
                <p style="color: #b91c1c; font-size: 1.05rem; margin-top: 0.4rem;">
                    Il vous faut un minimum de <b>{SCORE_REQUIS}/40 (80 %)</b> pour valider l'examen officiel. Continuez à vous entraîner !
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Tableau de bord des métriques
        m1, m2, m3 = st.columns(3)
        m1.metric("🏆 Note finale", f"{score40} / 40", f"{pourcentage} % de réussite")
        m2.metric("✅ Bonnes réponses", f"{st.session_state.score} / {total_q}", f"{len(st.session_state.errors)} erreur(s)")
        m3.metric("⏱️ Temps utilisé", f"{min_passees:02d}m {sec_passees:02d}s", "sur 45m 00s")

        st.markdown("---")
        st.subheader("📋 Bilan détaillé de vos erreurs")

        if not st.session_state.errors:
            st.success("🌟 **Sans-faute absolu !** Vous maîtrisez parfaitement toutes les questions de cette session.")
        else:
            for i, err in enumerate(st.session_state.errors):
                with st.expander(f"❌ Erreur n°{i+1} — {err['question'][:65]}..."):
                    st.markdown(f"**Question :** {err['question']}")
                    st.markdown(f"🔴 **Votre réponse :** `{err['choisie']}`")
                    st.markdown(f"🟢 **Bonne réponse :** `{err['correcte']}`")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Recommencer une nouvelle session", use_container_width=True, type="primary"):
            st.session_state.clear()
            st.rerun()

        st.stop()

    # ---------------------------------------------------------
    # B. ÉCRAN DE QUESTION EN COURS
    # ---------------------------------------------------------
    if temps_restant > 10 * 60:
        timer_class = "timer-ok"
    elif temps_restant > 3 * 60:
        timer_class = "timer-warn"
    else:
        timer_class = "timer-danger"

    top_col1, top_col2, top_col3 = st.columns([2, 2, 1])
    with top_col1:
        st.markdown(
            f'<div class="status-pill">📍 Question {st.session_state.index + 1} sur {total_q}</div>',
            unsafe_allow_html=True
        )
    with top_col2:
        st.markdown(
            f'<div class="status-pill {timer_class}">⏱️ {minutes:02d}:{secondes:02d}</div>',
            unsafe_allow_html=True
        )
    with top_col3:
        if st.button("✖ Quitter", use_container_width=True, help="Abandonner la session en cours"):
            st.session_state.clear()
            st.rerun()

    # Barre de progression
    progression = st.session_state.index / total_q
    st.progress(progression)

    # Récupération de la question actuelle
    q = st.session_state.questions[st.session_state.index]
    is_situation = q.get("type") == "situation"

    box_class = "question-box situation" if is_situation else "question-box"
    cat_label = "🎭 Mise en situation pratique" if is_situation else "📚 Connaissance générale"
    cat_color = "#b91c1c" if is_situation else "#1e40af"

    # Affichage de la carte de question
    st.markdown(f"""
    <div class="{box_class}">
        <div class="q-category" style="color: {cat_color};">{cat_label}</div>
        <div class="q-text">{q["question"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # Mélange unique des options pour la question en cours
    if "shuffled_options" not in st.session_state:
        st.session_state.shuffled_options = q["options"].copy()
        random.shuffle(st.session_state.shuffled_options)

    with st.form(key=f"form_question_{st.session_state.index}"):
        choice = st.radio(
            "Sélectionnez votre réponse :",
            st.session_state.shuffled_options,
            index=None
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(
            label="Valider et passer à la suivante ➡️",
            use_container_width=True,
            type="primary"
        )

        if submit_button:
            if choice is None:
                st.warning("⚠️ Veuillez sélectionner une proposition avant de valider.")
            else:
                if choice == q["reponse"]:
                    st.session_state.score += 1
                else:
                    st.session_state.errors.append({
                        "question": q["question"],
                        "choisie": choice,
                        "correcte": q["reponse"]
                    })

                st.session_state.index += 1
                del st.session_state.shuffled_options
                st.rerun()
