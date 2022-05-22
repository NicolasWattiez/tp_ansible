import os
config = {
    'user' : os.getenv("MARIADB_USER"),
    'password' : os.getenv("MARIADB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': 3306,
    'database': os.getenv("DB_NAME")
}
