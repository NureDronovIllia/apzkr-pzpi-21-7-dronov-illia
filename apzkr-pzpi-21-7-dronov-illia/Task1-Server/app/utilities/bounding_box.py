import random
from dataclasses import dataclass
from math import cos, radians

from geopy.distance import geodesic

MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180


@dataclass(frozen=True, slots=True)
class BoundingBoxDTO:
    """The class represents coordinates of four vertices of the bounding box."""

    nwlng: float
    selng: float
    nwlat: float
    selat: float
    nelng: float
    swlng: float
    nelat: float
    swlat: float


class GeoPoint:
    def __init__(self, latitude: float, longitude: float):
        if not MIN_LATITUDE <= latitude <= MAX_LATITUDE:
            raise ValueError("Invalid latitude value")
        if not MIN_LONGITUDE <= longitude <= MAX_LONGITUDE:
            raise ValueError("Invalid longitude value")
        self.latitude = latitude
        self.lognitude = longitude


class BoundingBox:
    def get_coords_of_bounding_box(
        self, point: GeoPoint, distance: int = 1000
    ) -> BoundingBoxDTO:
        """
        Calculate the coordinates of bounding box vertices.

        :param point: A GeoPoint object represents the geographic coordinates (latitude, longitude).
        :param distance: The distance in meters from side to side of the search area border.
        :return: Coordinates of four vertices of the bounding box.
        """

        # Calculate distance from center point to the vertex of the square
        distance_in_m = (distance / 2) / (1000 * cos(radians(45)))

        north_east_point = geodesic(kilometers=distance_in_m).destination(
            (point.latitude, point.lognitude), 45
        )
        south_east_point = geodesic(kilometers=distance_in_m).destination(
            (point.latitude, point.lognitude), 135
        )
        south_west_point = geodesic(kilometers=distance_in_m).destination(
            (point.latitude, point.lognitude), 225
        )
        north_west_point = geodesic(kilometers=distance_in_m).destination(
            (point.latitude, point.lognitude), 315
        )

        return BoundingBoxDTO(
            nwlng=north_west_point.longitude,
            selng=south_east_point.longitude,
            nwlat=north_west_point.latitude,
            selat=south_east_point.latitude,
            nelng=north_east_point.longitude,
            swlng=south_west_point.longitude,
            nelat=north_east_point.latitude,
            swlat=south_west_point.latitude,
        )

    def generate_random_point(self, bounding_box: BoundingBoxDTO) -> GeoPoint:
        """
        Generate a random point within the bounding box.

        :return: A GeoPoint object represents the random point.
        """
        # bounding_box: BoundingBoxDTO = self.get_coords_of_bounding_box(
        #     GeoPoint(49.990867, 36.264505), 12000
        # )
        random_lng = random.uniform(bounding_box.nwlng, bounding_box.selng)
        random_lat = random.uniform(bounding_box.swlat, bounding_box.nelat)

        return GeoPoint(latitude=random_lat, longitude=random_lng)


bounding_box = BoundingBox()
