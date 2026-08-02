import mysql.connector
import os # for .env

CPU = 0
MOBO = 1
RAM = 2
SSD = 3
GPU = 4


class CompatibilityList:
    def __init__(self):
        self.cpu = []
        self.motherboard = []
        self.ram = []
        self.storage = []
        self.gpu = []

class AccumulatedList:
    def __init__(self, initial_data):
        self.cpu = initial_data.cpu.copy()
        self.motherboard = initial_data.motherboard.copy()
        self.ram = initial_data.ram.copy()
        self.storage = initial_data.storage.copy()
        self.gpu = initial_data.gpu.copy()

    def merge(self, new_data):
        self.cpu = set(self.cpu).intersection(new_data.cpu)
        self.motherboard = set(self.motherboard).intersection(new_data.motherboard)
        self.ram = set(self.ram).intersection(new_data.ram)
        self.storage = set(self.storage).intersection(new_data.storage)
        self.gpu = set(self.gpu).intersection(new_data.gpu)

    def print_all(self):
        print("CPUs:")
        for cpu in self.cpu:
            print(cpu)
        print("Motherboards:")
        for motherboard in self.motherboard:
            print(motherboard)
        print("RAM:")
        for ram in self.ram:
            print(ram)
        print("Storage:")
        for storage in self.storage:
            print(storage)
        print("GPU:")
        for gpu in self.gpu:
            print(gpu)



def cpu_path(compat_list, cursor, last_compat_list = None):
    if last_compat_list == None:
        cursor.execute( "SELECT * FROM `CPU`")
        compat_list.cpu = list(cursor.fetchall())
    else:
        compat_list.cpu = last_compat_list.cpu.copy()

    print("Did we reach here?")
    print("List of CPU")
    for index, cpu in enumerate(compat_list.cpu):
        print(f"{index}: {cpu[1]}")

    # need type check
    selection = int(input("Type CPU id to select: "))
    print(f"You selected CPU {selection}: {compat_list.cpu[selection][1]}")
    compat_list.cpu = [compat_list.cpu[selection]] # only the one selected

    cursor.execute(f"SELECT * FROM `Motherboards` WHERE socket_type = (SELECT socket_type FROM `CPU` WHERE name='{compat_list.cpu[0][1]}')")
    compat_list.motherboard = list(cursor.fetchall())
    # print(f"Motherboard that's compatible with the {compat_list.cpu[0][1]}:")
    # for motherboard in compat_list.motherboard:
    #     print(motherboard)

    cursor.execute(f"SELECT * FROM `RAM` WHERE ddr_version = (SELECT ddr_version FROM `CPU` WHERE name='{compat_list.cpu[0][1]}')")
    compat_list.ram = list(cursor.fetchall())
    # print(f"RAM that's compatible with the {compat_list.cpu[0][1]}:")
    # for ram in compat_list.ram:
    #     print(ram)

    cursor.execute(f"SELECT * FROM `Storage`")
    compat_list.storage = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `GPU`")
    compat_list.gpu = list(cursor.fetchall())


def motherboard_path(compat_list, cursor, last_compat_list = None):
    if last_compat_list == None:
        cursor.execute( "SELECT * FROM `Motherboards`")
        compat_list.motherboard = list(cursor.fetchall())
    else:
        compat_list.motherboard = last_compat_list.motherboard.copy()

    print("List of Motherboards")
    for index, motherboard in enumerate(compat_list.motherboard):
        print(f"{index}: {motherboard[1]}")

    # need type check
    selection = int(input("Type Motherboard id to select: "))
    print(f"You selected CPU {selection}: {compat_list.motherboard[selection][1]}")
    compat_list.motherboard = [compat_list.motherboard[selection]] # only the one selected

    cursor.execute(f"SELECT * FROM `CPU` WHERE socket_type = (SELECT socket_type FROM `Motherboards` WHERE name='{compat_list.motherboard[0][1]}')")
    compat_list.cpu = list(cursor.fetchall())
    # print(f"Motherboard that's compatible with the {compat_list.cpu[0][1]}:")
    # for motherboard in compat_list.motherboard:
    #     print(motherboard)

    cursor.execute(f"SELECT * FROM `RAM` WHERE ddr_version = (SELECT ddr_version FROM `Motherboards` WHERE name='{compat_list.motherboard[0][1]}')")
    compat_list.ram = list(cursor.fetchall())
    # print(f"RAM that's compatible with the {compat_list.cpu[0][1]}:")
    # for ram in compat_list.ram:
    #     print(ram)

    cursor.execute(f"SELECT * FROM `Storage`")
    compat_list.storage = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `GPU`")
    compat_list.gpu = list(cursor.fetchall())


# prints out intersection of all selection so far
def print_compatibility_data(accumulated_list: AccumulatedList):

    print("Final compatibility list")
    print("CPUs:")
    for cpu in accumulated_list.cpu:
        print(cpu)
    print("Motherboards:")
    for motherboard in accumulated_list.motherboard:
        print(motherboard)
        
    return


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
    # add one then run function on it
    compat_lists.append(CompatibilityList())
    cpu_path(compat_lists[0], cursor)
    accumulated_list = AccumulatedList(compat_lists[0])

    compat_lists.append(CompatibilityList())
    motherboard_path(compat_lists[1], cursor, last_compat_list=compat_lists[0])
    accumulated_list.merge(compat_lists[1])

    print()
    print("-------------------------")
    print("Final compatibility list")
    print("-------------------------")
    accumulated_list.print_all()


main()
