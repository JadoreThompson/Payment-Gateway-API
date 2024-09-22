def print_exception(func_name, e):
    print(f"{func_name}, Type: {type(e)} Error: {str(e)}")


def validate_against_enum(target_enum, v) -> bool:
    if v in [item.value for item in target_enum]:
        return True
    return False


def value_error_string(topic ,target_enum) -> str:
    return f"{topic} must be of {[item.value for item in target_enum]}"
