import random
import models
import joueurs as j


# Ajout du nombre de joueurs à partir des noms, prénoms et classement attribués aléatoirement.
def auto_joueurs(nb_joueurs):
    joueur_list = []
    for p in range(nb_joueurs):
        # Liste de 100 noms
        nom = j.nom()
        # Liste de 100 prénom
        prenom = j.prenom()
        joueur_list.append(models.Joueur(random.choice(prenom), random.choice(nom), random.randint(800, 1500)))

    return joueur_list


# Ajout manuel des joueurs
def manuel_joueur(tournoi):
    joueur = models.Joueur(input("prenom: "), input("nom: "), int(input("côte: ")))
    tournoi.participants.append(joueur)
    retry = input("Ajouter d'autre joueurs? y/n:  ").lower()
    if retry == "y":
        manuel_auto = int(input("manuel(écrire 0) ou auto(écrire 1)? : "))
        if manuel_auto == 0:
            manuel_joueur(tournoi)
        elif manuel_auto == 1:
            players = auto_joueurs(int(input("Combien de joueurs? : ")))
            for joueurs in players:
                tournoi.participants.append(joueurs)
        else:
            print("Choisissez 0 ou 1 !")
    elif retry == "n":
        pass
    else:
        print("répondez y/n")


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


def rapport_tournoi(liste_tournois):
    for tournoi in liste_tournois:
        print(tournoi)


def rapport_tours(tournoi):
    for tours in tournoi.tournee:
        print(tours)


def rapport_match(tournoi):
    for tours in tournoi.tournee:
        print(tours.nom)
        for match in tours.match:
            print(f"Match {match.n_match}, {match.joueur1.nom} vs {match.joueur2.nom}")
            if type(match.winner) is str:
                print("Egalité !")
            else:
                print(f"{match.winner.nom} gagne !")


def rapport_joueur(tournoi):
    joueurs = tournoi.participants
    sorted_joueurs = sorted(joueurs, key=lambda joueur: (joueur.nom, joueur.rank))
    for player in sorted_joueurs:
        print(player, player.nom, player.rank)


def create_new_tournament():
    # 1. Créer un nouveau tournoi.
    tournoi = models.Tournoi(input("Nom du tournois: "))

    # Ajout manuel
    manuel = input("Ajouter manuellement? y/n: ")
    if manuel == "y":
        manuel_joueur(tournoi)
    elif manuel == "n":
        # 2. Ajouter x joueurs.
        joueur = auto_joueurs(int(input("Nombre de joueurs: ")))
        for player in joueur:
            tournoi.participants.append(player)
    else:
        create_new_tournament()

    # 3. L'ordinateur génère les paires de joueurs.
    for numero_tour in range(1, tournoi.tours + 1):
        pairs = pair(tournoi.participants, numero_tour, tournoi)
        # heure de debut et fin aléatoire
        debut = [random.randint(12, 19), random.randint(0, 59)]
        fin = [debut[0] + random.randint(1, 3), random.randint(0, 59)]
        # Résultats de chaque matches
        final_pairs = resultat(pairs)
        # Transformation des pairs en Match
        matches = []
        n_match = 1
        for match in final_pairs:
            match_final = models.Match(n_match, match[0][0], match[0][1], match[1])
            matches.append(match_final)
            n_match += 1
        tour = models.Tour(
            matches,
            "ROUND {}".format(numero_tour),
            "{}h{}".format(debut[0], debut[1]),
            "{}h{}".format(fin[0], fin[1])
        )

        # 4. Lorsque le tour est terminé j'enregistre le tour dans le tournoi
        tournoi.tournee.append(tour)

    return tournoi
