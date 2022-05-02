import random

def mainconfig(txt_file):
    with open(txt_file, "r") as f:
        contents = f.read()
        result = contents.split('___separator___')
        sn = random.randint(0, len(result) - 1)
        return result[sn]
