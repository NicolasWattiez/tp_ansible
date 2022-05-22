class Application:

    def __init__(self, connexion) -> None:
        # Propriété de l'objet application
        self.__nom = ''
        self.__editeur = ''
        self.__version = "22.04"
        self.__connexion = connexion


    def get_nom(self):
        return self.__nom

    def set_nom(self, nom):
        if isinstance(nom, str): 
            self.__nom = nom

    def get_editeur(self):
        return self.__editeur

    def set_editeur(self, editeur):
        if isinstance(editeur, str): 
            self.__editeur = editeur

    def get_version(self):
        return self.__version

    def set_version(self, version):
        if isinstance(version, str): 
            self.__version = version

    # Lister des applications informatiques avec les caractéristiques suivantes : 
    def listeapplications(self):
        # fichier = open('./applications.txt','r')
        # liste_applications = fichier.readlines()
        # fichier.close()
        cursor = self.__connexion.cursor()
        resultat = cursor.execute('SELECT * FROM machines;')
        liste_applications = cursor.fetchall()
        return liste_applications

    # Méthode pour transformer les propriétés de l'objet en chaine de caractère pour lire/erire dans le fichier texte
    def __totexteformat(self, liste_donnees):
        texte = ''
        compteur = 0
        while compteur < len(liste_donnees):
            texte += str(liste_donnees[compteur])
            if compteur < (len(liste_donnees)-1):
                texte += ','      
            compteur += 1
        return texte

    def saisie_application(self):
        liste_donnees = []
        nom = input('Quel est le nom de l\'application?')
        liste_donnees.append(nom)
        editeur = input('Quel est l editeur de l\'application ?')
        liste_donnees.append(editeur)
        version = input('Quel est la version de l\'application?')
        liste_donnees.append(version)
        return liste_donnees

    # • Permettre l’ajout d’une application
    def ajouterapplication(self, dictionnaire):
        application = '\n' + self.__totexteformat(dictionnaire)
        fichier = open('./applications.txt','a')
        fichier.write(application)
        fichier.close()
        return application + 'L\'application a bien été ajoutée'


    def __trouveruneapplication(self,hostname):
        liste_application = self.listeapplications()
        application_a_afficher = ''
        for application in liste_application:
            application_split = application.split(',')
            if application_split[0] == hostname:
                application_a_afficher = self.__totexteformat(application_split)
        return application_a_afficher

    # Permettre de récupérer les informations d’une application en saisissant son hostname
    def voirapplication(self, hostname) :
        application_a_afficher = self.__trouveruneapplication(hostname)
        return application_a_afficher
    
    # Permettre de modifier une application à partir de son hostname
    def modifierapplication(self, application, nouvelle_donnees):
        self.supprimerapplication(application)
        self.ajouterapplication(nouvelle_donnees)
        return self.voirapplication(application)

    # Permettre de supprimer une application
    def supprimerapplication(self, hostname):
        application_a_supprimer = self.__trouveruneapplication(hostname)
        liste_applications = self.listeapplications()
        for application in liste_applications:
            if application_a_supprimer ==  application:
                liste_applications.remove(application_a_supprimer)
        fichier = open('./applications.txt','w')
        fichier.writelines(liste_applications)
        fichier.close()
        return 'L\'application a bien été supprimée'import mariadb

