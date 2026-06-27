from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
YOUTUBE_DIR = BASE_DIR / "youtube" / "scripts"
SCHEMA_DIR = BASE_DIR / "docs" / "schemas"

NOTES_FILE = DATA_DIR / "notes.json"
PHOTOS_FILE = DATA_DIR / "photos_carnet.txt"

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


def slugify(text):
    return (
        text.lower()
        .replace(" ", "-")
        .replace("'", "")
        .replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
        .replace("à", "a")
        .replace("ç", "c")
    )


def create_study():
    print("\n=== Nouvelle étude biblique ===")

    subject = input("Sujet de l'étude : ")
    situation = input("Situation personnelle ou question : ")
    verse = input("Verset principal : ")
    note = input("Note / réflexion : ")

    weed = input("Mauvaise herbe spirituelle à enlever : ")
    flower = input("Bande florale spirituelle à cultiver : ")
    jesus = input("Où est Jésus dans cette étude ? ")

    study = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "subject": subject,
        "situation": situation,
        "verse": verse,
        "note": note,
        "mauvaise_herbe": weed,
        "bande_florale": flower,
        "importance_de_jesus": jesus
    }

    notes = load_notes()
    notes.append(study)
    save_notes(notes)

    print("\nÉtude enregistrée avec succès.")
    print("N'oublie pas de prendre une photo de ton carnet papier.")


def list_studies():
    notes = load_notes()

    if not notes:
        print("\nAucune étude enregistrée pour le moment.")
        return

    print("\n=== Mes études bibliques ===")

    for index, study in enumerate(notes, start=1):
        print(f"\n{index}. {study['subject']}")
        print(f"Date : {study['date']}")
        print(f"Verset : {study['verse']}")
        print(f"Mauvaise herbe : {study['mauvaise_herbe']}")
        print(f"Bande florale : {study['bande_florale']}")
        print(f"Jésus : {study['importance_de_jesus']}")


def analyze_last_study():
    notes = load_notes()

    if not notes:
        print("\nAucune étude à analyser.")
        return

    study = notes[-1]

    print("\n=== Analyse spirituelle ===")
    print(f"Sujet : {study['subject']}")
    print(f"Situation : {study['situation']}")
    print(f"Verset : {study['verse']}")

    print("\nCycle mauvais possible :")
    print(f"{study['mauvaise_herbe']} -> mauvaise pensée -> mauvais choix -> conséquence -> éloignement spirituel")

    print("\nCycle divin opposé :")
    print(f"Parole de Dieu -> méditation -> prière -> {study['bande_florale']} -> paix -> progrès spirituel")

    print("\nImportance de Jésus :")
    print(study["importance_de_jesus"])

    print("\nQuestion de méditation :")
    print("Quelle action concrète puis-je faire aujourd'hui pour suivre Jésus plus fidèlement ?")


def add_paper_photo_reference():
    print("\n=== Photo du carnet papier ===")
    photo_name = input("Nom ou chemin de la photo du carnet papier : ")

    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {photo_name}\n"

    with PHOTOS_FILE.open("a", encoding="utf-8") as file:
        file.write(line)

    print("Photo référencée.")
    print("Plus tard, le logiciel pourra analyser cette photo automatiquement.")


def generate_youtube_script():
    notes = load_notes()

    if not notes:
        print("\nAucune étude disponible pour créer une vidéo.")
        return

    study = notes[-1]
    filename = slugify(study["subject"]) + "-" + datetime.now().strftime("%Y%m%d-%H%M") + ".md"
    path = YOUTUBE_DIR / filename

    script = f"""# Script YouTube

## Titre
Quelle mauvaise herbe spirituelle bloque ma croissance ? - {study['subject']}

## Introduction
Aujourd'hui, on va réfléchir à un sujet important : {study['subject']}.

## Situation
{study['situation']}

## Verset principal
{study['verse']}

## Mauvaise herbe spirituelle
{study['mauvaise_herbe']}

Cette mauvaise herbe peut étouffer la paix intérieure et ralentir la croissance spirituelle.

## Bande florale spirituelle
{study['bande_florale']}

Cette bande florale aide à construire une meilleure relation avec Dieu.

## Où est Jésus dans cette étude ?
{study['importance_de_jesus']}

## Application personnelle
Aujourd'hui, je peux choisir une action simple pour enlever cette mauvaise herbe et cultiver cette bande florale.

## Question finale
Quelle mauvaise herbe dois-tu enlever aujourd'hui pour mieux suivre Jésus ?
"""

    path.write_text(script, encoding="utf-8")
    print(f"\nScript YouTube créé : {path}")


def generate_schema():
    notes = load_notes()

    if not notes:
        print("\nAucune étude disponible pour créer un schéma.")
        return

    study = notes[-1]
    filename = slugify(study["subject"]) + "-schema.md"
    path = SCHEMA_DIR / filename

    schema = f"""# Schéma spirituel : {study['subject']}

```text
                 Marche avec Jésus
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
 {study['importance_de_jesus']}

"""

path.write_text(schema, encoding="utf-8")
print(f"\nSchéma créé : {path}")

def main():
while True:
print("\n==============================")
print("Bible Study OS")
print("==============================")
print("1. Créer une étude biblique")
print("2. Voir mes études")
print("3. Analyser la dernière étude")
print("4. Ajouter une photo du carnet papier")
print("5. Générer un script YouTube")
print("6. Générer un schéma")
print("0. Quitter")

    choice = input("\nChoix : ")

    if choice == "1":
        create_study()
    elif choice == "2":
        list_studies()
    elif choice == "3":
        analyze_last_study()
    elif choice == "4":
        add_paper_photo_reference()
    elif choice == "5":
        generate_youtube_script()
    elif choice == "6":
        generate_schema()
    elif choice == "0":
        print("À bientôt. Continue ta marche avec sagesse.")
        break
    else:
        print("Choix invalide.")

if name == "main":
main()
