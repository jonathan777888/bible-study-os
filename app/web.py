import streamlit as st
from pathlib import Path
import json
import unicodedata
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



def normalize_text(value):
    value = value.lower().strip()
    value = unicodedata.normalize("NFD", value)
    value = "".join(char for char in value if unicodedata.category(char) != "Mn")
    return value


def load_verse_library():
    versets_file = DATA_DIR / "versets.json"

    if not versets_file.exists():
        return []

    return json.loads(versets_file.read_text(encoding="utf-8"))


def find_theme_items(query):
    query_clean = normalize_text(query)

    if not query_clean:
        return []

    results = []

    for item in load_verse_library():
        searchable_text = " ".join([
            item.get("theme", ""),
            item.get("type", ""),
            item.get("idee", ""),
            item.get("jesus", "")
        ])

        if query_clean in normalize_text(searchable_text):
            results.append(item)

    return results


def render_biblical_suggestions(title, theme):
    st.markdown(f"#### {title} : {theme}")

    results = find_theme_items(theme)

    if not results:
        st.info("Aucune référence trouvée pour ce thème dans la bibliothèque actuelle.")
        return

    for item in results:
        with st.expander(f"{item['theme']} - {item['type']}"):
            st.write("**Références :**")
            for ref in item["references"]:
                st.write(f"- {ref}")

            st.write(f"**Idée principale :** {item['idee']}")
            st.write(f"**Importance de Jésus :** {item['jesus']}")




def create_youtube_short_pack(study):
    shorts_dir = BASE_DIR / "youtube" / "shorts"
    subtitles_dir = BASE_DIR / "youtube" / "subtitles"
    prompts_dir = BASE_DIR / "youtube" / "prompts"

    shorts_dir.mkdir(parents=True, exist_ok=True)
    subtitles_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    base_name = safe_filename(study.get("sujet", "etude"))

    short_path = shorts_dir / f"{base_name}-short.md"
    srt_path = subtitles_dir / f"{base_name}.srt"
    prompts_path = prompts_dir / f"{base_name}-prompts.md"

    short_script = f"""# Script YouTube Shorts : {study.get('sujet', '')}

## Durée visée
45 à 60 secondes

## Hook
Quelle mauvaise herbe spirituelle bloque ta croissance ?

## Script
Aujourd'hui, on parle de : {study.get('sujet', '')}.

Dans cette étude, la mauvaise herbe à surveiller est : {study.get('mauvaise_herbe', '')}.

Cette mauvaise herbe peut créer un mauvais cycle :
mauvaise pensée, mauvais choix, conséquence, puis éloignement spirituel.

Mais il existe une bande florale à cultiver : {study.get('bande_florale', '')}.

Cette qualité peut t'aider à revenir vers un cycle divin :
Parole de Dieu, méditation, prière, paix et croissance.

Le verset principal est : {study.get('verset', '')}.

Et surtout, Jésus est au centre de cette étude :
{study.get('jesus', '')}

Question finale :
Quelle mauvaise herbe dois-tu enlever cette semaine pour mieux suivre Jésus ?
"""

    subtitles = f"""1
00:00:00,000 --> 00:00:04,000
Quelle mauvaise herbe spirituelle bloque ta croissance ?

2
00:00:04,000 --> 00:00:09,000
Aujourd'hui, on parle de : {study.get('sujet', '')}.

3
00:00:09,000 --> 00:00:15,000
La mauvaise herbe à surveiller est : {study.get('mauvaise_herbe', '')}.

4
00:00:15,000 --> 00:00:22,000
Elle peut créer un mauvais cycle : pensée, choix, conséquence, éloignement.

5
00:00:22,000 --> 00:00:29,000
La bande florale à cultiver est : {study.get('bande_florale', '')}.

6
00:00:29,000 --> 00:00:36,000
Elle aide à revenir vers la paix, la prière et la croissance spirituelle.

7
00:00:36,000 --> 00:00:43,000
Verset principal : {study.get('verset', '')}.

8
00:00:43,000 --> 00:00:52,000
Jésus est au centre : {study.get('jesus', '')}

9
00:00:52,000 --> 00:01:00,000
Quelle mauvaise herbe dois-tu enlever cette semaine pour mieux suivre Jésus ?
"""

    prompts = f"""# Prompts visuels pour la vidéo : {study.get('sujet', '')}

## Image 1 : Introduction
Un carnet biblique ouvert sur une table, lumière douce, ambiance calme, style éducatif spirituel.

## Image 2 : Mauvaise herbe
Une petite plante étouffée par une mauvaise herbe, symbole de {study.get('mauvaise_herbe', '')}, style simple et clair.

## Image 3 : Cycle mauvais
Un schéma circulaire montrant : mauvaise pensée -> mauvais choix -> conséquence -> éloignement spirituel.

## Image 4 : Bande florale
Un chemin avec des fleurs lumineuses représentant {study.get('bande_florale', '')}, ambiance paisible.

## Image 5 : Verset
Une Bible ouverte avec une lumière douce, texte : {study.get('verset', '')}.

## Image 6 : Jésus au centre
Un chemin lumineux qui mène vers Jésus, avec une personne qui avance avec espoir et humilité.

## Image 7 : Application
Une main qui enlève une mauvaise herbe et plante une fleur, symbole de transformation spirituelle.

## Image 8 : Question finale
Carnet papier, stylo, jardin spirituel en arrière-plan, texte : Quelle mauvaise herbe dois-tu enlever cette semaine ?
"""

    short_path.write_text(short_script, encoding="utf-8")
    srt_path.write_text(subtitles, encoding="utf-8")
    prompts_path.write_text(prompts, encoding="utf-8")

    return short_path, srt_path, prompts_path


