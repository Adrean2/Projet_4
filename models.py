import random
import ast
import json
from tinydb import TinyDB


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

# Création base de donnée tinydb
db = TinyDB("db.json")


# Conversions pour compatibilité tinydb (sauvegarde)
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

