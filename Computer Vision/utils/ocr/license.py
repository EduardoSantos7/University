import re


def extract_license(text: str):
    text = text.strip()
    pattern = re.compile(r'[0-9A-Z\-\s]+')
    matches = pattern.findall(text)
    return max(matches, key=len)
