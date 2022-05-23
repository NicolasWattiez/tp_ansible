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
docker cp . <name_master>:/etc/ansible/
```
Ici, `<name_master>` correspond simplement à "master".


## Configuration des hôtes

__1) Récupération des adresses IP :__ nous allons récupérer les IP de chaque hôtes (bien noter le nom qui coresspond à chaque IP) 
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

__4) Copie de la clé sur les machines hôtes :__  il vous faudra effectuer les commandes suivantes une par une en utilisant les adresses IP récupérées a l'étape 1 : (le mot de passe du root est *toor*)

```
ssh-copy-id root@<IPmachinehost1> 
ssh-copy-id root@<IPmachinehost2> 
ssh-copy-id root@<IPmachinehost3>
ssh-copy-id root@<IPmachinehost4>
```

__5) Connexion aux hôtes :__ nous allons nous connecter aux hôtes pour vérfier que la clé ssh est bien été copiée sur chacun des hôtes

```
ssh root@<IPmachinehost1>
ssh root@<IPmachinehost2>
ssh root@<IPmachinehost3>
ssh root@<IPmachinehost4>
```

## Lancement du playbook

Nous allons maintenant pouvoir lancer notre playbook dans le master pour la configuration de la base de donnée sur ubuntu
```
cd etc
cd ansible 
ansible-playbook config-dbserver.yml 
```
(ou bien config-appserver.yml(pour l'app sur ubuntu), config-dbcentos.yml(pour la base de donnée centos) selon la configuration que vous soufaitez faire)
