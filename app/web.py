import json
from datetime import datetime
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
NOTES_FILE = DATA_DIR / "notes.json"

DATA_DIR.mkdir(exist_ok=True)


def load_notes():
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    return []


def save_notes(notes):
    NOTES_FILE.write_text(
        json.dumps(notes, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


st.set_page_config(
    page_title="Bible Study OS",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Bible Study OS")
st.write("Lire → Comprendre → Mediter → Voir Jesus → Appliquer → Progresser")

menu = st.sidebar.radio(
    "Menu",
    [
        "Accueil",
        "Creer une etude",
        "Mes etudes",
        "Analyse spirituelle",
        "Jardin spirituel",
        "YouTube"
    ]
)

notes = load_notes()

if menu == "Accueil":
    st.header("Bienvenue dans Bible Study OS")
    st.write("""
    Bible Study OS est une plateforme d'etude biblique.

    Objectif :
    - Identifier les mauvaises herbes spirituelles
    - Cultiver les bandes florales spirituelles
    - Garder Jesus au centre de chaque analyse
    - Transformer les etudes en contenu YouTube
    """)

elif menu == "Creer une etude":
    st.header("Creer une nouvelle etude biblique")

    with st.form("study_form"):
        sujet = st.text_input("Sujet")
        situation = st.text_area("Situation ou question")
        verset = st.text_input("Verset principal")
        note = st.text_area("Note personnelle")
        mauvaise_herbe = st.text_input("Mauvaise herbe spirituelle")
        bande_florale = st.text_input("Bande florale spirituelle")
        jesus = st.text_area("Ou est Jesus dans cette etude ?")

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            study = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "sujet": sujet,
                "situation": situation,
                "verset": verset,
                "note": note,
                "mauvaise_herbe": mauvaise_herbe,
                "bande_florale": bande_florale,
                "jesus": jesus
            }

            notes.append(study)
            save_notes(notes)

            st.success("Etude enregistree avec succes.")
            st.info("Rappel : prends une photo de ton carnet papier.")

elif menu == "Mes etudes":
    st.header("Mes etudes bibliques")

    if not notes:
        st.warning("Aucune etude enregistree.")
    else:
        for index, study in enumerate(notes, start=1):
            with st.expander(f"{index}. {study.get('sujet', 'Sans sujet')}"):
                st.write(f"**Date :** {study.get('date', '')}")
                st.write(f"**Situation :** {study.get('situation', '')}")
                st.write(f"**Verset :** {study.get('verset', '')}")
                st.write(f"**Note :** {study.get('note', '')}")
                st.write(f"**Mauvaise herbe :** {study.get('mauvaise_herbe', '')}")
                st.write(f"**Bande florale :** {study.get('bande_florale', '')}")
                st.write(f"**Jesus :** {study.get('jesus', '')}")

elif menu == "Analyse spirituelle":
    st.header("Analyse spirituelle")

    if not notes:
        st.warning("Aucune etude disponible.")
    else:
        study = notes[-1]

        st.subheader(study.get("sujet", "Derniere etude"))
        st.write(f"**Verset :** {study.get('verset', '')}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Mauvaise herbe")
            st.write(study.get("mauvaise_herbe", ""))
            st.write("Cycle mauvais : mauvaise pensee → mauvais choix → consequence → eloignement spirituel")

        with col2:
            st.markdown("### Bande florale")
            st.write(study.get("bande_florale", ""))
            st.write("Cycle divin : Parole de Dieu → meditation → priere → paix → croissance")

        st.markdown("### Jesus au centre")
        st.write(study.get("jesus", ""))

elif menu == "Jardin spirituel":
    st.header("Jardin spirituel")

    if not notes:
        st.warning("Aucune etude disponible.")
    else:
        st.metric("Nombre total d'etudes", len(notes))

        mauvaises_herbes = {}
        bandes_florales = {}

        for study in notes:
            weed = study.get("mauvaise_herbe", "").strip()
            flower = study.get("bande_florale", "").strip()

            if weed:
                mauvaises_herbes[weed] = mauvaises_herbes.get(weed, 0) + 1

            if flower:
                bandes_florales[flower] = bandes_florales.get(flower, 0) + 1

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Mauvaises herbes")
            for weed, count in mauvaises_herbes.items():
                st.write(f"- {weed} : {count} fois")

        with col2:
            st.subheader("Bandes florales")
            for flower, count in bandes_florales.items():
                st.write(f"- {flower} : {count} fois")

elif menu == "YouTube":
    st.header("YouTube Studio")

    if not notes:
        st.warning("Aucune etude disponible.")
    else:
        study = notes[-1]

        script = f"""
# Script YouTube

## Titre
Quelle mauvaise herbe spirituelle bloque ma croissance ? - {study.get('sujet', '')}

## Introduction
Aujourd'hui, on parle de : {study.get('sujet', '')}.

## Situation
{study.get('situation', '')}

## Verset principal
{study.get('verset', '')}

## Mauvaise herbe
{study.get('mauvaise_herbe', '')}

## Bande florale
{study.get('bande_florale', '')}

## Jesus au centre
{study.get('jesus', '')}

## Application
Quelle action concrete puis-je faire aujourd'hui pour mieux suivre Jesus ?
"""

        st.download_button(
            "Telecharger le script YouTube",
            script,
            file_name="script-youtube.md",
            mime="text/markdown"
        )

        st.text_area("Apercu du script", script, height=500)
