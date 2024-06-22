from dataclasses import dataclass
from typing import Any

import requests

from config import get_base_url, get_jwt

JWT: str = get_jwt()
BASE_URL: str = get_base_url()


@dataclass
class Storage:
    max_amount: int
    critical_amount: int
    fuel_type: str
    id: int
    current_amount: float


def get_storages() -> list[Storage]:
    response = requests.get(
        f"{BASE_URL}/fuel/storages/", headers={"Authorization": f"Bearer {JWT}"}
    )
    return response.json()


def get_storages_ids() -> list[int]:
    storages: list[Storage] = get_storages()
    return [storage["id"] for storage in storages]


def get_storage_critical_lvl(storage_id: int) -> int:
    storages: list[Storage] = get_storages()
    for storage in storages:
        if storage["id"] == storage_id:
            return storage["critical_amount"]


def get_storage_current_lvl(storage_id: int) -> int:
    storages: list[Storage] = get_storages()
    for storage in storages:
        if storage["id"] == storage_id:
            return storage["current_amount"]


def send_current_fuel_lvl(storage_id: int, current_lvl: float) -> None:
    requests.patch(
        f"{BASE_URL}/fuel/storages/{storage_id}/update",
        json={"current_amount": current_lvl},
        headers={"Authorization": f"Bearer {JWT}"},
    )

def send_critical_message(storage_id: int) -> None:
    requests.post(
        f"{BASE_URL}/admin/send-critical-messages/",
        json={"storage_id": storage_id, "message": f"Storage {storage_id} requires fuel purchase"},
        headers={"Authorization": f"Bearer {JWT}"},
    )