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

#new_build.add_part_test("CPU", 16) #hardcoded value for testing only
#print(new_build.output_compatible("RAM"))

#print(new_build.test_output())

#print(new_build.first_pick_test("CPU"))
#print(new_build.output_compatible("Motherboards"))

#new_build.add_part_test("RAM", 13)
#new_build.add_part_test("CPU", 16)
print(new_build.output_compatible("Motherboards"))
print(new_build.output_compatible("CPU"))
print(new_build.output_compatible("RAM"))
print(new_build.output_compatible("1=1"))
#new_build.add_part_test("Motherboards", 13)
new_build.exit_and_save()


connection.close()
# global variables for now
""" motherboard_list = []
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
gpu_list = list(data_tuples) """


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

""" print("List of CPU")
for cpu in cpu_list:
    print(cpu) """

# need type check
#selection = int(input("Type CPU id to select: "))
# May have id's with large numbers due to auto-increment
#id of part may be 7, 8, 12, etc, so should make selection test
#agnostic of specific id that part has, so the user inputs the correct number
#i.e we want user to input 1, 2, 3, etc
""" print(f"You selected CPU {selection}: {cpu_list[selection][1]}")

compatible_motherboards = []

cursor.execute(f"SELECT * FROM `Motherboards` WHERE socket_type = (SELECT socket_type FROM `CPU` WHERE name='{cpu_list[selection][1]}')")
data_tuples = cursor.fetchall()
print(f"Motherboard that's compatible with the {cpu_list[selection][1]}:")
for data_tuple in data_tuples:
    print(data_tuple) """
