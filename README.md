
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