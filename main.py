from fpdf import FPDF
import json
from loguru import logger as log
import sys
def decode_lines(line: str):
    """Recusively splits the string into text and chords"""
    if "{" in line or "}" in line:
        splitted_line = line.rsplit("}",1)
        splitted_line2 = splitted_line[0].rsplit("{",1)
        text, chords = decode_lines(splitted_line2[0])
        text.append(splitted_line[1])
        chords.append(splitted_line2[1])
        return text, chords
    else:
        return [line], []

class Songbook:
    def __init__(self, title: str):
        self.title = title
        self.pdf = FPDF()

    def add_title_page(self):
        self.pdf.add_page()
        self.pdf.set_font("times", "", 60)
        self.pdf.cell(0, 10, self.title, 0, 0, "C")
        log.info(f"added Title Page with Title:{self.title}")

    def add_song(self, title: str, artist: str, verses: dict, scheme: list):
        self.pdf.add_page()
        self.pdf.set_font("times", "", 40)
        self.pdf.cell(
            0,
            10,
            title,
        )
        log.debug(f"added title of {title}")
        if artist:
            self.pdf.set_font_size(20)
            self.pdf.cell(0,10,artist)
        log.debug(f"verses:{scheme}")
        for verse in scheme:
            self.add_verse(verses[verse])
    def add_verse(self, verse: str):
        lines = verse.split("%")
        for line in lines:
            text, chords = decode_lines(line)
            log.debug(f"{chords = } {text = }")
            
    def output(self, name: str):
        self.pdf.output(name)


if __name__ == "__main__":
    songbook = Songbook("Ameisenliederbuch")
    songbook.add_title_page()
    with open("/home/user/repos/songbook/Songs/0.2/songs.json", "r") as f:
        data = json.load(f)
    songbook.add_song(
        "Butter Bei Die Fische",
        data["songs"]["Butter Bei Die Fische"]["meta"]["artist"],
        data["songs"]["Butter Bei Die Fische"]["txt"],
        data["songs"]["Butter Bei Die Fische"]["scheme"],
    )
    songbook.output("tmp_test.pdf")
