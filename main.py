from fpdf import FPDF
import json
from loguru import logger as log
import sys
from os import listdir

def decode_lines(line: str) -> tuple[list[str], list[str]]:
    """Recusively splits the string into line_par and chords"""
    if "{" in line or "}" in line:
        splitted_line = line.rsplit("}",1)
        splitted_line2 = splitted_line[0].rsplit("{",1)
        line_part, chords = decode_lines(splitted_line2[0])
        line_part.append(splitted_line[1])
        chords.append(splitted_line2[1])
        return line_part, chords
    else:
        return [line], []

class Songbook:
    def __init__(self, title: str):
        self.title = title
        self.pdf = FPDF()

    def add_title_page(self) -> None:
        self.pdf.add_page()
        self.pdf.set_font("times", "", 60)
        self.pdf.cell(0, 10, self.title, align="C")
        log.info(f"added Title Page with Title:{self.title}")
    def add_filler_page(self) -> None:
        log.info("added filler page")
        self.pdf.add_page()

    def add_song(self, title: str, artist: str, verses: dict[str,str], scheme: list[str]) -> None:
        height = 20
        for verse in scheme:
            height += verses[verse].count("%") * 9 + 9
        log.debug(f"{height}/{self.pdf.eph}")
        
        if height > self.pdf.eph and self.pdf.page_no() % 2 == 0:
            self.add_filler_page()
        self.pdf.add_page()
        self.pdf.set_font("times", "", 40)
        self.pdf.cell(0, 10, title,)
        self.pdf.ln()
        log.debug(f"added title of {title}")
        self.pdf.set_font_size(20)
        if artist:
            self.pdf.cell(0,10,artist)
        self.pdf.ln()
        log.debug(f"verses:{scheme}")
        for verse in scheme:
            self.add_verse(verses[verse])
    def add_verse(self, verse: str) -> None:
        lines = verse.split("%")
        if self.pdf.get_y() + len(lines) * 9 > self.pdf.eph:
            self.pdf.add_page()
        for line in lines:
            line_parts, chords = decode_lines(line)
            log.debug(f"{chords = } {line_parts = }")
            self.pdf.set_font("times", size=14)
            final_text = ""
            for line_part, chord in zip(line_parts, chords):
                self.pdf.x += self.pdf.get_string_width(line_part)
                self.pdf.cell(10,4, text=chord)
                self.pdf.x -= 10
                final_text += line_part
            final_text += line_parts[-1]
            self.pdf.ln()
            self.pdf.cell(0,5,text=final_text)
            self.pdf.ln()

            
    def output(self, name: str) -> None:
        self.pdf.output(name)


if __name__ == "__main__":
    songbook = Songbook("Ameisenliederbuch")
    songbook.add_title_page()
    path = "/home/user/repos/songbook/Songs/1.0/"
    files = listdir(path)
    log.debug(files)
    for file in files:
        with open(path + file, "r") as f:
            song = json.load(f)
        songbook.add_song(song["meta"]["title"], song["meta"]["artist"], song["verses"], song["scheme"])
    songbook.output("tmp_test.pdf")
