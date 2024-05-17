from typing import Any
import json
from collections import namedtuple
from Songbook.types import Song
def decode_songfile(path: str) -> Any:
    with open(path, "r") as f:
        data: Any= json.load(f)
        song = Song(data["verses"], data["meta"], data["scheme"])
        return song