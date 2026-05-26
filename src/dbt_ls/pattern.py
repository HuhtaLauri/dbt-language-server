import re


def ref_pattern(text: str):
    return re.match(r"ref\(('|\")\w*$", text)

def source_pattern(text: str):
    return re.match(r"source\(('|\")\w*$", text)

def column_pattern(text: str):
    return re.match(r"[a-zA-Z_][a-zA-Z0-9_]*\.([a-zA-Z_]*)$", text)
