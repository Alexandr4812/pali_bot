from typing import Dict
from typing import List


class SectionEntry:
    def __init__(self, filename: str, displayname: str, tags: List[str] = None):
        if tags is None:
            tags = []

        self.filename = filename
        self.displayname = displayname


def get_greeting_text(template: str, command_mapping: Dict[str, SectionEntry]) -> str:
    command_list = [f'{val.displayname}: /{key}' for key, val in command_mapping.items()]
    command_text = '\n'.join(command_list)
    return template.format(command_text=command_text)
