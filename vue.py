import random
import models
import controller
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
    tri = int(input("""Trier par :
            \n1 : Ordre alphabétique \n2 : Elo décroissant """))
    if tri == 1 :
        sorted_joueurs = sorted(joueurs, key=lambda joueur: (joueur.nom))
    elif tri == 2:
        sorted_joueurs = sorted(joueurs, key=lambda joueur: (joueur.rank),reverse=True)

    for player in sorted_joueurs:
        print(player, player.nom, player.family_name, player.rank)


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
        pairs = controller.pair(tournoi.participants, numero_tour, tournoi)
        # heure de debut et fin aléatoire
        debut = [random.randint(12, 19), random.randint(0, 59)]
        fin = [debut[0] + random.randint(1, 3), random.randint(0, 59)]
        # Résultats de chaque matches
        final_pairs = controller.resultat(pairs)
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
