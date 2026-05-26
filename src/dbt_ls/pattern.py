import re


def ref_pattern(text: str):
    return re.match(r"ref\(('|\")\w*$", text)

def source_pattern(text: str):
    return re.match(r"source\(('|\")\w*$", text)
