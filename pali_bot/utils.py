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

from typing import List

from telegram.constants import MAX_MESSAGE_LENGTH

from pali_bot.sutta_provider import Sutta
from pali_bot.sutta_provider import SuttaProvider


def html_format_sutta(sutta: Sutta) -> str:
    # Tags must me closed at the same line where have been open because of
    # following spliting
    footnotes_entries = [f'<i>{ind}</i> — {text}' for ind, text in sutta['footnotes'].items()]
    footnotes = ''
    if len(footnotes_entries) > 0:
        footnotes += '___\n'
        footnotes += '\n'.join(footnotes_entries)
        footnotes += '\n\n'

    result = f'''
<b>{sutta['title']}</b>
<b><a href="{sutta['url']}">{sutta['index']}</a></b>

{sutta['text']}

{footnotes}<i>{sutta['credits']}</i>
'''

    return result


def split_long_message(text: str) -> List[str]:
    buf = ''
    result = []
    for line in text.splitlines():
        assert len(line) < MAX_MESSAGE_LENGTH, 'Too long line'
        line += '\n'
        if len(buf) + len(line) < MAX_MESSAGE_LENGTH:
            buf += line
        else:
            result.append(buf)
            buf = line

    result.append(buf.rstrip())

    return result
