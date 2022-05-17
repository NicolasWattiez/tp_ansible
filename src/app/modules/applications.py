import mariadb

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
        cursor = self.__connexion.cursor()
        cursor.execute('SELECT * FROM applications;')
        liste_applications = cursor.fetchall()
        return liste_applications


    def saisie_application(self, liste_donnees = []):
        if liste_donnees:
            liste_donnees = list(liste_donnees)
            nom = input('Quel est le nom de l\'application?('+str(liste_donnees[1])+')' ) or liste_donnees[1] 
            editeur = input('Quel est l editeur de l\'application ?('+str(liste_donnees[2])+')') or liste_donnees[2] 
            version = input('Quel est la version de l\'application?('+str(liste_donnees[3])+')') or liste_donnees[3] 
            ancien_id = liste_donnees[0]
            liste_donnees[0] = nom
            liste_donnees[1] = editeur
            liste_donnees[2] = version
            liste_donnees[3] = ancien_id

        else: 
            nom = input('Quel est le nom de l\'application?')
            editeur = input('Quel est l editeur de l\'application ?') 
            version = input('Quel est la version de l\'application?') 
            liste_donnees.append(nom)
            liste_donnees.append(editeur)
            liste_donnees.append(version)

        return liste_donnees

    # • Permettre l’ajout d’une application
    def ajouterapplication(self, liste_donnees):
        try:
            cursor = self.__connexion.cursor()
            cursor.execute('INSERT INTO applications ( `nom`, `editeur`, `version`)  VALUES (?, ?, ?);',(liste_donnees[0], liste_donnees[1], liste_donnees[2],))
            self.__connexion.commit()
            return 'L\'application a bien été ajoutée'
        except mariadb.Error as e:     
            return f'Erreur lors de la suppression {e} '


    def __trouveruneapplication(self,application):
        cursor = self.__connexion.cursor()
        cursor.execute('SELECT * FROM applications WHERE nom = ?;',(application,))
        application_a_afficher = cursor.fetchone()
        return application_a_afficher

    # Permettre de récupérer les informations d’une application en saisissant son hostname
    def voirapplication(self, application) :
        application_a_afficher = self.__trouveruneapplication(application)
        return application_a_afficher
    
    # Permettre de modifier une application à partir de son hostname
    def modifierapplication(self, nouvelle_donnees):
        try: 
            cursor = self.__connexion.cursor()
            cursor.execute('UPDATE applications SET `nom` = ? , `editeur` = ? ,  `version` = ? WHERE `id` = ?;',(nouvelle_donnees[0], nouvelle_donnees[1], nouvelle_donnees[2], nouvelle_donnees[3],))
            self.__connexion.commit()
            return self.voirapplication(nouvelle_donnees[0])
        except mariadb.Error as e:     
            return f'Erreur lors de la suppression {e} '

    # Permettre de supprimer une application
    def supprimerapplication(self, application):
        try :
            cursor = self.__connexion.cursor()
            cursor.execute('DELETE FROM applications WHERE nom = ?;',(application,))
            self.__connexion.commit()
            return 'La machine a bien été supprimée'
        except mariadb.Error as e:     
            return f'Erreur lors de la suppression {e} '