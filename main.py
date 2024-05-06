from fpdf import FPDF
import json
from loguru import logger as log
import sys
from os import listdir
log.remove()
log.add(sys.stderr, level="INFO")

def decode_lines(line: str):
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
    def __init__(self, title: str, font: str="helvetica"):
        self.title = title
        self.index = {}
        self.pdf = FPDF()
        self.font = font


    def add_title_page(self):
        self.pdf.add_page()
        self.pdf.set_font(self.font, "", 60)
        self.pdf.cell(0, 10, self.title, align="C")
        log.info(f"added Title Page with Title: {self.title}")
    def add_filler_page(self):
        log.info("added filler page")
        self.pdf.add_page()
    def add_song(self, title: str, artist: str, verses: dict, scheme: list):
        height = 20
        for verse in scheme:
            height += verses[verse].count("%") * 9 + 9
        log.debug(f"{height}/{self.pdf.eph}")
        
        if height > self.pdf.eph and self.pdf.page_no() % 2 == 0:
            self.add_filler_page()
        log.info(f"adding song {title} on page {self.pdf.page_no()}")
        self.index[title] = self.pdf.page_no()
        self.pdf.add_page()
        self.pdf.set_font(self.font, "", 30)
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
    def add_verse(self, verse: str):
        lines = verse.split("%")
        if self.pdf.get_y() + len(lines) * 9 > self.pdf.eph:
            self.pdf.add_page()
        for line in lines:
            line_parts, chords = decode_lines(line)
            log.debug(f"{chords = } {line_parts = }")
            self.pdf.set_font(self.font, size=14)
            final_text = ""
            for line_part, chord in zip(line_parts, chords):
                final_text += line_part
                self.pdf.x = 10 + self.pdf.get_string_width(final_text)
                self.pdf.cell(10,4, text=chord)
                self.pdf.x -= 10
            final_text += line_parts[-1]
            self.pdf.ln()
            self.pdf.cell(0,5,text=final_text)
            self.pdf.ln()
    def add_index(self):
        self.pdf.add_page()
        with self.pdf.table() as table:
            row = table.row()
            row.cell("Song")
            row.cell("Page")
            for song, page in self.index.items():
                row = table.row()
                row.cell(song)
                row.cell(str(page))

            
    def output(self, name: str):
        self.pdf.output(name)




def main():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    songbook = Songbook(settings["generator_settings"]["title"])
    songbook.add_title_page()
    files = listdir(settings["generator_settings"]["input_path"])
    log.debug(files)
    files.sort()
    for file in files:
        with open(settings["generator_settings"]["input_path"] + file, "r") as f:
            song = json.load(f)
        songbook.add_song(song["meta"]["title"], song["meta"]["artist"], song["verses"], song["scheme"])
    songbook.add_index()
    songbook.output(settings["generator_settings"]["output_path"])

if __name__ == "__main__":
    main()