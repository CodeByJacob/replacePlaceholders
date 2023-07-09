import os
import typing as t
import re


def get_values_to_replace(_keys: t.List = None) -> t.Dict:
    values_to_replace: t.Dict = {}

    for key in _keys:
        values_to_replace[key] = os.getenv(key)

    print(values_to_replace)
    return values_to_replace


def replace_tokens(_file_content: str, _payload_data: t.Dict) -> str:
    for key, value in _payload_data.items():
        print(key, '->', value)
        _file_content = str(_file_content).replace(key, value)

    return _file_content


def prepare_dict_to_replacement(_prefix: str, _suffix: str, _file_content: str) -> t.Dict:
    replacement_dict: t.Dict = {}

    matches = re.findall(
        pattern=r"#{(.*?)}#",
        string=_file_content
    )

    for placeholder in matches:
        key = _prefix + placeholder + _suffix
        replacement_dict[key] = os.environ.get(placeholder) or ''

    return replacement_dict


if __name__ == "__main__":
    PREFIX: str = os.environ.get("INPUT_PREFIX") or "#{"
    SUFFIX: str = os.environ.get('INPUT_SUFFIX') or "}#"
    FILE: str = os.environ.get('INPUT_FILE')

    new_text: str = ""

    with open(FILE, 'r') as file:
        text = file.read()

        prepared_dict = prepare_dict_to_replacement(PREFIX, SUFFIX, text)
        new_text = replace_tokens(text, prepared_dict)

        file.close()

    with open(FILE, 'w') as file:
        file.write(new_text)