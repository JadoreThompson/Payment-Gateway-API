from typing import Tuple


def print_exception(func_name, e):
    print(f"{func_name}, Type: {type(e)} Error: {str(e)}")


def validate_against_enum(target_enum, v) -> bool:
    if v in [item.value for item in target_enum]:
        return True
    return False


def value_error_string(topic ,target_enum) -> str:
    return f"{topic} must be of {[item.value for item in target_enum]}"


def get_cols_and_placeholders(data: dict) -> Tuple[str, str, list]:
    """
    :param data:
    :return:
        - 'col1', 'col2', 'col3'
        - $1, $1, $1
        - [val1, val2, val3]
    """
    cols = [key for key in data if data[key] != None]
    placeholders = [f"${i}" for i in range(1, len(cols) + 1)]
    values = [data[key] for key in cols]
    return ", ".join(cols), ", ".join(placeholders), values
