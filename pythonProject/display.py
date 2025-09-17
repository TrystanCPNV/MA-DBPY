import database

def menu():
    while True:
        print("\n=== MENU ORDRE EN CLASSE ===")
        print("1. Afficher l’ordre en classe")
        print("2. Générer le planning")
        print("3. Valider l’ordre en classe de la semaine")
        print("4. Supprimer un élève")
        print("5. Ajouter un élève")
        print("6. Générer le document « Ordre en classe »")
        print("7. Sortir")

        choix = input("Choix : ")

        if choix == "1":
            eleves = database.get_students()
            print("\nListe des élèves :")
            for e in eleves:
                print(f"ID: {e[0]}, Nom: {e[1]}, Prénom: {e[2]}, Classe: {e[3]}")
        elif choix == "2":
            planning = database.generate_planning()
            print("\nPlanning généré :")
            for p in planning:
                print(f"ID: {p[0]}, Classe: {p[1]}, Date: {p[2]}, Nom: {p[3]}, Prénom: {p[4]}, Validé: {p[5]}")
        elif choix == "3":
            database.validate_week()
            print("Ordre en classe de la semaine validé.")
        elif choix == "4":
            id_eleve = input("ID de l’élève à supprimer : ")
            database.delete_student(id_eleve)
            print("Élève supprimé.")
        elif choix == "5":
            nom = input("Nom de l’élève : ")
            prenom = input("Prénom de l’élève : ")
            classe_id = input("Classe ID : ")
            database.add_student(nom, prenom, classe_id)
            print("Élève ajouté.")
        elif choix == "6":
            print("Génération du document (à coder selon le format souhaité).")
        elif choix == "7":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
