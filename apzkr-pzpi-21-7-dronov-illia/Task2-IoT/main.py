from typing import Optional

from api_fetch import get_storages_ids
from auth import authenticate_iot
from services import refuel_critical, refuel_regular


def _ask_storage_id() -> Optional[int]:
    storage_id: int = int(input("Enter fuel storage_id:"))
    available_ids: list[int] = get_storages_ids()

    if storage_id not in available_ids:
        print("Wrong storage id")
        return None
    
    return storage_id


def main() -> None:
    authenticate_iot()

    try:
        scenario: int = int(
            input(
                'If you want to start a refuel to critical amount enter "1"\nIf you want to refuel to a specific amount enter "2":'
            )
        )

        if scenario not in [1, 2]:
            print("Only 1 and 2 are allowed")
            return

        if scenario == 1:
            storage_id = _ask_storage_id()
            if storage_id:
                refuel_critical(storage_id)
        else:
            storage_id = _ask_storage_id()
            fuel_amount: int = int(input("Enter fuel amount:"))
            if storage_id:
                refuel_regular(storage_id, fuel_amount)

    except ValueError:
        print("Value should be an integer")


if __name__ == "__main__":
    main()
