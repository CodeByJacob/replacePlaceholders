import os
import typing as t
import re

PREFIX: str = os.environ.get("INPUT_PREFIX") or "#{"
SUFFIX: str = os.environ.get('INPUT_SUFFIX') or "}#"
FILE: str = os.environ.get('INPUT_FILES')
FILES_PATH: str = os.environ.get('INPUT_WORK_PATH') or "./"


def get_values_to_replace(_keys: t.List = None) -> t.Dict:
    values_to_replace: t.Dict = {}

    for key in _keys:
        values_to_replace[key] = os.getenv(key)

    return values_to_replace


def replace_tokens(_file_content: str, _payload_data: t.Dict) -> str:
    print("Replaced tokens:")
    for key, value in _payload_data.items():
        _file_content = str(_file_content).replace(key, value)
        print(key, '->', value)

    return _file_content


def prepare_dict_to_replacement(_prefix: str, _suffix: str, _file_content: str) -> t.Dict:
    replacement_dict: t.Dict = {}

    tokens_pattern = fr"{_prefix}(.*?){_suffix}"

    matches = re.findall(
        pattern=tokens_pattern,
        string=_file_content
    )

    for placeholder in matches:
        key = _prefix + placeholder + _suffix
        replacement_dict[key] = os.environ.get(placeholder) or ''

    return replacement_dict


def get_files(_files_str: str) -> t.List:
    _files: t.List[str] = []
    _files = _files_str.translate(str.maketrans('', '', ' []')).split(',')

    return _files


if __name__ == "__main__":
    _files_list: t.List = get_files(FILE)

    for _file in _files_list:
        new_text: str = ""
        file_path = FILES_PATH + _file
        print(f"Replacing token in {_file}")

        print(file_path)
        with open(file_path, 'r') as file:
            text = file.read()

            prepared_dict = prepare_dict_to_replacement(PREFIX, SUFFIX, text)
            new_text = replace_tokens(text, prepared_dict)

            print(new_text)
            file.close()

        with open(file_path, 'w') as file:
            file.write(new_text)
            file.close()
