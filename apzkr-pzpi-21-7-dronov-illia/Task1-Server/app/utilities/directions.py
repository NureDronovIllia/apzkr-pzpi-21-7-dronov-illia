from typing import Any

from googlemaps import Client, directions

from app.config.settings.base import settings


def get_direction(
    start_point: tuple[float], end_point: tuple[float]
) -> list[dict[str, Any]]:
    gmaps = Client(key=settings.GOOGLE_CLOUD_API_KEY)
    directions_result = directions.directions(
        gmaps, start_point, end_point, mode="driving"
    )

    return directions_result


def get_address(point: tuple[float]) -> str:
    data: list[dict[str, Any]] = get_direction(point, point)
    address: str = data[0]["legs"][0]["start_address"]

    return address
