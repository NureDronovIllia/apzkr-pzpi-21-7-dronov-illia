import json

STORAGE_FILE_NAME: str = "local_storage.json"


def get_base_url() -> str:
    with open(STORAGE_FILE_NAME, "r", encoding="utf-8") as file:
        data: dict = json.loads(file.read())
        return data["base_url"]


def get_jwt() -> str:
    with open(STORAGE_FILE_NAME, "r", encoding="utf-8") as file:
        data: dict = json.loads(file.read())
        return data["jwt"]


def get_auth_creds() -> dict[str, str]:
    with open(STORAGE_FILE_NAME, "r", encoding="utf-8") as file:
        data: dict = json.loads(file.read())
        return {"email": data["device_email"], "password": data["device_password"]}


def set_jwt(token: str) -> None:
    with open(STORAGE_FILE_NAME, "r", encoding="utf-8") as file:
        current_data: dict = json.loads(file.read())
        current_data["jwt"] = token

    with open(STORAGE_FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(current_data, file, ensure_ascii=False, indent=4)
