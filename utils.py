from __future__ import annotations

import re
from pathlib import Path

from mapper import format_output_date


INVALID_FILENAME_CHARS = r'[<>:"/\\|?*]'



def sanitize_filename_part(value: str, fallback: str = "unknown") -> str:
    cleaned = re.sub(INVALID_FILENAME_CHARS, "_", value or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.replace(" ", "_")
    return cleaned or fallback



def build_driver_folder_name(driver_name: str) -> str:
    parts = [part for part in (driver_name or "").split() if part]
    if not parts:
        return "UnknownDriver"

    surname = parts[0]
    initials = "".join(part[0].upper() for part in parts[1:3] if part)
    base = f"{surname}_{initials}" if initials else surname
    return sanitize_filename_part(base, fallback="UnknownDriver")



def build_file_name(transaction: dict) -> str:
    date_part = format_output_date(transaction.get("date", ""))
    vehicle = sanitize_filename_part(transaction.get("transportName", ""), fallback="UnknownVehicle")
    driver_raw = transaction.get("personName", "") or ""
    driver_surname = driver_raw.split()[0] if driver_raw.strip() else "UnknownDriver"
    driver = sanitize_filename_part(driver_surname, fallback="UnknownDriver")
    return f"{date_part}_{vehicle}_{driver}.docx"



def build_output_paths(base_output_dir: Path, transaction: dict) -> tuple[Path, Path]:
    date_part = format_output_date(transaction.get("date", ""))
    vehicle_folder = sanitize_filename_part(transaction.get("transportName", ""), fallback="UnknownVehicle")
    driver_folder = build_driver_folder_name(transaction.get("personName", ""))
    file_name = build_file_name(transaction)

    vehicle_path = base_output_dir / "by_vehicle" / vehicle_folder / date_part / file_name
    driver_path = base_output_dir / "by_driver" / driver_folder / date_part / file_name
    return vehicle_path, driver_path
