import re
from typing import Tuple


async def check_if_user_exists(cur, email) -> bool:
    if await cur.fetchrow('SELECT 1 FROM users WHERE email = $1', email):
        return True
    return False


def get_cols_and_placeholders(data: dict) -> Tuple[str, str, list]:
    """
    :param data:
    :return:
        - 'col1', 'col2', 'col3'
        - $1, $1, $1
        - [val1, val2, val3]
    """
    cols = [key for key in data if data[key]]
    placeholders = [f"${i}" for i in range(len(cols))]
    values = [data[key] for key in cols]
    return ", ".join(cols), ", ".join(placeholders), values


def validate_password(v: str) -> str:
    min_chars = 8
    min_nums = 2
    min_special_chars = 2

    # num_count = len(re.findall(r'\d', v))
    # special_char_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', v))

    if len(v) < min_chars:
        raise ValueError(f"Password must be at least {min_chars} characters long.")
    if len(re.findall(r'\d', v)) < min_nums:
        raise ValueError(f"Password must contain at least {min_nums} numbers.")
    if len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', v)) < min_special_chars:
        raise ValueError(f"Password must contain at least {min_special_chars} special characters.")
    return v
