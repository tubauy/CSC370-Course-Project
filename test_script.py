import mysql.connector
import os # for .env
from test_lib import *


def main():
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

    compat_lists = []

    # Can do this in any order
    # add one empty list to compat_lists then run function on it
    compat_lists.append(CompatibilityList())
    cpu_path(compat_lists[0], cursor)
    accumulated_list = AccumulatedList(compat_lists[0])

    compat_lists.append(CompatibilityList())
    motherboard_path(compat_lists[1], cursor, accumulated_list)
    accumulated_list.merge(compat_lists[1])

    compat_lists.append(CompatibilityList())
    ram_path(compat_lists[2], cursor, accumulated_list)
    accumulated_list.merge(compat_lists[2])

    print()
    print("-------------------------")
    print("Final compatibility list")
    print("-------------------------")
    accumulated_list.print_all()


main()
