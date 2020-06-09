import re


def extract_license(text: str):
    if not text:
        return ""
    text = text.strip()
    pattern = re.compile(r'[0-9A-Z\-\s]{7,18}')
    matches = pattern.findall(text)
    if not matches:
        return ""
    return max(matches, key=len)
