DEFAULTS = {
    "Motherboards": {
        "name": None, "form_factor": None, "socket_type": None,
        "ddr_version": None, "ram_slots": None,
        "PCIe_1_gen": None, "PCIe_1_slots": None,
        "PCIe_4_gen": None, "PCIe_4_slots": None,
        "PCIe_8_gen": None, "PCIe_8_slots": None,
        "PCIe_16_gen": None, "PCIe_16_slots": None,
        "M_2_slots": None, "SATA_6_ports": None, "SATA_3_ports": None, "U_2_ports": None,
    },
    "RAM": {
        "name": None, "capacity_MB": None,
        "ddr_version": None, "speed_MHz": None,
    },
    "CPU": {
        "name": None, "socket_type": None, "cores": None,
        "clock_speed_MHz": None, "max_ram_capacity_MB": None, "ddr_version": None,
    },
    "Storage": {
        "capacity_GB": None, "storage_type": None, "form_factor": None,
        "interface": None, "cache_MB": None, "nvme": None,
    },
    "GPU": {
        "name": None, "clock_speed_MHz": None, "vram_GB": None,
        "vram_type": None, "PCIe_gen": None, "PCIe_lanes": None,
    },
}

def add_component(cursor, table, data):
    if table not in DEFAULTS:
        raise ValueError(f"Unknown table: {table}")

    template = DEFAULTS[table]
    record = {}

    for key, default_value in template.items():
        if key in data:
            record[key] = data[key]
        else:
            record[key] = default_value

    columns = list(template.keys())
    values = tuple(record[col] for col in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    col_list = ", ".join(columns)

    query = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders});"
    cursor.execute(query, values)