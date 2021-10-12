import csv
from pathlib import Path

absolute_path = Path(__file__).absolute().parent


def prenom():
    prenom_list = []
    with open(absolute_path/"prenom.csv", mode="r") as prenoms:
        reader = csv.reader(prenoms, delimiter=",")
        for prenom in reader:
            for p in prenom:
                prenom_list.append(p)
    return prenom_list


def nom():
    noms_list = []
    with open(absolute_path/"patronymes.csv", mode="r") as prenoms:
        reader = csv.reader(prenoms, delimiter=",")
        for patronymes in reader:
            for p in patronymes:
                noms_list.append(p)
    return noms_list
