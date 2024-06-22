import re
from datetime import datetime
from typing import Optional

import regex
from fastapi import HTTPException, status

from app.config.logs.logger import logger
from app.utilities.formatters.http_error import error_wrapper
from app.utilities.validators.payload.string_stripper import string_stripper


@string_stripper
def validate_text(
    value: str,
    field_name: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
):
    if value is None:
        return value

    if min_length and max_length:
        if not min_length <= len(value) <= max_length:
            logger.warning(f"Validation error: {field_name} has invalid length")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_wrapper(
                    f"{field_name} should contain from {min_length} to {max_length} characters",
                    field_name,
                ),
            )

    if not regex.fullmatch(r"^[\p{L}1-9\-./!,\(\) ]+$", value):
        logger.warning(
            f"Validation error: {field_name} field contains restricted characters"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "This field may contain only english letters, numbers and special characters (.-'!()/ )",
                field_name,
            ),
        )

    return value


def validate_manufacture_year(value: str):
    if value is None:
        return
    current_year = datetime.utcnow().year
    if not re.compile(r"^\d{4}$").match(str(value)):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Manufacture year should be a valid 4-digit integer",
                "manufacture_year",
            ),
        )
    if not 1800 <= value <= current_year:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                f"Manufacture year should have value from 1800 to {current_year}",
                "manufacture_year",
            ),
        )

    return str(value)


def validate_license_plate(value: str):
    if value is None:
        return
    if not regex.fullmatch(r"^(?!^0+$)[\p{L}0-9]{1,10}$", value):
        logger.warning("Validation error: invalid driver license number")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Car license plate should contain from 1 to 10 characters",
                "license_plate",
            ),
        )

    return value
