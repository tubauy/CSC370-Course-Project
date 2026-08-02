# seprate file to house mysql-connector setup, called from CLI
import mysql.connector
import os # for .env

#sets up the connection, and prints out error if couldn't connect
def setup():
    with open(".env", "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=")
            os.environ[key.strip()] = value.strip().strip('"').strip("'")


    try:
        connection = mysql.connector.connect(
            host = os.environ["host"],
            port = os.environ["port"],
            user = os.environ["user"],
            password = os.environ["password"],
            database = os.environ["database"]
        )

    except mysql.connector.Error as err:
        print(err)

    else:
        cursor = connection.cursor()




cursor.close()
connection.close()



