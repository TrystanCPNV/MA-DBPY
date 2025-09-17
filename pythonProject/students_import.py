import csv
import mysql.connector
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("Secrete info.env")


def get_connection():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    if not all([host, user, password, database]):
        raise ValueError("Une ou plusieurs variables d'environnement manquent !")

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )


def import_students(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            prenom = row['Prenom']
            nom = row['Nom']
            classe_nom = row['Classe']

            # Récupérer l'id de la classe
            cursor.execute("SELECT id FROM classes WHERE nom=%s;", (classe_nom,))
            classe_id = cursor.fetchone()

            if classe_id:
                cursor.execute(
                    "INSERT INTO students (prenom, nom, classe_id) VALUES (%s, %s, %s);",
                    (prenom, nom, classe_id[0])
                )
            else:
                print(f"Classe '{classe_nom}' non trouvée pour l'étudiant {prenom} {nom}.")

    conn.commit()
    conn.close()
    print("Import students terminé.")


if __name__ == "__main__":
    import_students("students.csv")
