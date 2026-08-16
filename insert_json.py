from db_add import *
import json
import sys
import os
import mysql.connector



def parse_common_fields(data):
    """Fields shared by every part type — lives on Components."""
    metadata = data.get("metadata", {})
    release_year = metadata.get("releaseYear")
    return {
        "name": metadata.get("name"),
        "manufacturer": metadata.get("manufacturer"),
        "release_date": f"{release_year}-01-01" if release_year else None,
    }


def parse_ddr_version(ram_type):
    """'DDR5' -> 5, None -> None"""
    if not ram_type:
        return None
    digits = "".join(ch for ch in ram_type if ch.isdigit())
    return int(digits) if digits else None


def parse_cpu_json(data):
    socket_type = data.get("socket")
    cores = data.get("cores", {}).get("total")

    base_clock_ghz = data.get("clocks", {}).get("performance", {}).get("base")
    clock_speed_MHz = int(base_clock_ghz * 1000) if base_clock_ghz else None

    memory = data.get("specifications", {}).get("memory", {})
    max_ram_capacity_GB = memory.get("maxSupport")
    max_ram_capacity_MB = int(max_ram_capacity_GB * 1024) if max_ram_capacity_GB else None

    types = memory.get("types", [])
    ddr_version = parse_ddr_version(types[0] if types else None)

    return {
        "socket_type": socket_type,
        "cores": cores,
        "clock_speed_MHz": clock_speed_MHz,
        "max_ram_capacity_MB": max_ram_capacity_MB,
        "ddr_version": ddr_version,
    }


def parse_ram_json(data):
    capacity_GB = data.get("capacity")
    capacity_MB = int(capacity_GB * 1024) if capacity_GB else None

    return {
        "capacity_MB": capacity_MB,
        "ddr_version": parse_ddr_version(data.get("ram_type")),
        "speed_MHz": data.get("speed"),
    }


def parse_motherboard_json(data):
    memory = data.get("memory", {})
    storage_devices = data.get("storage_devices", {})

    # find the x16 PCIe slot entry (lanes == 16)
    pcie_16_gen, pcie_16_slots = None, None
    for slot in data.get("pcie_slots", []):
        if slot.get("lanes") == 16:
            pcie_16_gen = float(slot["gen"]) if slot.get("gen") else None
            pcie_16_slots = slot.get("quantity")
            break

    onboard_ethernet = data.get("onboard_ethernet", [])
    ethernet_speed = onboard_ethernet[0].get("speed") if onboard_ethernet else None

    return {
        "form_factor": data.get("form_factor"),
        "socket_type": data.get("socket"),
        "ddr_version": parse_ddr_version(memory.get("ram_type")),
        "ram_slots": memory.get("slots"),
        "PCIe_16_gen": pcie_16_gen,
        "PCIe_16_slots": pcie_16_slots,
        "M_2_slots": len(data.get("m2_slots", [])),
        "SATA_6_ports": storage_devices.get("sata_6_gb_s"),
        "SATA_3_ports": storage_devices.get("sata_3_gb_s"),
        "U_2_ports": storage_devices.get("u2"),
        "ethernet_speed": ethernet_speed,
        "WiFi": data.get("wireless_networking"),
    }


def parse_storage_json(data):
    return {
        "capacity_GB": data.get("capacity"),
        "storage_type": data.get("storage_type"),
        "form_factor": data.get("form_factor"),
        "INTerface": data.get("interface"),  # key name must match SUBTYPE_DEFAULTS["Storage"] in db_add.py
        "cache_MB": None,  # not present in source data
        "nvme": data.get("nvme"),
    }


def parse_gpu_json(data):
    interface = data.get("interface", "") or ""
    pcie_16_gen = None
    for part in interface.split():
        try:
            pcie_16_gen = float(part)
        except ValueError:
            pass

    return {
        "clock_speed_MHz": data.get("core_base_clock"),
        "vram_GB": data.get("memory"),
        "vram_type": data.get("memory_type"),
        "PCIe_16_gen": pcie_16_gen,
    }


def parse_psu_json(data):
    # NOTE: no PSU sample provided yet — field paths below are guesses
    # and will need correcting against a real PSU JSON.
    specs = data.get("specifications", {})
    connectors = specs.get("connectors", {})

    return {
        "wattage": specs.get("wattage"),
        "form_factor": specs.get("formFactor"),
        "efficiency_rating": specs.get("efficiencyRating"),
        "atx_24_pin": connectors.get("atx24pin"),
        "eps_8_pin": connectors.get("eps8pin"),
        "pcie_12vhpwr": connectors.get("pcie12vhpwr"),
        "pcie_6_plus_2": connectors.get("pcie6plus2"),
        "sata": connectors.get("sata"),
        "molex_4_pin": connectors.get("molex4pin"),
    }


# maps part_type -> subtype-specific parser
PART_TYPE_PARSERS = {
    "CPU": parse_cpu_json,
    "RAM": parse_ram_json,
    "Motherboard": parse_motherboard_json,
    "Storage": parse_storage_json,
    "GPU": parse_gpu_json,
    "PSU": parse_psu_json,
}


def parse_component_json(filepath, part_type):
    if part_type not in PART_TYPE_PARSERS:
        raise ValueError(f"Unknown part type: {part_type}")

    with open(filepath, "r") as f:
        data = json.load(f)

    record = parse_common_fields(data)
    record.update(PART_TYPE_PARSERS[part_type](data))
    return record


def load_component_from_json(cnx, filepath, part_type):
    record = parse_component_json(filepath, part_type)
    return add_component(cnx, part_type, record)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_components.py <PartType> [folder]")
        print("e.g.:  python load_components.py CPU")
        print("       python load_components.py GPU ./my_gpu_folder")
        sys.exit(1)

    part_type = sys.argv[1]
    folder = ("open-db-json/" + part_type)

    if part_type not in PART_TYPE_PARSERS:
        print(f"Unknown part type: {part_type}")
        print(f"Valid types: {', '.join(PART_TYPE_PARSERS.keys())}")
        sys.exit(1)

    if not os.path.isdir(folder):
        print(f"No such folder: {folder}")
        sys.exit(1)

    cnx = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="tbu",
        password="",
        database="localtest",
    )

    loaded = 0
    failed = 0

    try:
        for filename in os.listdir(folder):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(folder, filename)
            try:
                load_component_from_json(cnx, filepath, part_type)
                print(f"Loaded: {filename}")
                loaded += 1
            except Exception as e:
                print(f"Failed: {filename} -> {e}")
                failed += 1

        cnx.commit()
    finally:
        cnx.close()

    print(f"\nDone. {loaded} loaded, {failed} failed.")