# Documentation

## Organisation du projet
Il existe dans ce projet deux dossiers : *Analytics* contient ce qu'a été fait comme analyse ad-hoc et autres requètes de test. Le dossier *Servier* est un module Python, celui de la data pipeline créé afin de traiter les PubMed et d'opérer la transformation.

Le module se compose comme suite:
- .
    - /[adr](../adr/main.md)
    - /**config** : la configuration du module sous format YAML. Il est aussi possible de surcharger quqleus parapetre lors de l'instantiation de la class ``` PubMed()```
    - /**data** : on peut y trouver un échantillon de la data il est possible de modifier le path dans le fichier de configuration. Certains fichiers ont été laissé intentionnelement du .gitignore pour demo
    - /**doc** : ici
    - /**helpers** : principalement des fonctions d'aide au traitement ou a la connexion ...Etc
    - /**models** : sous forme de classes. Nous traduisons ici les règles de gestion. Toute la "business logic" doit être mise là
    - **run.py**

## Autre Document
- [Scale Up](./scaleup.md)
- [Ad-Hoc analysis: journals score](../../../../analytics/adhoc_journals_score.ipynb)
- Queries : 
    - [Query 1](../../../../analytics/SQL_samples/query_1.sql)
    - [Query 2](../../../../analytics/SQL_samples/query_2.sql)