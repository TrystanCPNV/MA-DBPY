import csv
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("Secrete info.env")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def import_classes(file_path):
    conn = get_connection()
    cursor = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            Nom = row['Nom']
            Salle = row['Salle']
            cursor.execute("INSERT INTO classes (nom, salle) VALUES (%s, %s);", (Nom, Salle))
    conn.commit()
    conn.close()
    print("Import classes terminé.")


def import_students(file_path):
    conn = get_connection()
    cursor = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            Prenom = row['Prenom']
            Nom = row['Nom']
            Email = row['Email']
            Classe_nom = row['Classe']
            # Récupérer l'id de la classe
            cursor.execute("SELECT id FROM classes WHERE nom=%s;", (Classe_nom,))
            Classe_id = cursor.fetchone()
            if classe_id:
                cursor.execute(
                    "INSERT INTO students (prenom, nom, email, classe_id) VALUES (%s, %s, %s, %s);",
                    (Prenom, Nom, Email, Classe_id[0])
                )
    conn.commit()
    conn.close()
    print("Import students terminé.")


# Exemple d'utilisation
import_classes('classes.csv')
import_students('students.csv')


# 1. Afficher l’ordre en classe
def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, prenom, classe_id FROM students ORDER BY classe_id, nom;")
    result = cursor.fetchall()
    conn.close()
    return result


# 2. Générer le planning « Ordre en classe »
def generate_planning():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.classe_id, p.date, s.nom, s.prenom, p.valide
        FROM planning p
        JOIN students s ON p.eleve_id = s.id
        ORDER BY p.date, p.classe_id;
    """)
    result = cursor.fetchall()
    conn.close()
    return result


# 3. Valider l’ordre en classe de la semaine
def validate_week():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE planning SET valide=1 WHERE WEEK(date) = WEEK(CURDATE());")
    conn.commit()
    conn.close()


# 4. Supprimer un élève
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s;", (student_id,))
    conn.commit()
    conn.close()


# 5. Ajouter un élève
def add_student(nom, prenom, classe_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (nom, prenom, classe_id) VALUES (%s, %s, %s);",
                   (nom, prenom, classe_id))
    conn.commit()
    conn.close()
