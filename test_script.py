import mysql.connector
import os # for .env
from current_build import CurrentBuild, SavedBuild
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

new_build = CurrentBuild(connection, config_name = "First_upload")

#Insert test script for oracle server here


print("TESTING SCRATCH BUILD")
#print(new_build.output_compatible("Motherboards"))
#new_build.add_part_test("Motherboards", 1006)
#print("ADDED MB")
#print(new_build.output_compatible("CPUs"))
#new_build.add_part_test("CPUs", 1026)
#print("ADDED CPU")
#print(new_build.output_compatible("RAM"))
#new_build.add_part_test("RAM", 1011)
#new_build.exit_and_save()

connection.close()

print("TESTING SAVED BUILD")
connection = mysql.connector.connect(
    host = os.environ["host"],
    port = os.environ["port"],
    user = os.environ["user"],
    password = os.environ["password"],
    database = os.environ["database"]
)

editing_build = SavedBuild(connection, config_name = "First_upload")
print(editing_build.output_compatible("Motherboards"))
print(editing_build.test_output("Motherboards"))
print(editing_build.output_compatible("GPUs"))
editing_build.add_part_test("GPUs",1041)
#editing_build.add_part_test


#new_build.exit_and_save()
query = (
    "SELECT `Components`.`component_id`, `name` FROM `Motherboards` JOIN `Components` "
    "ON (`Motherboards`.`component_id` = `Components`.`component_id`) LIMIT 10"
)

query2 = (
    "SELECT `socket_type`,`component_id` FROM `Motherboards` WHERE component_id = 1006"
)

query3 = (
    "SELECT `configuration_name` FROM `Configurations`"
)

query4 = (
    "SELECT `name`,`manufacturer` FROM `Components` LIMIT 10"
)

""" connection.start_transaction()
with connection.cursor() as cursor:
    cursor.execute(query3)
    print(cursor.fetchall()) 
    connection.rollback() """

""" connection.start_transaction() """

""" with connection.cursor(dictionary=True, buffered=True) as cursor:
    cursor.execute(query4)
    print(cursor.fetchone()["name"])
connection.rollback() """

connection.close()
