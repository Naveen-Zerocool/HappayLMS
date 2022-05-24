from datetime import datetime

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


def validate_data(data, validator, mandatory=False):
    if not callable(validator):
        raise ValueError(f"{validator} should be a function")

    is_valid, error_message = True, None
    if mandatory or data:
        is_valid, error_message = validator(data)

    return data if is_valid else None, error_message


def validate_phone_number(phone_number):
    try:
        formatted_phone_number = phonenumbers.parse(phone_number, None)
        if phonenumbers.is_possible_number(
                formatted_phone_number
        ) and phonenumbers.is_valid_number(
            formatted_phone_number
        ):
            return True, None
        return False, "Not Valid Phone Number"
    except NumberParseException:
        return False, "Not Valid Phone Number"


def validate_date(given_date, validate_format="%Y-%m-%d"):
    try:
        datetime.strptime(str(given_date), validate_format)
        return True, None
    except ValueError:
        return False, "Date format not valid, date should follow YYYY-MM-DD format. Example: 2022-03-07"
