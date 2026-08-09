PART_TYPE_TABLES = {
    "Motherboard": "Motherboards",
    "RAM": "RAM",
    "CPU": "CPUs",
    "Storage": "Storage",
    "GPU": "GPUs",
    "PSU": "PSUs",
}

# shared fields on Components
COMPONENT_DEFAULTS = {
    "name": None,
    "manufacturer": None,
    "price": None,
    "release_date": None,
}

# fields specific to each subtype table
SUBTYPE_DEFAULTS = {
    "Motherboards": {
        "form_factor": None, "socket_type": None,
        "ddr_version": None, "ram_slots": None,
        "PCIe_1_gen": None, "PCIe_1_slots": None,
        "PCIe_4_gen": None, "PCIe_4_slots": None,
        "PCIe_8_gen": None, "PCIe_8_slots": None,
        "PCIe_16_gen": None, "PCIe_16_slots": None,
        "M_2_slots": None, "SATA_6_ports": None,
        "SATA_3_ports": None, "U_2_ports": None,
        "ethernet_speed": None, "WiFi": None,
    },
    "RAM": {
        "capacity_MB": None, "ddr_version": None, "speed_MHz": None,
    },
    "CPUs": {
        "socket_type": None, "cores": None, "clock_speed_MHz": None,
        "max_ram_capacity_MB": None, "ddr_version": None,
    },
    "Storage": {
        "capacity_GB": None, "storage_type": None, "form_factor": None,
        "INTerface": None, "cache_MB": None, "nvme": None,
    },
    "GPUs": {
        "clock_speed_MHz": None, "vram_GB": None, "vram_type": None,
        "PCIe_gen": None, "PCIe_lanes": None,
    },
    "PSUs": {
        "wattage": None, "form_factor": None, "efficiency_rating": None,
        "atx_24_pin": None, "eps_8_pin": None, "pcie_12vhpwr": None,
        "pcie_6_plus_2": None, "sata": None, "molex_4_pin": None,
    },
}

CONFIG_FIELD_TABLES = {
    "motherboard_id": "Motherboards",
    "ram_id": "RAM",
    "cpu_id": "CPUs",
    "storage_id": "Storage",
    "gpu_id": "GPUs",
    "psu_id": "PSUs",
}


def add_component(cnx, part_type, data):
    cursor = cnx.cursor()
    try:
        cnx.start_transaction()

        # check part_type is valid
        if part_type not in PART_TYPE_TABLES:
            raise ValueError(f"Unknown part type: {part_type}")
        table = PART_TYPE_TABLES[part_type]

        # check manufacturer exists
        manufacturer = data.get("manufacturer")
        if manufacturer is not None:
            cursor.execute("SELECT 1 FROM Manufacturers WHERE name = %s;", (manufacturer,))
            if cursor.fetchone() is None:
                raise ValueError(f"Unknown manufacturer: {manufacturer}")

        # add component
        comp_cols = ["part_type"] + list(COMPONENT_DEFAULTS.keys())
        comp_vals = [part_type] + [data.get(c, d) for c, d in COMPONENT_DEFAULTS.items()]
        cursor.execute(
            f"INSERT INTO Components ({', '.join(comp_cols)}) VALUES ({', '.join(['%s'] * len(comp_cols))});",
            comp_vals,
        )

        # get the new component_id
        component_id = cursor.lastrowid

        # add subtype row (e.g. GPUs, CPUs, PSUs...) linked to that component_id
        sub_defaults = SUBTYPE_DEFAULTS[table]
        sub_cols = ["component_id"] + list(sub_defaults.keys())
        sub_vals = [component_id] + [data.get(c, d) for c, d in sub_defaults.items()]
        cursor.execute(
            f"INSERT INTO {table} ({', '.join(sub_cols)}) VALUES ({', '.join(['%s'] * len(sub_cols))});",
            sub_vals,
        )

        cnx.commit()
        return component_id

    except Exception:
        cnx.rollback()
        raise
    finally:
        cursor.close()


def add_configuration(cnx, username, configuration_name, **component_ids):
    cursor = cnx.cursor()
    try:
        cnx.start_transaction()

        # check the user exists
        cursor.execute("SELECT 1 FROM Users WHERE username = %s;", (username,))
        if cursor.fetchone() is None:
            raise ValueError(f"Unknown user: {username}")

        # check each given id exists in its matching subtype table
        for field, comp_id in component_ids.items():
            if comp_id is None:
                continue
            subtype_table = CONFIG_FIELD_TABLES[field]
            cursor.execute(f"SELECT 1 FROM {subtype_table} WHERE component_id = %s;", (comp_id,))
            if cursor.fetchone() is None:
                raise ValueError(f"{field}={comp_id} not found in {subtype_table}")

        # add configuration row (keyed on username and configuration_name)
        cols = ["username", "configuration_name"] + list(CONFIG_FIELD_TABLES.keys())
        vals = [username, configuration_name] + [component_ids.get(f) for f in CONFIG_FIELD_TABLES]
        cursor.execute(
            f"INSERT INTO Configurations ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))});",
            vals,
        )

        cnx.commit()

    except Exception:
        cnx.rollback()
        raise
    finally:
        cursor.close()

def add_manufacturer(cnx, name, country=None, address=None):
    cursor = cnx.cursor()
    try:
        cnx.start_transaction()

        # check manufacturer doesn't already exist
        cursor.execute("SELECT 1 FROM Manufacturers WHERE name = %s;", (name,))
        if cursor.fetchone() is not None:
            raise ValueError(f"Manufacturer already exists: {name}")

        # add manufacturer
        cursor.execute(
            "INSERT INTO Manufacturers (name, country, address) VALUES (%s, %s, %s);",
            (name, country, address),
        )

        cnx.commit()

    except Exception:
        cnx.rollback()
        raise
    finally:
        cursor.close()