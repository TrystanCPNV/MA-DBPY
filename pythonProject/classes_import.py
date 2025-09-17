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


def import_classes(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            nom = row['Nom']
            salle = row['Salle']
            # Insérer ou mettre à jour si le nom existe déjà
            cursor.execute(
                "INSERT INTO classes (nom, salle) VALUES (%s, %s) "
                "ON DUPLICATE KEY UPDATE salle=%s;",
                (nom, salle, salle)
            )

    conn.commit()
    conn.close()
    print("Import classes terminé.")


if __name__ == "__main__":
    import_classes("classes.csv")
