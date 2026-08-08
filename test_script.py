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


#NOTE: for testing purposes, numbers in add_part_test are id values from localhost experimental server
print(new_build.output_compatible("Motherboards"))
print(new_build.output_compatible("CPU"))
print(new_build.output_compatible("RAM"))
print(new_build.output_compatible("1=1"))
print(new_build.output_compatible("GPU"))
print(new_build.output_compatible("Storage"))

print("----")
new_build.add_part_test("Motherboards", 1)
print(new_build.output_compatible("CPU"))
new_build.add_part_test("CPU", 21)
print(new_build.output_compatible("RAM"))
new_build.add_part_test("RAM", 10)
print(new_build.output_compatible("GPU"))
new_build.add_part_test("GPU", 40)
print(new_build.output_compatible("Storage"))
new_build.add_part_test("Storage", 30)

new_build.exit_and_save()


connection.close()
