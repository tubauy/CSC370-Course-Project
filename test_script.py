import mysql.connector
import os # for .env
from current_build import CurrentBuild
# load all .env variables into os.environ
# TODO: change .env file to localhost for testing purposes
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

new_build = CurrentBuild(connection)

#Insert test script for oracle server here

#new_build.exit_and_save()


connection.close()
