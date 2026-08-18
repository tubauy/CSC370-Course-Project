import mysql.connector
import os # for .env
from current_build import CurrentBuild
from cli import Client
from user_login import get_username
#To use the application, run this file

# load all .env variables into os.environ
with open(".env", "r") as file:
    for line in file:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        key, value = line.split("=")
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


connection = mysql.connector.connect(
    host = os.environ["host"],
    port = os.environ["port"],
    user = os.environ["user"],
    password = os.environ["password"],
    database = os.environ["database"]
)

given_username = get_username(connection)
connection.close()

connection2 = mysql.connector.connect(
    host = os.environ["host"],
    port = os.environ["port"],
    user = os.environ["user_api"],
    password = os.environ["password"],
    database = os.environ["database"]
)
client = Client(connection=connection2, username=given_username)
client.start()
#connection.close()
#TODO: MAKE SURE CONNECTION CLOSED
