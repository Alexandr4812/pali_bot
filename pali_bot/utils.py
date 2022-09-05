from typing import List

from telegram.constants import MAX_MESSAGE_LENGTH

from pali_bot.sutta_provider import SuttaProvider


def html_format_sutta(sutta: SuttaProvider.Sutta) -> str:
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
