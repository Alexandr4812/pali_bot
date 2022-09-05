import random

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import yaml


class SuttaProvider:
    Sutta = Dict[str, Any]

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = './data/'

        self._data: Dict[str, List[Dict]] = {}

        files = Path(data_dir).glob('*.yaml')

        # TODO Validate with JSONSchema
        for file_path in files:
            with open(file_path, 'r', encoding='UTF-8') as file:
                content = yaml.safe_load(file)
            section = Path(file_path).stem
            self._data[section] = content

        all_ = []
        for key, val in self._data.items():
            all_.extend(val)

        self._data['any'] = all_

    @property
    def sections(self) -> List[str]:
        return list(self._data)

    def get_random_sutta(self, section: Optional[str] = None) -> Sutta:
        if section is None:
            section = 'any'

        suttas = self._data[section]
        index = random.randint(0, len(suttas) - 1)

        return suttas[index]
