from db_add import *
import json


def parse_cpu_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    name = data.get("metadata", {}).get("name")
    socket_type = data.get("socket")
    cores = data.get("cores", {}).get("total")

    base_clock_ghz = data.get("clocks", {}).get("performance", {}).get("base")
    clock_speed_MHz = int(base_clock_ghz * 1000) if base_clock_ghz else None

    max_ram_capacity_GB = data.get("specifications", {}).get("memory", {}).get("maxSupport")
    max_ram_capacity_MB = int(max_ram_capacity_GB * 1024) if max_ram_capacity_GB else None

    ddr_types = data.get("specifications", {}).get("memory", {}).get("types", [])
    ddr_version = None
    if ddr_types:
        digits = "".join(ch for ch in ddr_types[0] if ch.isdigit())
        ddr_version = int(digits) if digits else None

    return {
        "name": name,
        "socket_type": socket_type,
        "cores": cores,
        "clock_speed_MHz": clock_speed_MHz,
        "max_ram_capacity_MB": max_ram_capacity_MB,
        "ddr_version": ddr_version,
    }


def load_cpu_from_json(cursor, filepath):
    record = parse_cpu_json(filepath)
    return add_component(cursor, "CPU", record)