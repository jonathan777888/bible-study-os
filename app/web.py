import streamlit as st
from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
YOUTUBE_DIR = BASE_DIR / "youtube" / "scripts"
SCHEMA_DIR = BASE_DIR / "docs" / "schemas"

NOTES_FILE = DATA_DIR / "notes.json"

DATA_DIR.mkdir(exist_ok=True)
YOUTUBE_DIR.mkdir(parents=True, exist_ok=True)
SCHEMA_DIR.mkdir(parents=True, exist_ok=True)


def load_notes():
    if NOTES_FILE.exists():
        return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
    return []


def save_notes(notes):
    NOTES_FILE.write_text(
        json.dumps(notes, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def create_youtube_script(study):
    filename = study["sujet"].lower().replace(" ", "-") + "-youtube.md"
    path = YOUTUBE_DIR / filename

    script = f"""# Script YouTube

## Titre
Quelle mauvaise herbe spirituelle bloque ma croissance ? - {study['sujet']}

## Introduction
Aujourd'hui, on parle de : {study['sujet']}.

## Situation
{study['situation']}

## Verset principal
{study['verset']}

## Mauvaise herbe
{study['mauvaise_herbe']}

## Bande florale
{study['bande_florale']}

## Importance de Jésus
{study['jesus']}

## Application
Quelle action concrète puis-je faire aujourd'hui pour mieux suivre Jésus ?
"""

    path.write_text(script, encoding="utf-8")
    return path


def create_schema(study):
    filename = study["sujet"].lower().replace(" ", "-") + "-schema.md"
    path = SCHEMA_DIR / filename

    schema = f"""# Schéma spirituel : {study['sujet']}

```text
                Ma marche avec Jésus
                         |
        --------------------------------
        |                              |
 Mauvaise herbe                 Bande florale
        |                              |
 {study['mauvaise_herbe']}       {study['bande_florale']}
        |                              |
 Cycle mauvais                  Cycle divin
        |                              |
 Éloignement                    Paix et croissance
        |                              |
        -------- Jésus au centre -------
                         |
 {study['jesus']}

"""

path.write_text(schema, encoding="utf-8")
return path

st.set_page_config(
page_title="Bible Study OS",
page_icon="📖",
layout="wide"
)

st.title("📖 Bible Study OS")
st.write("Lire → Comprendre → Méditer → Voir Jésus → Appliquer → Progresser")

menu = st.sidebar.radio(
"Menu",
[
"Accueil",
"Créer une étude",
"Mes études",
"Analyse spirituelle",
"YouTube",
"Schéma"
]
)

notes = load_notes()

if menu == "Accueil":
st.header("Bienvenue dans Bible Study OS")

st.write("""
Cette plateforme t'aide à organiser tes études bibliques avec une image agricole :

- Les **mauvaises herbes** représentent ce qui nuit à ta marche spirituelle.
- Les **bandes florales** représentent ce qui t'aide à grandir.
- Jésus reste au centre de chaque analyse.
""")

st.info("Rappel : prends régulièrement une photo de ton carnet papier pour garder une trace de tes réflexions.")

elif menu == "Créer une étude":
st.header("Créer une nouvelle étude biblique")

with st.form("study_form"):
    sujet = st.text_input("Sujet de l'étude")
    situation = st.text_area("Situation personnelle ou question")
    verset = st.text_input("Verset principal")
    note = st.text_area("Note personnelle")
    mauvaise_herbe = st.text_input("Mauvaise herbe spirituelle")
    bande_florale = st.text_input("Bande florale spirituelle")
    jesus = st.text_area("Où est Jésus dans cette étude ?")

    submitted = st.form_submit_button("Enregistrer l'étude")

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

        st.success("Étude enregistrée avec succès.")
        st.info("N'oublie pas de prendre une photo de ton carnet papier.")

elif menu == "Mes études":
st.header("Mes études bibliques")

if not notes:
    st.warning("Aucune étude enregistrée pour le moment.")
else:
    for index, study in enumerate(notes, start=1):
        with st.expander(f"{index}. {study['sujet']}"):
            st.write(f"**Date :** {study['date']}")
            st.write(f"**Verset :** {study['verset']}")
            st.write(f"**Situation :** {study['situation']}")
            st.write(f"**Note :** {study['note']}")
            st.write(f"**Mauvaise herbe :** {study['mauvaise_herbe']}")
            st.write(f"**Bande florale :** {study['bande_florale']}")
            st.write(f"**Jésus :** {study['jesus']}")

elif menu == "Analyse spirituelle":
st.header("Analyse spirituelle")

if not notes:
    st.warning("Aucune étude disponible.")
else:
    study = notes[-1]

    st.subheader(study["sujet"])
    st.write(f"**Situation :** {study['situation']}")
    st.write(f"**Verset :** {study['verset']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌿 Cycle mauvais")
        st.write(f"{study['mauvaise_herbe']} → mauvaise pensée → mauvais choix → conséquence → éloignement spirituel")

    with col2:
        st.markdown("### 🌸 Cycle divin")
        st.write(f"Parole de Dieu → méditation → prière → {study['bande_florale']} → paix → croissance")

    st.markdown("### ✝️ Importance de Jésus")
    st.write(study["jesus"])

elif menu == "YouTube":
st.header("Générer un script YouTube")

if not notes:
    st.warning("Aucune étude disponible.")
else:
    study = notes[-1]
    st.write(f"Dernière étude : **{study['sujet']}**")

    if st.button("Créer le script YouTube"):
        path = create_youtube_script(study)
        st.success(f"Script créé : {path}")

elif menu == "Schéma":
st.header("Générer un schéma spirituel")

if not notes:
    st.warning("Aucune étude disponible.")
else:
    study = notes[-1]
    st.write(f"Dernière étude : **{study['sujet']}**")

    if st.button("Créer le schéma"):
        path = create_schema(study)
        st.success(f"Schéma créé : {path}")