def create_storyboard(study):
    storyboard_dir = BASE_DIR / "youtube" / "storyboards"
    storyboard_dir.mkdir(parents=True, exist_ok=True)

    filename = safe_filename(study.get("sujet", "etude")) + "-storyboard.md"
    path = storyboard_dir / filename

    content = f"""# Storyboard YouTube : {study.get('sujet', '')}

## Format
Vidéo courte ou vidéo YouTube éducative.

## Objectif de la vidéo
Aider à comprendre une mauvaise herbe spirituelle, cultiver une bande florale, et voir l'importance de Jésus.

---

## Scène 1 : Introduction

**Texte à l'écran :**
Quelle mauvaise herbe bloque ma croissance spirituelle ?

**Voix :**
Aujourd'hui, on parle de : {study.get('sujet', '')}.

**Image / schéma :**
Une plante qui grandit, avec une mauvaise herbe autour.

---

## Scène 2 : Situation

**Texte à l'écran :**
Situation ou question

**Voix :**
{study.get('situation', '')}

**Image / schéma :**
Carnet ouvert avec une note personnelle.

---

## Scène 3 : Mauvaise herbe

**Texte à l'écran :**
Mauvaise herbe : {study.get('mauvaise_herbe', '')}

**Voix :**
Cette mauvaise herbe peut créer un cycle mauvais : mauvaise pensée, mauvais choix, conséquence, puis éloignement spirituel.

**Image / schéma :**
Racines d'une mauvaise herbe qui étouffe une plante.

---

## Scène 4 : Bande florale

**Texte à l'écran :**
Bande florale : {study.get('bande_florale', '')}

**Voix :**
Cette bande florale aide à remplacer le mauvais cycle par un cycle divin : Parole de Dieu, méditation, prière, paix et croissance.

**Image / schéma :**
Fleurs autour d'un chemin lumineux.

---

## Scène 5 : Verset principal

**Texte à l'écran :**
{study.get('verset', '')}

**Voix :**
Ce verset nous aide à comprendre le chemin à suivre.

**Image / schéma :**
Bible ouverte avec lumière douce.

---

## Scène 6 : Jésus au centre

**Texte à l'écran :**
Où est Jésus dans cette étude ?

**Voix :**
{study.get('jesus', '')}

**Image / schéma :**
Un chemin centré sur Jésus, avec la lumière qui guide.

---

## Scène 7 : Application

**Texte à l'écran :**
Action aujourd'hui

**Voix :**
Quelle action concrète puis-je faire aujourd'hui pour enlever cette mauvaise herbe et cultiver cette bande florale ?

**Image / schéma :**
Main qui enlève une mauvaise herbe et plante une fleur.

---

## Scène 8 : Question finale

**Texte à l'écran :**
Quelle mauvaise herbe dois-tu enlever cette semaine ?

**Voix :**
Prends un moment pour réfléchir, écrire dans ton carnet, et avancer avec Jésus.

**Image / schéma :**
Carnet papier + jardin spirituel.
"""

    path.write_text(content, encoding="utf-8")
    return path


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

