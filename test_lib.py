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


def cpu_path(compat_list, cursor, accumulated_list: AccumulatedList = None):
    if accumulated_list == None:
        cursor.execute( "SELECT * FROM `CPU`")
        compat_list.cpu = list(cursor.fetchall())
    else:
        compat_list.cpu = list(accumulated_list.cpu)

    print("List of CPU")
    for index, cpu in enumerate(compat_list.cpu):
        print(f"{index}: {cpu[1]}")

    # need type check
    selection = int(input("Type CPU id to select: "))
    print(f"You selected CPU {selection}: {compat_list.cpu[selection][1]}")
    compat_list.cpu = [compat_list.cpu[selection]] # only the one selected

    cursor.execute(f"SELECT * FROM `Motherboards` WHERE socket_type = (SELECT socket_type FROM `CPU` WHERE name='{compat_list.cpu[0][1]}')")
    compat_list.motherboard = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `RAM` WHERE ddr_version = (SELECT ddr_version FROM `CPU` WHERE name='{compat_list.cpu[0][1]}')")
    compat_list.ram = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `Storage`")
    compat_list.storage = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `GPU`")
    compat_list.gpu = list(cursor.fetchall())


def motherboard_path(compat_list, cursor, accumulated_list: AccumulatedList = None):
    if accumulated_list == None:
        cursor.execute( "SELECT * FROM `Motherboards`")
        compat_list.motherboard = list(cursor.fetchall())
    else:
        compat_list.motherboard = list(accumulated_list.motherboard)

    print("List of Motherboards")
    for index, motherboard in enumerate(compat_list.motherboard):
        print(f"{index}: {motherboard[1]}")

    # need type check
    selection = int(input("Type Motherboard id to select: "))
    print(f"You selected Motherboard {selection}: {compat_list.motherboard[selection][1]}")
    compat_list.motherboard = [compat_list.motherboard[selection]] # only the one selected

    cursor.execute(f"SELECT * FROM `CPU` WHERE socket_type = (SELECT socket_type FROM `Motherboards` WHERE name='{compat_list.motherboard[0][1]}')")
    compat_list.cpu = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `RAM` WHERE ddr_version = (SELECT ddr_version FROM `Motherboards` WHERE name='{compat_list.motherboard[0][1]}')")
    compat_list.ram = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `Storage`")
    compat_list.storage = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `GPU`")
    compat_list.gpu = list(cursor.fetchall())


def ram_path(compat_list, cursor, accumulated_list: AccumulatedList = None):
    if accumulated_list == None:
        cursor.execute( "SELECT * FROM `RAM`")
        compat_list.ram = list(cursor.fetchall())
    else:
        compat_list.ram = list(accumulated_list.ram)

    print("List of RAM")
    for index, ram in enumerate(compat_list.ram):
        print(f"{index}: {ram[1]}")

    # need type check
    selection = int(input("Type RAM id to select: "))
    print(f"You selected RAM {selection}: {compat_list.ram[selection][1]}")
    compat_list.ram = [compat_list.ram[selection]] # only the one selected

    cursor.execute(f"SELECT * FROM `Motherboards` WHERE socket_type = (SELECT socket_type FROM `RAM` WHERE name='{compat_list.ram[0][1]}')")
    compat_list.motherboard = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `CPU` WHERE ddr_version = (SELECT ddr_version FROM `RAM` WHERE name='{compat_list.ram[0][1]}')")
    compat_list.cpu = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `Storage`")
    compat_list.storage = list(cursor.fetchall())

    cursor.execute(f"SELECT * FROM `GPU`")
    compat_list.gpu = list(cursor.fetchall())
