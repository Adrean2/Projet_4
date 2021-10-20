import models
import vue


def menu():
    tournois = []
    running = True
    while running is True:
        print("""\nMENU PRINCIPAL\n
                \n1: Créer un tournoi
                \n2: Regarder stats tournoi
                \n3: Sauvegarder/Charger
                \n4: Exit
                \n""")
        choix1 = int(input("Quel choix?: "))

        # Création tournois
        if choix1 == 1:
            tn = vue.create_new_tournament()
            tournois.append(tn)

        # Récupération/affichage des stats
        elif choix1 == 2:
            if len(tournois) >= 1:
                print(
                    """ \n Quelles stats voulez-vous voir?\n1: Tournois
                        \n2: Joueurs\n3: Tours\n4: Matches\n5: Exit """)
                choix2 = int(input("Quel est votre choix?: "))
                if choix2 in range(2, 5):
                    for tournoi in tournois:
                        print(f"Le tournoi '{tournoi.nom}' a l'index '{tournois.index(tournoi)}'")
                    choix_tournois = int(input("Pour quel tournois ?: "))
                    tournois_choisis = tournois[choix_tournois]
                if choix2 == 1:
                    vue.rapport_tournoi(tournois)
                elif choix2 == 2:
                    vue.rapport_joueur(tournois_choisis)
                elif choix2 == 3:
                    vue.rapport_tours(tournois_choisis)
                elif choix2 == 4:
                    vue.rapport_match(tournois_choisis)
                elif choix2 == 5:
                    pass
                else:
                    print("\nFaites un choix valide! (1 à 5)")
            else:
                print("\nIl n'y a pas encore de tournoi !!")
        elif choix1 == 3:
            choix2 = int(input("1: Sauvegarder\n2: Charger\n3: Retour \nQuel est votre choix?: "))
            if choix2 == 1:
                # Sauvegarde dans le db.json
                for tournoi in tournois:
                    models.tiny_save(tournoi, tournois)
            # Chargement des joueurs et tournois
            elif choix2 == 2:
                tournois = []
                for tournoi in models.db.table("tournois"):
                    dz_tournoi = models.deserializing_tournoi(tournoi)
                    tournois.append(dz_tournoi)
                print(tournois)
        # Fermeture de l'application
        elif choix1 == 4:
            print("Goodbye ! ")
            running = False
        else:
            print("Faites un choix valide! (1 à 4)")


if __name__ == '__main__':
    menu()
