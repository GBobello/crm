import re


def validate_phone(phone: str) -> bool:
    value = re.sub(r"[()./-]", "", phone)
    value = re.sub(r"[\s]", "", value)

    if not re.match(r"^(\d{1,3}[- ]?)?\d{10}$", value):
        return False

    return True
