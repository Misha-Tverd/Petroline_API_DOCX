from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    petroline_base_url: str
    petroline_login: str
    petroline_password: str
    petroline_token: str
    petroline_timeout: int
    use_sample_data: bool
    sample_data_path: Path
    template_path: Path
    output_dir: Path
    processed_ids_path: Path
    missing_log_path: Path
    retry_seconds: int
    date_from: str
    date_to: str
    subdivision_id: int | None
    take: int
    target_driver: str
    company: str
    structural_unit: str
    accountant: str
    fuel_limit: float
    unit_name: str



def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}



def _to_int_or_none(value: str | None) -> int | None:
    if not value:
        return None
    return int(value)


def _to_float(value: str | None, default: float = 0) -> float:
    if value is None or value.strip() == "":
        return default
    return float(value.replace(",", "."))



def get_settings() -> Settings:
    return Settings(
        petroline_base_url=os.getenv("PETROLINE_BASE_URL", "https://apiv2.petroline.in.ua").rstrip("/"),
        petroline_login=os.getenv("PETROLINE_LOGIN", ""),
        petroline_password=os.getenv("PETROLINE_PASSWORD", ""),
        petroline_token=os.getenv("PETROLINE_TOKEN", ""),
        petroline_timeout=int(os.getenv("PETROLINE_TIMEOUT", "30")),
        use_sample_data=_to_bool(os.getenv("USE_SAMPLE_DATA", "true"), default=True),
        sample_data_path=Path(os.getenv("SAMPLE_DATA_PATH", "sample_data/sample_transactions.json")),
        template_path=Path(os.getenv("TEMPLATE_PATH", "templates/template.docx")),
        output_dir=Path(os.getenv("OUTPUT_DIR", "output")),
        processed_ids_path=Path(os.getenv("PROCESSED_IDS_PATH", "data/processed_ids.json")),
        missing_log_path=Path(os.getenv("MISSING_LOG_PATH", "logs/missing_fields_log.json")),
        retry_seconds=int(os.getenv("RETRY_SECONDS", "0")),
        date_from=os.getenv("DATE_FROM", ""),
        date_to=os.getenv("DATE_TO", ""),
        subdivision_id=_to_int_or_none(os.getenv("SUBDIVISION_ID")),
        take=int(os.getenv("TAKE", "100")),
        target_driver=os.getenv("TARGET_DRIVER", "Кондратюк Сергій Анатолійович"),
        company=os.getenv("COMPANY", ""),
        structural_unit=os.getenv("STRUCTURAL_UNIT", ""),
        accountant=os.getenv("ACCOUNTANT", ""),
        fuel_limit=_to_float(os.getenv("FUEL_LIMIT"), default=1000),
        unit_name=os.getenv("UNIT_NAME", "літр"),
    )
