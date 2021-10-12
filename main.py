import random
import joueurs as j
import json
from tinydb import TinyDB
import ast

db = TinyDB("db.json")


class Tournoi:
    def __init__(self, nom):
        self.nom = nom
        self.lieu = ""
        self.date = f"{random.randint(1,31)}/{random.randint(1,12)}"
        self.tours = 4
        self.tournee = []
        self.participants = []
        self.time = random.choice(["bullet", "blitz", "coup rapide"])
        self.description = "Description"


class Joueur:
    def __init__(self, nom, family_name, rank):
        self.nom = nom
        self.family_name = family_name
        self.birthday = f"{random.randint(1,31)}/{random.randint(1,12)}/{random.randint(1950,2015)}"
        self.sexe = random.choice(["Homme", "Femme", "Non-binaire"])
        self.rank = rank
        self.point = 0


class Tour:
    def __init__(self, match, nom, date_heure_debut, date_heure_fin):
        self.match = match
        self.nom = nom
        self.date_heure_debut = date_heure_debut
        self.date_heure_fin = date_heure_fin


class Match:
    def __init__(self, n_match, joueur1, joueur2, winner):
        self.n_match = n_match
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.winner = winner


# Conversions pour tinydb
def serializing_tournois(liste_tournoi):
    liste_serialized_tournoi = []
    for tournoi in liste_tournoi:
        serialized_tournoi = {
            "nom": tournoi.nom,
            "lieu": tournoi.lieu,
            "date": tournoi.date,
            "tours": tournoi.tours,
            "tournee": [serializing_tour(t) for t in tournoi.tournee],
            "participants": serializing_players(tournoi),
            "time": tournoi.time,
            "description": tournoi.description
            }
        liste_serialized_tournoi.append(serialized_tournoi)
    return liste_serialized_tournoi


def serializing_tour(tour):
    serialized_tour = {
        "match": [serializing_match(m) for m in tour.match],
        "nom": tour.nom,
        "date_heure_debut": tour.date_heure_debut,
        "date_heure_fin": tour.date_heure_fin,
        }
    return serialized_tour


def serializing_match(match):
    serialized_match = {
        "joueur1": ast.literal_eval(json.dumps(match.joueur1.__dict__)),
        "joueur2": ast.literal_eval(json.dumps(match.joueur2.__dict__)),
        "n_match": f"Match {match.n_match}, {match.joueur1.nom} vs {match.joueur2.nom}",
    }
    if type(match.winner) is str:
        serialized_match["winner"] = match.winner
    else:
        serialized_match["winner"] = ast.literal_eval(json.dumps(match.winner.__dict__))

    return serialized_match


def serializing_players(tournoi):
    liste__serialized_players = []
    for joueur in tournoi.participants:
        serialized_player = {
            'nom': joueur.nom,
            "family_name": joueur.family_name,
            "birthday": joueur.birthday,
            "sexe": joueur.sexe,
            "rank": joueur.rank,
            "point": joueur.point,
        }
        liste__serialized_players.append(serialized_player)
    return liste__serialized_players


# Conversions depuis la sauvegarde tinydb
def deserializing_tournoi(tournoi):
    dz_tournoi = Tournoi(tournoi["nom"])
    dz_tournoi.lieu = tournoi["lieu"]
    dz_tournoi.date = tournoi["date"]
    dz_tournoi.tours = tournoi["tours"]
    dz_tournoi.tournee = deserializing_tour(tournoi["tournee"])
    dz_tournoi.participants = [deserializing_joueur(joueur) for joueur in tournoi["participants"]]
    dz_tournoi.description = tournoi["description"]
    return dz_tournoi


def deserializing_tour(liste_tour):
    liste_dz_tour = []
    for tour in liste_tour:
        d_tour = Tour(
            deserializing_match(tour["match"]),
            tour["nom"],
            tour["date_heure_debut"],
            tour["date_heure_fin"]
        )
        liste_dz_tour.append(d_tour)

    return liste_dz_tour


