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

print(new_build.output_compatible("Motherboards"))
new_build.add_part_test("Motherboards", 1006)
print(new_build.output_compatible("CPUs"))
#new_build.exit_and_save()
query = (
    "SELECT `Components`.`component_id`, `name` FROM `Motherboards` JOIN `Components` "
    "ON (`Motherboards`.`component_id` = `Components`.`component_id`) LIMIT 10"
)

query2 = (
    "SELECT socket_type FROM `Motherboards` WHERE component_id = 1006"
)

query3 = (
    "SELECT socket_type FROM `CPUs`"
)

""" connection.start_transaction()
with connection.cursor() as cursor:
    cursor.execute(query3)
    print(cursor.fetchall()) 
    connection.rollback() """

connection.close()
