import requests

from config import get_auth_creds, get_base_url, get_jwt, set_jwt

BASE_URL: str = get_base_url()


def authenticate_iot(force: bool = False) -> None:
    jwt: str = get_jwt()
    if not jwt or force:
        auth_data: dict[str, str] = get_auth_creds()
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login/",
                json={"email": auth_data["email"], "password": auth_data["password"]},
            )
            if response.status_code != 200:
                print("Server-side error, try later")
                return

            jwt = (response.json())["token"]
            set_jwt(jwt)
        except requests.ConnectionError as e:
            print("Error while authenticating the device")
