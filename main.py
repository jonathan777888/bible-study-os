from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
NOTES_FILE = DATA_DIR / "notes.json"
RELATION_FILE = DATA_DIR / "relation_jesus.json"
DATA_DIR.mkdir(exist_ok=True)

BASE_REFLECTIONS = [
    {
        "source": "bilan",
        "question": "Est-ce que je recherche premièrement le Royaume des cieux ?",
        "reponse": "Durant mon périple de 40 jours, oui. Mais en toute honnêteté, je veux revenir plus profondément.",
        "categorie": "Royaume",
    },
    {
        "source": "bilan",
        "question": "Est-ce que je me pardonne ? Et est-ce que je pardonne les autres ?",
        "reponse": "Oui.",
        "categorie": "Pardon",
    },
    {
        "source": "bilan",
        "question": "Est-ce que je savoure le processus de croissance ?",
        "reponse": "Je vois plus clair.",
        "categorie": "Croissance",
    },
    {
        "source": "bilan",
        "question": "Est-ce que l’amour vient de Jésus-Christ ?",
        "reponse": "Cet amour est fraternel.",
        "categorie": "Amour",
    },
    {
        "source": "nutriments",
        "question": "La prière",
        "reponse": "Oui.",
        "categorie": "Nutriment spirituel",
    },
    {
        "source": "nutriments",
        "question": "La Parole",
        "reponse": "Oui.",
        "categorie": "Nutriment spirituel",
    },
    {
        "source": "nutriments",
        "question": "L’obéissance et la crainte envers Jéhovah",
        "reponse": "Oui.",
        "categorie": "Nutriment spirituel",
    },
    {
        "source": "nutriments",
        "question": "L’humilité",
        "reponse": "Tu es ma force.",
        "categorie": "Nutriment spirituel",
    },
    {
        "source": "nutriments",
        "question": "La maîtrise de soi",
        "reponse": "Aide-moi Père.",
        "categorie": "Nutriment spirituel",
    },
    {
        "source": "nutriments",
        "question": "La confiance",
        "reponse": "J’ai confiance en Dieu.",
        "categorie": "Confiance",
    },
    {
        "source": "nutriments",
        "question": "Est-ce que tu as peur du futur ?",
        "reponse": "Oui.",
        "categorie": "Peur",
    },
    {
        "source": "nutriments",
        "question": "As-tu toujours besoin de tout contrôler ou laisses-tu Jéhovah prendre le relais à travers Jésus-Christ ?",
        "reponse": "Je laisse tout dans les mains de Dieu.",
        "categorie": "Abandon",
    },
    {
        "source": "nutriments",
        "question": "Te compares-tu avec d’autres personnes ?",
        "reponse": "Parfois, mais mon histoire est entre Dieu et moi.",
        "categorie": "Comparaison",
    },
]

SOS_STUDY = {
    "sujet": "Quand je suis seul, je cherche un faux refuge",
    "situation": "Je suis tenté de retourner vers la pornographie ou la masturbation pour soulager la solitude.",
    "verset": "Matthieu 6:33",
    "note": "La vie n’est pas seulement performance. Le but est de revenir à Dieu une étape à la fois.",
    "mauvaise_herbe": "Chercher un soulagement rapide au lieu de me réfugier en Dieu.",
    "bande_florale": "Confiance en Jéhovah dans la solitude.",
    "jesus": "Jésus a donné sa vie pour que ma chute ne devienne pas mon abandon.",
    "action_1_minute": "Éloigner l’écran pendant 5 minutes et dire une prière courte.",
    "humeur": "tentation / solitude",
}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_notes() -> list[dict[str, Any]]:
    return load_json(NOTES_FILE, [])


def save_notes(notes: list[dict[str, Any]]) -> None:
    save_json(NOTES_FILE, notes)


def load_relation() -> list[dict[str, Any]]:
    relation = load_json(RELATION_FILE, [])
    if not relation:
        save_json(RELATION_FILE, BASE_REFLECTIONS)
        relation = BASE_REFLECTIONS
    return relation


def normalize_study(study: dict[str, Any]) -> dict[str, Any]:
    return {
        "date": study.get("date", datetime.now().strftime("%Y-%m-%d %H:%M")),
        "sujet": study.get("sujet") or study.get("subject") or "Sans sujet",
        "situation": study.get("situation", ""),
        "verset": study.get("verset") or study.get("verse") or "",
        "note": study.get("note", ""),
        "mauvaise_herbe": study.get("mauvaise_herbe", ""),
        "bande_florale": study.get("bande_florale", ""),
        "jesus": study.get("jesus") or study.get("importance_de_jesus") or "",
        "action_1_minute": study.get("action_1_minute", ""),
        "humeur": study.get("humeur", ""),
    }


