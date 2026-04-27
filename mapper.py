from __future__ import annotations

from datetime import datetime
from unicodedata import normalize



def format_datetime(iso_date: str) -> str:
    if not iso_date:
        return ""

    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y %H:%M")


def format_day(iso_date: str) -> str:
    if not iso_date:
        return ""

    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y")



def format_output_date(iso_date: str) -> str:
    if not iso_date:
        return "unknown-date"

    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d")



def format_liters(value) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.2f}"


def format_number(value) -> str:
    if value is None or value == "":
        return ""

    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.2f}".rstrip("0").rstrip(".")



def format_amount(value) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.2f} грн"



def map_transaction_to_word_tags(transaction: dict) -> dict:
    return {
        "date": format_datetime(transaction.get("date", "")),
        "driver": transaction.get("personName", "") or "",
        "vehicle": transaction.get("transportName", "") or "",
        "fuel": transaction.get("fuelName", "") or "",
        "liters": format_liters(transaction.get("valueLitr")),
        "amount": format_amount(transaction.get("value")),
        "azs": transaction.get("azsName", "") or "",
        "transaction_id": str(transaction.get("id", "")),
        "card1_number": transaction.get("card1Number", "") or "",
        "card2_number": transaction.get("card2Number", "") or "",
        "recipient": transaction.get("recipientName", "") or "",
    }


def normalize_text(value: str) -> str:
    value = normalize("NFKC", value or "").casefold()
    return " ".join(value.split())


def get_driver_name(transaction: dict) -> str:
    return (
        transaction.get("personName")
        or transaction.get("recipientName")
        or transaction.get("driverName")
        or ""
    )


def get_transaction_liters(transaction: dict) -> float:
    value = (
        transaction.get("valueLitr")
        or transaction.get("liters")
        or transaction.get("quantity")
        or transaction.get("amount")
        or 0
    )
    return float(str(value).replace(",", "."))


def transaction_matches_driver(transaction: dict, driver_name: str) -> bool:
    expected = normalize_text(driver_name)
    actual = normalize_text(get_driver_name(transaction))
    return bool(expected and actual and expected in actual)


def map_transactions_to_limit_card(transactions: list[dict], settings) -> dict:
    if not transactions:
        raise ValueError("Cannot build limit card without transactions.")

    sorted_transactions = sorted(transactions, key=lambda item: item.get("date", ""))
    first = sorted_transactions[0]
    driver = get_driver_name(first) or settings.target_driver
    vehicle = first.get("transportName") or first.get("vehicleName") or ""
    fuel = first.get("fuelName") or first.get("productName") or "ДП"
    limit = float(settings.fuel_limit)

    rows = []
    total_issued = 0.0
    for item in sorted_transactions:
        issued = get_transaction_liters(item)
        total_issued += issued
        rows.append(
            {
                "date": format_day(item.get("date", "")),
                "fuel": item.get("fuelName") or fuel,
                "unit": settings.unit_name,
                "limit": format_number(limit),
                "issued": format_number(issued),
                "balance": format_number(limit - total_issued),
            }
        )

    return {
        "company": settings.company,
        "structural_unit": settings.structural_unit,
        "recipient_line": " ".join(part for part in (vehicle, driver) if part),
        "recipient_name": driver,
        "vehicle": vehicle,
        "fuel": fuel,
        "unit": settings.unit_name,
        "limit": format_number(limit),
        "date": format_day(first.get("date", "")),
        "rows": rows,
        "total_issued": format_number(total_issued),
        "total_with_returned": format_number(total_issued),
        "driver_signature": driver,
        "accountant": settings.accountant,
    }
