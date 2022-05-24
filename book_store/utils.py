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


def can_string_be_converted_to_bool(str_):
    """
    To check if the supplied value can be converted to bool
    :param str_: supplied value
    :return: bool value
    """
    if not str_:
        return False
    if str_ in [True, False, 0, 1] or str_.lower() in ['true', 't', 'yes', 'y', '1', "false", 'f', 'no', 'n', '0']:
        return True
    return False


def convert_string_to_bool(str_):
    """
    To convert the supplied value to boolean
    :param str_: supplied value
    :return: bool value
    """
    if can_string_be_converted_to_bool(str_=str_):
        true = ("True", "true", "TRUE", "T", "t", True,
                "YES", "Yes", "yes", "Y", "y", "1", 1)
        false = ("False", "false", "FALSE", "F", "f",
                 False, "No", "no", "NO", "N", "n", "0", 0)
        if str_ in true:
            return True
        elif str_ in false:
            return False
        else:
            raise ValueError("Invalid inputs for STR to Bool conversion ")
    else:
        return False
