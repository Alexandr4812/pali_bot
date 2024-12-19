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
from typing import Dict
from typing import List
from typing import TypedDict
from typing import Optional

import jsonschema
import yaml

import pali_bot


class Sutta(TypedDict):
    title: str
    index: str
    text: str
    url: str
    footnotes: Dict[int, str]


class SuttaProvider:
    class InvalidData(RuntimeError):
        ...

    def __init__(self, data_dir: str):
        self._logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

        self._data: Dict[str, List[Sutta]] = {}

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
            self._logger.info('%s file is loaded', file_path)

        self._logger.info('Data is loaded')

        all_ = []
        for val in self._data.values():
            all_.extend(val)

        self._data['any'] = all_

    @property
    def sections(self) -> List[str]:
        """ Get list of existing section including special "any" section
        """
        return list(self._data)

    def get_section_length(self, section: Optional[str]) -> int:
        """ Get length of the named section

        :param section: "any" if None
        :return: int
        :raises KeyError: if named section is not exists
        """
        if section is None:
            section = 'any'
        return len(self._data[section])

    def get_sutta(self, section: Optional[str], number: int) -> Sutta:
        """ Get sutta from named section by index

        :param section: "any" if None
        :param number: number of a text in the section starting from 1
        :return: Sutta
        :raises KeyError: if named section is not exists
        :raises IndexError: if number is out of range
        """
        if number < 1:
            raise IndexError('Only positive inices accepted beginning from 1')
        if section is None:
            section = 'any'
        return self._data[section][number - 1]

    def get_random_sutta(self, section: Optional[str] = None) -> Sutta:
        """ Get random sutta from named section

        :param section: name of section, "any" if None
        :return: Sutta
        :raises KeyError: if named section is not exists
        """
        index = random.randint(1, self.get_section_length(section))
        return self.get_sutta(section=section, number=index)