class Machine:

    def __init__(self, application, connexion) -> None:
        # Propriété de l'objet machine
        self.__nom = ''
        self.__IP = ''
        self.__nombre_cpu = 1
        self.__taille_ram = '1Go'
        self.__disque  = ['10Go']
        self.__OS = 'Linux-Ubuntu'
        self.__version_os = "22.04"
        self.__application = application
        self.__liste_application = application.listeapplications()
        self.__connexion = connexion

    def get_nom(self):
        return self.__nom

    def set_nom(self, nom):
        if isinstance(nom, str): 
            self.__nom = nom

    def get_IP(self):
        return self.__IP

    def set_IP(self, IP):
        if isinstance(IP, str): 
            self.__IP = IP

    def get_nombre_cpu(self):
        return self.__nombre_cpu

    def set_nombre_cpu(self, nombre_cpu):
        if isinstance(nombre_cpu, int): 
            self.__nombre_cpu = nombre_cpu

    def get_taille_ram(self):
        return self.__taille_ram

    def set_taille_ram(self, taille_ram):
        if isinstance(taille_ram, str): 
            self.__taille_ram = taille_ram

    def get_disque(self):
        return self.__disque

    def set_disque(self, disque):
        if isinstance(disque, list): 
            self.__disque = disque

    def get_OS(self):
        return self.__OS

    def set_OS(self, OS):
        if isinstance(OS, str): 
            self.__OS = OS

    def get_version_os(self):
        return self.__version_os

    def set_version_os(self, version_os):
        if isinstance(version_os, str): 
            self.__version_os = version_os

    def get_liste_application(self):
        return self.__liste_application

    def set_liste_application(self, liste_application):
        if isinstance(liste_application, list):
            self.__liste_application = liste_application

    # Lister des machines informatiques avec les caractéristiques suivantes : 
    def listeMachines(self):
        # fichier = open('./machines.txt','r')
        # liste_machines = fichier.readlines()
        # fichier.close()
        cursor = self.__connexion.cursor()
        resultat = cursor.execute('SELECT * FROM machines')
        liste_machines =  cursor.fetchall()
        machine_liste = [] 
        for machine in liste_machines :
            cursor.execute('SELECT * FROM disques WHERE machine_id = ? ;', (machine[0],))
            nouvelle_machine = machine + tuple(cursor.fetchall())
            machine_liste.append(nouvelle_machine)

        return machine_liste

    # Méthode pour transformer les propriétés de l'objet en chaine de caractère pour lire/erire dans le fichier texte
    # def __totexteformat(self, liste_donnees):
    #     texte = ''
    #     compteur = 0
    #     while compteur < len(liste_donnees):
    #         texte += str(liste_donnees[compteur])
    #         if compteur < (len(liste_donnees)-1):
    #             texte += ','      
    #         compteur += 1
    #     return texte

    def saisie_disque(self):
        disques =[]
        autre_disque = 'O' 
        while autre_disque == 'O':
            disque = []
            nom_disque = input('Quel est le nom du disque?')
            taille_disque = input('Quel est la taille du disque')
            disque.append(nom_disque)
            disque.append(taille_disque)
            disques = [] 
            autre_disque = input('Voulez-vous ajouter un autre disque ? (O ou N)')
            disques.append(disque)
        return disques 

    def saisie_machine(self):
        liste_donnees = []
        hostname = input('Quel est le hostname de la machine?')
        liste_donnees.append(hostname)
        IP = input('Quel est l adresse IP de la machine ?')
        liste_donnees.append(IP)
        CPU = int(input('Quel est le nombre de CPU ?'))
        liste_donnees.append(CPU)
        RAM = input('Quel est la taille de la RAM ?')
        liste_donnees.append(RAM)
        OS = input('Quel est le système d exploitaiton?') 
        liste_donnees.append(OS)
        version = input('Quel est la version du système d exploitation?')
        liste_donnees.append(version)
        liste_donnees.append(self.saisie_disque())
        liste_application = input('Quel est la liste des applications installée ?')
        liste_donnees.append(liste_application)
        return liste_donnees

    # • Permettre l’ajout d’une machine
    def ajouterMachine(self, liste_donnees):
        # machine = '\n' + self.__totexteformat(dictionnaire)
        # fichier = open('./machines.txt','a')
        # fichier.write(machine)
        # fichier.close()
        cursor = self.__connexion.cursor()
        cursor.execute('INSERT INTO machines ( `nom`, `ip`, `nombre_cpu`, `taille_ram`, `os`, `version`)  VALUES (?, ?, ?, ?, ?, ?);',(liste_donnees[0], liste_donnees[1], liste_donnees[2], liste_donnees[3], liste_donnees[4], liste_donnees[5],))
        id_machine = cursor.lastrowid
        disques = liste_donnees[6]
        for disque in disques:
            cursor.execute('INSERT INTO `disques` (`nom`, `taille`, `machine_id`)  VALUES (?, ?, ?);',(disque[0], disque[1], id_machine, ))
            self.__connexion.commit()
        return 'La machine a bien été ajoutée'


    def __trouverunemachine(self,hostname):
        # liste_machine = self.listeMachines()
        # machine_a_afficher = ''
        # for machine in liste_machine:
        #     machine_split = machine.split(',')
        #     if machine_split[0] == hostname:
        #         machine_a_afficher = self.__totexteformat(machine_split)
        cursor = self.__connexion.cursor()
        cursor.execute('SELECT * FROM machines WHERE nom = ?;',(hostname,))
        machine_a_afficher = cursor.fetchone()
        cursor.execute('SELECT * FROM disques WHERE machine_id = ? ;', (machine_a_afficher[0],))
        machine_a_afficher = machine_a_afficher + tuple(cursor.fetchall())
        return machine_a_afficher

    # Permettre de récupérer les informations d’une machine en saisissant son hostname
    def voirMachine(self, hostname) :
        machine_a_afficher = self.__trouverunemachine(hostname)
        return machine_a_afficher
    
    # Permettre de modifier une machine à partir de son hostname
    def modifierMachine(self, machine, nouvelle_donnees):
        self.supprimerMachine(machine)
        self.ajouterMachine(nouvelle_donnees)
        return self.voirMachine(machine)

    # Permettre de supprimer une machine
    def supprimerMachine(self, hostname):
        # machine_a_supprimer = self.__trouverunemachine(hostname)
        # liste_machines = self.listeMachines()
        # for machine in liste_machines:
        #     if machine_a_supprimer ==  machine:
        #         liste_machines.remove(machine_a_supprimer)
        # fichier = open('./machines.txt','w')
        # fichier.writelines(liste_machines)
        # fichier.close()
        try :
            cursor = self.__connexion.cursor()
            cursor.execute('SELECT id FROM machines WHERE nom = ? ',(hostname,))
            id_machine = cursor.fetchone()
            cursor.execute('DELETE FROM disques WHERE machine_id = ?',(id_machine[0] ,))
            cursor.execute('DELETE FROM machines WHERE nom = ?;',(hostname,))
            self.__connexion.commit()
            return 'La machine a bien été supprimée'
        except mariadb.Error as e:     
            return f'Erreur lors de la suppression {e} '