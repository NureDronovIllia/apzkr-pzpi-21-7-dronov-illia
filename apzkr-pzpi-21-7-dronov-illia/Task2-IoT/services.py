from time import sleep

from tqdm import tqdm

from api_fetch import get_storage_critical_lvl, get_storage_current_lvl, send_current_fuel_lvl, send_critical_message


def refuel_critical(storage_id: int) -> None:
    critical_lvl: int = get_storage_critical_lvl(storage_id)
    current_lvl: int = get_storage_current_lvl(storage_id)

    steps: int = int(current_lvl // 50)

    print("Start refueling the vehicle")
    for _ in tqdm(range(steps)):
        current_lvl -= 50
        send_current_fuel_lvl(storage_id, current_lvl)
        sleep(0.2)

        if current_lvl <= critical_lvl:
            send_critical_message(storage_id)
            print("Critical amount message was sent to administrator")
            break


    print("Refueling is over")


def refuel_regular(storage_id: int, fuel_amount: float) -> None:
    print("Start refueling the vehicle")
    current_lvl: int = get_storage_current_lvl(storage_id)
    send_current_fuel_lvl(storage_id, current_lvl - fuel_amount)
    print("Refueling is over")
