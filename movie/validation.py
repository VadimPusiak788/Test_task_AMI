from movie.exception import PageNotAnInteger, LengthNotCorrect


def validate_number(number: int) -> int:
    try:
        if isinstance(number, float) and not number.is_integer():
            raise ValueError
        page_number = int(number)
    except (TypeError, ValueError):
        raise PageNotAnInteger

    return page_number


def validate_len(src: str) -> str:
    if not (len(src) >= 2 and len(src) <= 20):
        raise LengthNotCorrect
