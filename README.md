# apache_log_parser
Parser des fichiers de log générer par Apache et les restituer dans un fichier JSON ou une base de donnée.

## Objectif 
Créer un script python permettant de parser des fichiers de log générer par Apache et de les restituer dans un fichier JSON ou une base de donnée.

## Enoncé
Le but est d'extraire les connexions d'un fichier de log d'accès et d'indiquer : 
- Le nombre de chaque code retour pour chaque adresse IP
- Le nombre total de requêtes de chaque adresse IP
- La date de la première/dernière requête de chaque adresse IP
- La liste des navigateurs utilisés pour chaque adresse IP
Le résultat devra ensuite être stocké dans un fichier JSON.