def add_study(study: dict[str, Any]) -> None:
    notes = [normalize_study(item) for item in load_notes()]
    normalized = normalize_study(study)
    normalized["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    notes.append(normalized)
    save_notes(notes)


def parse_uploaded_excel(uploaded_file: Any) -> list[dict[str, str]]:
    try:
        import pandas as pd
    except ImportError:
        st.error("Pour importer Excel, ajoute pandas et openpyxl dans requirements.txt.")
        return []

    sheets = pd.read_excel(uploaded_file, sheet_name=None, header=None)
    rows: list[dict[str, str]] = []
    for sheet_name, frame in sheets.items():
        for _, row in frame.iterrows():
            values = ["" if pd.isna(value) else str(value).strip() for value in row.tolist()[:3]]
            if not any(values):
                continue
            question = values[0] or values[1]
            answer = values[1] if values[0] else values[2]
            if question.lower() in {"oui", "non"}:
                continue
            rows.append(
                {
                    "source": sheet_name,
                    "question": question,
                    "reponse": answer,
                    "categorie": "Import Excel",
                }
            )
    return rows


st.set_page_config(page_title="Bible Study OS", page_icon="📖", layout="wide")

st.sidebar.title("Bible Study OS")
page = st.sidebar.radio(
    "Menu",
    [
        "Accueil",
        "SOS solitude / tentation",
        "Créer une étude",
        "Ma relation avec Jésus",
        "Jardin spirituel",
        "Mes études",
        "YouTube Studio",
    ],
)

notes = [normalize_study(item) for item in load_notes()]
relation = load_relation()

if page == "Accueil":
    st.title("📖 Bible Study OS")
    st.caption("Lire → Comprendre → Méditer → Voir Jésus → Appliquer → Progresser")
    st.markdown(
        """
        ### But
        T’aider à revenir à Dieu une étape à la fois, sans honte inutile, avec Jésus au centre.

        **Mauvaise herbe** : pensée, habitude ou influence qui étouffe ta marche spirituelle.  
        **Bande florale** : pratique, vérité ou action qui te rapproche de Dieu par Jésus.
        """
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Études", len(notes))
    col2.metric("Réflexions relation", len(relation))
    col3.metric("Action", "1 chose à la fois")

    st.info("Phrase centrale : Jésus n’est pas mort pour que ta chute devienne ton abandon. Il est mort pour que tu reviennes à Dieu.")

elif page == "SOS solitude / tentation":
    st.title("🛟 SOS solitude / tentation")
    st.subheader("Une seule chose maintenant")
    st.success("Éloigne ton écran de ton corps pendant 5 minutes.")
    st.markdown(
        """
        Quand tu es seul, le but n’est pas de prouver que tu es fort.  
        Le but est de revenir au bon refuge.

        **Prière courte :**  
        Jéhovah, quand je suis seul, aide-moi à ne pas chercher un faux refuge. Apprends-moi à te faire confiance maintenant.
        """
    )
    if st.button("Enregistrer cette chute comme étude de restauration"):
        add_study(SOS_STUDY)
        st.success("Étude SOS enregistrée. Tu reprends le chemin, une étape à la fois.")

elif page == "Créer une étude":
    st.title("Créer une étude biblique")
    with st.form("study_form"):
        sujet = st.text_input("Sujet", value="Quand je suis seul, je veux faire confiance à Dieu")
        situation = st.text_area("Situation ou question")
        verset = st.text_input("Verset principal", value="Matthieu 6:33")
        note = st.text_area("Note personnelle")
        col1, col2 = st.columns(2)
        with col1:
            mauvaise_herbe = st.text_input("Mauvaise herbe spirituelle")
            humeur = st.selectbox("État du moment", ["", "solitude", "tentation", "peur", "fatigue", "culpabilité", "paix", "gratitude"])
        with col2:
            bande_florale = st.text_input("Bande florale spirituelle")
            action_1_minute = st.text_input("Action de 1 minute")
        jesus = st.text_area("Où est Jésus dans cette étude ?")
        submitted = st.form_submit_button("Enregistrer")

    if submitted:
        add_study(
            {
                "sujet": sujet,
                "situation": situation,
                "verset": verset,
                "note": note,
                "mauvaise_herbe": mauvaise_herbe,
                "bande_florale": bande_florale,
                "jesus": jesus,
                "action_1_minute": action_1_minute,
                "humeur": humeur,
            }
        )
        st.success("Étude enregistrée avec succès.")

elif page == "Ma relation avec Jésus":
    st.title("Ma relation avec Jésus")
    st.write("Cette section transforme ton fichier Excel en carnet spirituel propre : questions, réponses, catégories et progression.")

    uploaded = st.file_uploader("Importer ton fichier Excel 'ma relation avec Jésus'", type=["xlsx"])
    if uploaded is not None:
        imported_rows = parse_uploaded_excel(uploaded)
        if imported_rows:
            save_json(RELATION_FILE, imported_rows)
            relation = imported_rows
            st.success(f"{len(imported_rows)} lignes importées depuis Excel.")

    categories = Counter(item.get("categorie", "Autre") for item in relation)
    st.subheader("Résumé")
    st.write(dict(categories))

    for item in relation:
        with st.expander(f"{item.get('categorie', 'Autre')} — {item.get('question', '')}"):
            st.write(f"**Source :** {item.get('source', '')}")
            st.write(f"**Réponse :** {item.get('reponse', '')}")
            if st.button("Transformer en étude", key=f"study_{item.get('source','')}_{item.get('question','')}"):
                add_study(
                    {
                        "sujet": item.get("question", "Relation avec Jésus"),
                        "situation": item.get("reponse", ""),
                        "verset": "Matthieu 6:33",
                        "note": "Question issue du carnet Ma relation avec Jésus.",
                        "mauvaise_herbe": "Oublier de chercher d’abord le Royaume.",
                        "bande_florale": item.get("categorie", "Confiance"),
                        "jesus": "Jésus me ramène vers le Père et m’apprend à vivre dans la vérité.",
                        "action_1_minute": "Prier honnêtement pendant 1 minute.",
                    }
                )
                st.success("Transformé en étude.")

elif page == "Jardin spirituel":
    st.title("Jardin spirituel")
    st.caption("Voir les mauvaises herbes qui reviennent et les bandes florales à cultiver.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Études", len(notes))
    col2.metric("Mauvaises herbes uniques", len({n.get("mauvaise_herbe") for n in notes if n.get("mauvaise_herbe")}))
    col3.metric("Bandes florales uniques", len({n.get("bande_florale") for n in notes if n.get("bande_florale")}))

    weeds = Counter(n.get("mauvaise_herbe", "").strip() for n in notes if n.get("mauvaise_herbe", "").strip())
    flowers = Counter(n.get("bande_florale", "").strip() for n in notes if n.get("bande_florale", "").strip())

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Mauvaises herbes fréquentes")
        if weeds:
            st.bar_chart(dict(weeds.most_common(10)))
        else:
            st.info("Aucune donnée pour le moment.")
    with col_b:
        st.subheader("Bandes florales fréquentes")
        if flowers:
            st.bar_chart(dict(flowers.most_common(10)))
        else:
            st.info("Aucune donnée pour le moment.")

elif page == "Mes études":
    st.title("Mes études")
    if not notes:
        st.warning("Aucune étude enregistrée.")
    else:
        for index, study in enumerate(reversed(notes), start=1):
            with st.expander(f"{index}. {study.get('sujet', 'Sans sujet')}"):
                st.write(f"**Date :** {study.get('date', '')}")
                st.write(f"**Situation :** {study.get('situation', '')}")
                st.write(f"**Verset :** {study.get('verset', '')}")
                st.write(f"**Note :** {study.get('note', '')}")
                st.write(f"**Mauvaise herbe :** {study.get('mauvaise_herbe', '')}")
                st.write(f"**Bande florale :** {study.get('bande_florale', '')}")
                st.write(f"**Jésus :** {study.get('jesus', '')}")
                st.write(f"**Action 1 minute :** {study.get('action_1_minute', '')}")

elif page == "YouTube Studio":
    st.title("YouTube Studio")
    if not notes:
        st.warning("Aucune étude disponible pour créer un script.")
    else:
        study = notes[-1]
        script = f"""# Script YouTube

## Titre
{study.get('sujet', '')}

## Introduction
Aujourd’hui, je parle d’une lutte réelle : {study.get('situation', '')}

## Verset principal
{study.get('verset', '')}

## Mauvaise herbe
{study.get('mauvaise_herbe', '')}

## Bande florale
{study.get('bande_florale', '')}

## Où est Jésus ?
{study.get('jesus', '')}

## Application simple
{study.get('action_1_minute', 'Faire une seule chose fidèle maintenant.')}

## Conclusion
La vie n’est pas seulement performance. Le chemin, c’est revenir à Dieu une étape à la fois.
"""
        st.text_area("Script généré", script, height=500)
        st.download_button("Télécharger le script", script, file_name="script-bible-study-os.md", mime="text/markdown")
