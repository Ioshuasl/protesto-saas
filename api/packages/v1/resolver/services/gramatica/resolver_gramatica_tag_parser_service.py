import re
from typing import Optional, Tuple

GRAMATICA_TAG_REGEX = re.compile(r"^<!\[(?P<palavra>[^\]]+)\]\[(?P<tipo>\d+)\]!>$")
CONTROL_CHARS_REGEX = re.compile(r"[\x00-\x1F\x7F]")


def parse_gram_tag(raw: str) -> Optional[Tuple[str, str]]:
    if not raw:
        return None

    match = GRAMATICA_TAG_REGEX.match(raw.strip())
    if not match:
        return None

    palavra = match.group("palavra")
    palavra = CONTROL_CHARS_REGEX.sub("", palavra)
    palavra = " ".join(palavra.strip().split())
    tipo = match.group("tipo")
    if not palavra:
        return None

    return palavra, tipo
