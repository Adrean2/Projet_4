# OCR_Projet_4
## Description
Il s'agit du projet numéro 4 du parcours *Développeur d'application Python* d'OpenClassrooms

## Utilisation de l'application
#### L'application se base sur un menu affiché dans votre terminal.
![menu](https://puu.sh/IhMQr/d9ae47010a.png)
<br/>Il faudra ensuite renseigner les informations souhaitées en fonction de ce que le programme vous demande.
<br/>Par exemple la **création d'un tournoi** :
<br/>![réponses](https://puu.sh/IhMQK/5a24ace1c6.png)

#### Rapports des tournois
Les rapports sont accessibles une fois un tournoi créé.
Il faudra utiliser l'index qui a été attribué aux tournois pour que le rapport fonctionne.<br/>
Par exemple un rapport de match se fera comme ceci :
<br/>
![rapport_match](https://puu.sh/IhNaV/36aa1624b1.png)

## joueurs.py
Il s'agit d'un module qui permet de traiter les fichiers csv patronymes et prenom

## Patronymes et Prenom
Il s'agit des ressources csv que j'ai utilisé pour générer aléatoirement des noms et prénoms parmis les plus répandus.
<br/>Basées puis modifiées d'après [data.gouv.fr](https://www.data.gouv.fr/en/datasets/liste-de-prenoms-et-patronymes/)

## Flake8
Pour vérifier que le programme était conforme aux réglementations PEP8, j'ai utilisé flake8 de la manière suivante:
#### D'abord en l'installant
```shell
pip install flake8
pip install flake8-html
```
#### Puis en générant des rapports
```shell
flake8 .\main.py .\joueurs.py --format=html --htmldir=flake-report --max-line-length 119
```
<br/> Dans mon cas, le rapport est exempt d'erreurs !
![rapport-flake8](https://puu.sh/IhNgi/4d0227c665.png)

## Requirements
tinydb version 4.5.2 https://tinydb.readthedocs.io/
flake8 version 3.9.2 https://flake8.pycqa.org/
flake8-html version 0.4.1 https://pypi.org/project/flake8-html/
