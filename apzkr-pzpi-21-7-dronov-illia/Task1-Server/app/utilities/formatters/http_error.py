from uuid import UUID


def error_wrapper(message: str, field: str) -> dict[str, str]:
    return {"message": message, "field": field}
