# immo-tools

## tests

lancer les tests :

````shell script
pytest
````

avec le coverage :

````shell script
pytest --cov
````

lancer les tests avec nox : (attention, c'est super long !):

````shell scripts
nox -r
````

Permet de lancer les tests sur plusieurs versions de python et de manière isollée.
Nox crée son propre environnement virtuel et y install les dépendances.
L'option ``-r`` permet déviter de recréer tout l'environnement virtuel à chaque fois.

## build & publish

build :

````shell script
poetry build
````


publish sur pypi :

````shell script
poetry publish --build
````

