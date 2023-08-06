# immo tools lib

## installation

avec pip :
````shell script
pip install immo-tools-lib
````

avec poetry :
````shell script
poetry add immo-tools-lib
````

## usage

````python
from immo_tools import calculator

duration = 300
amount = 250000
year_rate = 1.5
insurance_rate = .26

loan = calculator.build_loan(
    duration, 
    amount, 
    year_rate, 
    insurance_rate, 
    build_summary=True, 
    duration_unit='month')

# Tableau d'amoritssement :
loan.summary

# montant total des intérêts payés :
loan.get_interests()

# mensualités sans assurance :
loan.get_monthly()

# Coût de l'emprunt au bout de 10 ans :
loan.get_cost(10)
````

## développement

### tests

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

### build & publish

build :

````shell script
poetry build
````


publish sur pypi :

````shell script
poetry publish --build
````

