from __future__ import annotations

from datetime import datetime



def format_datetime(iso_date: str) -> str:
    if not iso_date:
        return ""

    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y %H:%M")



def format_output_date(iso_date: str) -> str:
    if not iso_date:
        return "unknown-date"

    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d")



def format_liters(value) -> str:
    if value is None or value == "":
        return ""
    return f"{float(value):.2f}"



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
