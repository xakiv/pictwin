# pictwin

Projet de fin d’année - DUT ANALYSE & PROGRAMMATION (2015-2016)

> Je tiens à remercier Thomas VUARCHEX pour son aimable autorisation à utiliser sa création comme
> élément de travail pour ce projet de fin d'année.
> La finalité de se projet est la mise en œuvre quelques possibilités de traitement d'image pour
> résoudre un casse-tête. Ça sera ainsi l’occasion de voir comment une image est représentée
> numériquement et comment, par cette représentation, on peut appliquer des traitements : conversion
> colorimétrique, sélection d’une région de l’image, comparaison de textures pour en déterminer les
> similitudes et détection de zones d'intérêt.


La finalité de ce _répo_ est de garder une trace d'un premier projet en Python.

## Installation

Télécharger les sources dans son répertoire de travail.
```
cd /working_directory
git clone https://gitlab.com/ChBnh/pictwin.git
```

Initialiser et activer un environnement virtuel en Python3 puis installer les dépendances dans le venv nouvellement créé.
```
cd /working_directory
python3 -m venv venv
source venv/bin/activate
pip install -r /pictwin/requirements.txt
```

Lancer le script et suivre les instructions sur le terminal.
```
cd /working_directory
source venv/bin/activate
cd /working_directory/pictwin
python main.py
```
