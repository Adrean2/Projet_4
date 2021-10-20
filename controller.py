import models
import vue
import random


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


# Création des pairs
def pair(pool, numero_tour, tournoi):
    # Trie à partir du rang des joueurs
    pairs = []
    if numero_tour == 1:
        sorted_list = sorted(pool, key=lambda joueur: joueur.rank, reverse=True)
        # modulable pour plus de joueurs
        top_tier = sorted_list[0:int(len(sorted_list)/2)]
        low_tier = sorted_list[len(top_tier):len(sorted_list)+1]
        # attribution d'une paire en fonction de leur classement et de leurs résultats (en ronde suisse)
        index = 0
        for pair in range(len(top_tier)):
            pick = top_tier[index]
            pick2 = low_tier[index]
            pairs.append([[pick, pick2], []])
            if index <= len(top_tier):
                index += 1

    # Trie à partir de leurs points après le 2ème tour
    else:
        sorted_list = sorted(pool, key=lambda joueur: (joueur.point, joueur.rank), reverse=True)
        for index_n in range(int(len(sorted_list)/2)):
            faced_before = False
            pick = sorted_list[0]
            pick2 = sorted_list[1]
            # Vérification si les joueurs se sont déjà affrontés
            for tours in tournoi.tournee:
                for match in tours.match:
                    joueurs = [match.joueur1, match.joueur2]
                    if pick in joueurs and pick2 in joueurs:
                        if len(sorted_list) >= 3:
                            faced_before = True
            if faced_before is True and len(sorted_list) > 2:
                pick2 = sorted_list[2]
            pairs.append([[pick, pick2], []])
            sorted_list.remove(pick)
            sorted_list.remove(pick2)

    return pairs

# Détermine un gagnant ou une égalité lors d'un match
def resultat(pairs):
    for pair in pairs:
        p1 = pair[0][0]
        p2 = pair[0][1]
        outcome = [1, 0, 1/2]
        result = random.choice(outcome)
        if result == 1 or result == 0:
            winner = random.choice((p1, p2))
            winner.point += 1
            pair[1] = winner
        else:
            p1.point += result
            p2.point += result
            pair[1] = "EGALITE"

    return tuple(pairs)


if __name__ == '__main__':
    menu()
