# Qualite-PGE

Se placer dans ```docker/``` et executer ```./launch.sh``` (en mode admin si user n'appartient pas au groupe docker).

Cliquer sur le lien une fois l'image construite, et se connecter directement sans saisir de mot de passe.

Une fois dans le docker, il y a sur le bureau : ```pge/``` qui contient un clone du repo ```github.com/hakimcherfi/Qualite-PGE```, ```volume_map``` est un dossier partagé entre le conteneur et le dossier de la machine hôte ```volume_map```.

Pour ouvrir l'éditeur vscode dans le dossier de votre choix (creer un dossier pour cela, se placer dedans) : ```code . --user-data-dir='.' --no-sandbox```

Traitement images pour détection de trous et de défaut : de placer dans ```code/```, lancer ```python proto.py```.

Lancement de ROS : à compléter

Développeurs : à la fermeture du conteneur, celui-ci est supprimé, il faut penser à faire un commit avant sa fermeture ou utiliser le volume partagé pour récupérer le travail sur la machine hôte.
