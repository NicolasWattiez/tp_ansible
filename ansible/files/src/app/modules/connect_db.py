import mariadb

class ConnectDb:

    def __init__(self, config):
        self.__user = config['user']
        self.__password = config['password']
        self.__host = config['host']
        self.__port = config['port']
        self.__database = config['database']
    
    def connect(self):
        try:
            conn = mariadb.connect(
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=self.__port,
                database=self.__database
            )
            return conn
        except mariadb.Error as e:
            return f"Error connecting to MariaDB Platform: {e}"
