# TP 6 Ansible

Ce TP a été réalisé dans le cadre de la formation "Ingénieur devops" d'AJC ingénieurie. Le sujet a été réalisé par Vanessa David, Ingénieure DevOps.

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
```
## Création des hôtes

Nous allons utiliser le fichier docker-compose.yml pour créer le master, 2 hôtes ubuntu (1 pour l'application python et 1 pour la base de donnée) et 2 hôtes CentOS (idem)

```
docker-compose up -d
```

## Copier le playbook dans le master01

Dans votre terminal : 
```
docker cp ~/tp_ansible/playbook.yml <id_master01>:/playbook.yml
```
*où <id_master01> est l'id du conteneur master01 que vous pouvez trouver en faisant* 
```
docker container ls
```

## Configuration des hôtes

__1) Récupération des adresses IP :__ nous allons récupérer les IP de chaque hôtes (bien noter le nom qui coresspond à chaque IP) 
```
docker inspect <nom_conteneur> | grep IP 
```
*<nom_conteneur> est le nom donné à chaque hôte (ex: master0A, host01 etc...)*

__2) Connexion au master__

```
docker exec -it master01 sh
```
Vous êtes désormais connecter dans le master01, nous allons maintenant connecter le master01 aux 4 hôtes (ubuntu et CentOS) via ssh 

__3) Connexion en SSH :__ effectuer les commandes ci dessous dans le master01, une par une : (les deux dernières étapes sont là pour s'assurer que la clé ssh ait bien été ajoutée)

```
ssh-keygen
eval "$(ssh-agent)"
ssh-add /root/.ssh/id_rsa
```
*NB: penser à modifier /root/.ssh/id_rsa si vous avez enregistré votre clé ailleurs que dans le chemin par défaut

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

## Créer le fichier /etc/ansible/hosts

Créer le fichier /etc/ansible/hosts qui contiendra :
```
[hostpython]
<nom_host_ubuntu_python> ansible_host=<IP_correspondant>
<nom_host_ceontOS_python> ansible_host=<IP_correspondant>
[hostbdd]
<nom_host_ubuntu_mysql> ansible_host=<IP_correspondant>
<nom_host_ceontOS_mysql> ansible_host=<IP_correspondant>
```
*où <nom_host_ubuntu_python> est le nom d'un des hôtes ubuntu qui acceuillera l'application, <nom_host_ubuntu_mysql> est le nom d'un des hôtes ubuntu qui acceuillera la base de donnée et idem pour CentOS*

## Lancement du playbook

Nous allons maintenant pouvoir lancer notre playbook.yml dans le master01
```
ansible-playbook playbook.yml
```