def deserializing_match(liste_match):
    liste_dz_match = []
    for match in liste_match:
        d_match = Match(
            match["n_match"],
            deserializing_joueur(match["joueur1"]),
            deserializing_joueur(match["joueur2"]),
            match["winner"]
        )
        if match["winner"] == "EGALITE":
            pass
        else:
            d_match.winner = deserializing_joueur(match["winner"])

        liste_dz_match.append(d_match)
    return liste_dz_match


def deserializing_joueur(joueur):
    dz_player = Joueur(
                nom=joueur["nom"],
                family_name=joueur["family_name"],
                rank=joueur["rank"],
                )
    dz_player.sexe = joueur["sexe"]
    dz_player.birthday = joueur["birthday"]

    dz_player.point = joueur["point"]

    return dz_player


def tiny_save(tournoi, liste_tournois):
    # Sauvegarde des joueurs
    tiny_players = serializing_players(tournoi)
    players_table = db.table("players")
    players_table.truncate()
    players_table.insert_multiple(tiny_players)

    # Sauvegarde des tournois
    tiny_tournois = serializing_tournois(liste_tournois)
    tournois_table = db.table("tournois")
    tournois_table.truncate()
    tournois_table.insert_multiple(tiny_tournois)

    return players_table, tournois_table


# Ajout du nombre de joueurs à partir des noms, prénoms et classement attribués aléatoirement.
def auto_joueurs(nb_joueurs):
    joueur_list = []
    for p in range(nb_joueurs):
        # Liste de 100 noms
        nom = j.nom()
        # Liste de 100 prénom
        prenom = j.prenom()
        joueur_list.append(
            Joueur(random.choice(prenom),
                   random.choice(nom),
                   random.randint(800, 1500))
        )
    return joueur_list


# Ajout manuel des joueurs
def manuel_joueur(tournoi):
    joueur = Joueur(input("prenom: "), input("nom: "), input("côte: "))
    tournoi.participants.append(joueur)
    retry = input("Ajouter d'autre joueurs? y/n:  ").lower()
    if retry == "y":
        manuel_joueur(tournoi)
    elif retry == "n":
        pass
    else:
        print("répondez y/n")


def menu():
    tournois = []
    running = True
    while running is True:
        print("""\nMENU PRINCIPAL\n\n1: Créer un tournoi
                \n2: Regarder stats tournoi
                \n3: Sauvegarder/Charger
                \n4: Exit
                \n""")
        choix1 = int(input("Quel choix?: "))

        # Création tournoisfapport
        if choix1 == 1:
            tn = create_new_tournament()
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
                    rapport_tournoi(tournois)
                elif choix2 == 2:
                    rapport_joueur(tournois_choisis)
                elif choix2 == 3:
                    rapport_tours(tournois_choisis)
                elif choix2 == 4:
                    rapport_match(tournois_choisis)
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
                    tiny_save(tournoi, tournois)
            # Chargement des joueurs et tournois
            elif choix2 == 2:
                tournois = []
                for tournoi in db.table("tournois"):
                    dz_tournoi = deserializing_tournoi(tournoi)
                    tournois.append(dz_tournoi)
                print(tournois)
        # Fermeture de l'application
        elif choix1 == 4:
            print("Goodbye ! ")
            running = False


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


def create_new_tournament():
    # 1. Créer un nouveau tournoi.
    tournoi = Tournoi(input("Nom du tournois: "))

    # Ajout manuel?
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
            match_final = Match(n_match, match[0][0], match[0][1], match[1])
            matches.append(match_final)
            n_match += 1
        tour = Tour(
            matches,
            "ROUND {}".format(numero_tour),
            "{}h{}".format(debut[0], debut[1]),
            "{}h{}".format(fin[0], fin[1])
        )

        # 4. Lorsque le tour est terminé j'enregistre le tour dans le tournoi
        tournoi.tournee.append(tour)

    return tournoi


if __name__ == '__main__':
    menu()
