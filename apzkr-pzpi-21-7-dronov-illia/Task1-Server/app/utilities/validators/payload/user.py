import re

import regex
from fastapi import HTTPException, status

from app.config.logs.logger import logger
from app.utilities.formatters.http_error import error_wrapper
from app.utilities.validators.payload.string_stripper import string_stripper


def validate_password(value: str, field_name: str = "password"):
    if not re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$").match(value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Password should contain at least eight characters, at least one letter and one number",
                field_name,
            ),
        )
    return value


@string_stripper
def validate_name(value: str, field_name: str):
    if value is None:
        return value
    if not (2 <= len(value) <= 25):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                f"{field_name} should contain from 2 to 25 characters", field_name
            ),
        )

    if not regex.fullmatch(r"\p{L}+", value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                f"{field_name} should contain only letters", field_name
            ),
        )
    return value


@string_stripper
def validate_phone_number(value: str):
    if value is None:
        return value
    if not (8 <= len(value[1:]) <= 20):
        logger.warning("Validation error: 'phone_number' has invalid length")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Phone number should contain from 8 to 20 characters", "phone_number"
            ),
        )
    if value[0] != "+" or not re.compile(r"^[0-9]+$").match(value[1:]):
        logger.warning(
            "Validation error: 'phone_number' field does not contain '+' character or contains incorrect characters"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Phone number should start with '+' and contain only numeric characters (0-9)",
                "phone_number",
            ),
        )
    return value


def validate_driver_license_number(value: str) -> str:
    if value is None:
        return
    if not bool(re.search(r"\d", value)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Driver license number should contain at least 1 number",
                "driver_license_number",
            ),
        )
    if not re.compile(r"^(?!^0+$)[a-zA-Z0-9]{3,20}$").match(value):
        logger.warning("Validation error: invalid driver license number")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Driver license number should contain from 3 to 20 characters and shouldn't contain only 0's",
                "driver_license_number",
            ),
        )

    return value


def validate_passport_number(value: str) -> str:
    if value is None:
        return
    if not bool(re.search(r"\d", value)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Passport number should contain at least 1 number", "passport_number"
            ),
        )
    if not re.compile(r"^(?!^0+$)[a-zA-Z0-9]{3,20}$").match(value):
        logger.warning("Validation error: invalid passport number")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_wrapper(
                "Passport number should contain from 3 to 20 characters and shouldn't contain only 0's",
                "passport_number",
            ),
        )

    return value
