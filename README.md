
# Projet Dash


### Installation 

Créez un environnement virtuel et installer le fichier requirements.txt.

Si vous avez besoin de nouvelles librairies, ajoutez les au fichier requirements.txt


### Organisation

__Créez une branche__ de main, pour faire vos modifications.

Pour éviter les problèmes, chacun travaille sur ces fichiers et dans les dossiers spécifiques. 
Nommez avec l'id de votre parti et le nom de votre graph, ex : hover_template_3_circuit.py

Dans /src, il y a 
- /assest   : pour store vos datasets
- /graphs   : pour vos fonctions plot
- hover_template : pour vos hover
- /preprocessing : pour vos fonctions de données 


### App.py

Le fichier app.py sera là où seront rassemblés tous les graphs. Comme vous êtes sur votre branche vous pouvez le modifier.

Il reste à savoir comment on fait le scrollable story. 

### Merge 

Avant de merge, pour ne pas avoir de conflit sur le fichier App.py, renomez le.

Si vous avez bien suivi les consignes précédentes, il ne devrait pas y avoir de problèmes. 

Pour merge : allez sur la branch main ( git checkout main) puis (git merge votre_branch)


### Deploy

Ajouter Procfile et requirements.txt dans la racine du git
Python version --> 3.11.3
Numpy wheel --> numpy-1.26.3-cp311-cp311-win_amd64.whl   (mettre numpy==1.26.3 dans requirements.txt)
Pandas wheel --> pandas-2.1.0-cp311-cp311-win_amd64.whl (mettre pandas==2.1.0)
Fastf1 --> 3.2.0
dash --> 2.16.1
Ajouter des fichiers vides __init__.py dans les dossiers.

Attention aux importations :
    toujours partir de src, ex dans app.py : 
        
        from .preprocessing.preprocessing_3 import get_data, get_max_speed

        path_max = os.path.join("src","assets", "data", "telemetry_spain_2021_VER.csv")

Vous pouvez toujours travailler nomalement sur le main. Lorsque vous push, cela va build à nouveau 


Attention ! nouvelle commande pour lancer localement : python -m src.server


Site : 
https://dash-equipe-15-320e9a161b3c.herokuapp.com/