import config
import yaml

from typing import List
from typing import Optional
#from typing import 


def random_sutta(txt_file: str) -> str:
    file_path = os.path.join(DIR, 'data', txt_file)
    with open(file_path, 'r', encoding='cp1251') as f:
        contents = CACHE.get(txt_file)
        if contents is None:
            contents = f.read()
            CACHE[txt_file] = contents

    text_split = contents.split('___separator___')
    sn = random.randint(0, len(text_split) - 1)
    result = text_split[sn]
    return result

class SuttaProvider:
    def __init__(self, data_dir: Optional[str] = None):

    def get_sections(self) -> List[str]:
        ...

    def get_random(section: Optional[str] = None) -> str:
        ...
