# TP 6 Ansible

Ce TP a été réalisé dans le cadre de la formation "Ingénieur devops" d'AJC ingénieurie. Le sujet a été réalisé par Vanessa David, Ingénieure DevOps.

L’application est un outil pour le suivi du parc informatique de l’entreprise.

L’application permet de stocker des données concernant les machines du parc informatiques dans une base mysql.
L’utilisateur peut réaliser des actions sur cette base de donnée telle que :
- Lister les machines avec l’ensemble de leurs informations
- Voir une machine à partir de son nom
- Modifier une machine
- Supprimer une machine
- Ajouter une machine

Les fichiers docker-compose, playbook.yaml et Jenkinsfile rédigé dans ce TP ont pour but de permettre la mise en place d'un déploiement continu.

## Pré-requis 

Il est nécessaire d'avoir installer les outils ci-dessous 
- Docker
- Jenkins

Dans un second temps il vous faudra récupérer le dossier git qui se trouve à l'adresse suivante : https://github.com/NicolasWattiez/tp_ansible

Pour le cloner sur votre machine, ouvrir un terminal et effectuer la commande suivante :
```
git clone https://github.com/NicolasWattiez/tp_ansible
```
Il faudra se placer sur la branche jenkins après s'être placé dans le dossier tp_ansible
```
git checkout jenkins
``` 
## Se place dans le dossier de travail

Se déplacer dans le dossier de travail 
```
cd tp_ansible
cd ansible
```
## Création des hôtes

Nous allons utiliser le fichier docker-compose.yml pour créer le master, 2 hôtes ubuntu (1 pour l'application python et 1 pour la base de donnée) et 2 hôtes CentOS (idem)

```
docker-compose up -d
```

## Copier les fichier du dossier ansible dans le master

Dans votre terminal : 
```
docker cp . master:/etc/ansible/
```
Revenez au dossier parent puis copier le Jenkinsfile dans le conteneur jenkins
```
cd ..
docker cp Jenkinsfile jenkins:/home
```

## Configuration des hôtes

__1) Récupération des adresses IP (facultatif) :__ nous allons récupérer les IP de chaque hôtes (bien noter le nom qui coresspond à chaque IP) 
```
docker inspect <nom_conteneur> | grep IP 
```
*<nom_conteneur> est le nom donné à chaque hôte (ex: master, appubuntu, appcentos, dbubuntu, dbcentos)*

__2) Connexion au master__

```
docker exec -it master sh
```
Vous êtes désormais connecté dans le master, nous allons maintenant connecter le master aux 4 hôtes (ubuntu et CentOS) via ssh 

__3) Connexion en SSH :__ effectuer les commandes ci-dessous dans le master, une par une : (les deux dernières étapes sont là pour s'assurer que la clé ssh ait bien été ajoutée)

```
ssh-keygen
eval "$(ssh-agent)"
ssh-add /root/.ssh/id_rsa
```
*NB: penser à modifier /root/.ssh/id_rsa si vous avez enregistré votre clé ailleurs que dans le chemin par défaut*

__4) Copie de la clé sur les machines hôtes :__  il vous faudra effectuer les commandes suivantes une par une en utilisant les adresses IP récupérées a l'étape 1 à la place du nom machine ou bien utiliser directement les commandes suivantes (le mot de passe du root est *toor*)

```
ssh-copy-id root@dbubuntu 
ssh-copy-id root@dbcentos 
ssh-copy-id root@appubuntu
ssh-copy-id root@appcentos
```

__5) Connexion aux hôtes :__ nous allons nous connecter aux hôtes pour vérfier que la clé ssh est bien été copiée sur chacun des hôtes (une fois connecté, il faut penser à faire "exit" pour revenir dans le master et lancer une nouvelle connexion ssh )

```
ssh root@dbubuntu
exit
ssh root@dbcentos
exit
ssh root@appubuntu
exit
ssh root@appcentos
exit
```
On se déconnecte maintenant du conteneur master
```
exit
```

## Connexion au conteneur master depuis le conteneur jenkins
Nous allons nous connecter au conteneur master depuis le conteneur jenkins pour pouvoir par la suite lancer nos playbook via le Jenkinsfile

``` 
docker exec -it jenkins sh
ssh-keygen
eval "$(ssh-agent)"
ssh-add /root/.ssh/id_rsa
ssh-copy-id root@master
ssh root@master
exit
```

## Connexion a Jenkins
Ouvre jenkins dans un onglet de votre navigateur en tapant localhost:8098
COnfigurez le si nécessaire en respectant les étapes indiqués sur Jenkins. 

Une fois sur Jenkins :

1) Se rendre sur Manage Jenkins
2) Se rendre dans Global Tool Configuration 
3) Ajouter un Gradle en lui donnant le nom 'gradle'
4) Save
5) Créer un projet pipeline et donné lui un nom 
6) Dans Pipeline définition choisir Pipeline Script from SCM
7) Choisir git
8) ChoisCOpier l'url suivant dans la case correspondante :https://github.com/NicolasWattiez/tp_ansible
9) Dans branch to build saisir : */jenkins
10) Save 
11) Lancer le Build Now

## Lancement du playbook (étape facultatif si on ne se sert pas de Jenkinsfile pour lancer nos playbooks)

Nous allons maintenant pouvoir lancer notre playbook dans le master pour la configuration de la base de donnée sur ubuntu
```
cd etc
cd ansible 
ansible-playbook config-dbserver.yml 
```
(ou bien config-appserver.yml(pour l'app sur ubuntu), config-dbcentos.yml(pour la base de donnée centos) selon la configuration que vous soufaitez faire)
