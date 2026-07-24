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

# global variables for now
motherboard_list = []
cpu_list= []
ram_list= []
storage_list = []
gpu_list= []

cursor = connection.cursor()

cursor.execute( "SELECT * FROM `Motherboards`")
data_tuples = cursor.fetchall()
motherboard_list = list(data_tuples)

cursor.execute( "SELECT * FROM `CPU`")
data_tuples = cursor.fetchall()
cpu_list = list(data_tuples)

cursor.execute( "SELECT * FROM `RAM`")
data_tuples = cursor.fetchall()
ram_list = list(data_tuples)

cursor.execute( "SELECT * FROM `Storage`")
data_tuples = cursor.fetchall()
storage_list = list(data_tuples)

cursor.execute( "SELECT * FROM `GPU`")
data_tuples = cursor.fetchall()
gpu_list = list(data_tuples)


# cursor.execute( "SELECT * FROM `Motherboards` WHERE socket_type = (SELECT socket_type FROM `CPU` WHERE name='AMD Ryzen 5 7600')")
# data_tuples = cursor.fetchall()
# print("Motherboard that's compatible with the Ryzen 5 7600:")
# for data_tuple in data_tuples:
#     print(data_tuple)
#
#
# cursor.execute( "SELECT * FROM `RAM` WHERE ddr_version = (SELECT ddr_version FROM `CPU` WHERE name='AMD Ryzen 5 7600')")
# data_tuples = cursor.fetchall()
# print("RAM that's compatible with the Ryzen 5 7600:")
# for data_tuple in data_tuples:
#     print(data_tuple)

print("List of CPU")
for cpu in cpu_list:
    print(cpu)

# need type check
selection = int(input("Type CPU id to select: "))
print(f"You selected CPU {selection}: {cpu_list[selection][1]}")

compatible_motherboards = []

cursor.execute(f"SELECT * FROM `Motherboards` WHERE socket_type = (SELECT socket_type FROM `CPU` WHERE name='{cpu_list[selection][1]}')")
data_tuples = cursor.fetchall()
print(f"Motherboard that's compatible with the {cpu_list[selection][1]}:")
for data_tuple in data_tuples:
    print(data_tuple)
