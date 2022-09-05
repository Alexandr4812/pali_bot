#! /usr/bin/env python3

# Copyright 2022 Alexandr Cherkaev, Anton Karmanov <a.karmanov@inventati.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import importlib
import logging
import random

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import jsonschema
import yaml

import pali_bot


class SuttaProvider:
    class InvalidData(RuntimeError):
        ...

    Sutta = Dict[str, Any]

    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = './data/'

        self._logger = logging.getLogger(f'{__name__}.{__class__.__name__}')

        self._data: Dict[str, List[Dict]] = {}

        files = Path(data_dir).glob('*.yaml')

        schema_txt = importlib.resources.open_text(pali_bot, 'data_schema.yaml')
        schema = yaml.safe_load(schema_txt)

        self._logger.info('Begin loading data')
        for file_path in files:
            with open(file_path, 'r', encoding='UTF-8') as file:
                content = yaml.safe_load(file)
                try:
                    jsonschema.validate(content, schema)
                except jsonschema.ValidationError as error:
                    raise self.InvalidData(f'Misformed data in {file_path}: {error}') from None
            section = Path(file_path).stem
            self._data[section] = content
            self._logger.info(f'{file_path} file is loaded')

        self._logger.info('Data is loaded')

        all_ = []
        for val in self._data.values():
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
