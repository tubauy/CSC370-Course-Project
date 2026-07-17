import mysql.connector
import os # for .env

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

cursor = connection.cursor()

query = "SELECT * FROM `Motherboards`"
cursor.execute(query)
data_tuples = cursor.fetchall()

print("Motherboards data:")
for data_tuple in data_tuples:
    print(data_tuple)

query = "SELECT * FROM `CPU`"
cursor.execute(query)
data_tuples = cursor.fetchall()

print("CPU data:")
for data_tuple in data_tuples:
    print(data_tuple)


query = "SELECT * FROM `Motherboards` WHERE socket = (SELECT socket FROM `CPU` WHERE name='AMD Ryzen 5 7600')"
cursor.execute(query)
data_tuples = cursor.fetchall()

print("Motherboard that's compatible with the Ryzen 5 7600:")
for data_tuple in data_tuples:
    print(data_tuple)



query = "SELECT * FROM `Motherboards` WHERE socket = (SELECT socket FROM `CPU` WHERE name='AMD Ryzen 5 5500')"
cursor.execute(query)
data_tuples = cursor.fetchall()

print("Motherboard that's compatible with the Ryzen 5 5500:")
for data_tuple in data_tuples:
    print(data_tuple)
