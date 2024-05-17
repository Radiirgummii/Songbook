from Songbook.Pdf import Pdf
from Songbook.logger import log
from Songbook.decode_lines import decode_lines


class Songbook:
    def __init__(self, title: str, font: str = "helvetica"):
        """This class represents a Songbook."""
        self.title = title
        self.index: dict[str, int] = {}
        self.pdf = Pdf()
        self.font = font

    def add_title_page(self) -> None:
        """this funktion adds a title Page to the Songbook with the title supplied to the initializer"""
        self.pdf.add_page()
        self.pdf.print_page_number = False
        self.pdf.set_font(self.font, "", 60)
        self.pdf.cell(0, 10, self.title, align="C")
        log.info(f"added Title Page with Title: {self.title}")

    def add_filler_page(self) -> None:
        log.info("added filler page")
        self.pdf.add_page()
        self.pdf.print_page_number = True


    def add_song(self, title: str, artist: str, verses: dict[str, str], scheme: list[str]) -> None:
        height = 20
        for verse in scheme:
            height += verses[verse].count("%") * 9 + 9
        log.debug(f"{height}/{self.pdf.eph}")

        if height > self.pdf.eph and self.pdf.page_no() % 2 == 0:
            self.add_filler_page()
        log.info(f"adding song {title} on page {self.pdf.pagenumber}")
        self.index[title] = self.pdf.pagenumber
        self.pdf.add_page()
        self.pdf.print_page_number = True
        self.pdf.set_font(self.font, "", 30)
        self.pdf.multi_cell(
            0,
            10,
            title,
        )
        self.pdf.ln()
        log.debug(f"added title of {title}")
        self.pdf.set_font_size(20)
        if artist:
            self.pdf.cell(0, 10, artist)
        self.pdf.ln()
        log.debug(f"verses:{scheme}")
        for verse in scheme:
            self.add_verse(verses[verse])

    def add_verse(self, verse: str) -> None:
        lines = verse.split("%")
        if self.pdf.get_y() + len(lines) * 9 > self.pdf.eph:
            self.pdf.add_page()
            self.pdf.print_page_number = True
        for line in lines:
            line_parts, chords = decode_lines(line)
            log.debug(f"{chords = } {line_parts = }")
            self.pdf.set_font(self.font, size=14)
            final_text = ""
            for line_part, chord in zip(line_parts, chords):
                final_text += line_part
                self.pdf.x = 10 + self.pdf.get_string_width(final_text)
                self.pdf.cell(10, 4, text=chord)
                self.pdf.x -= 10
            final_text += line_parts[-1]
            self.pdf.ln()
            self.pdf.cell(0, 5, text=final_text)
            self.pdf.ln()

    def add_index(self) -> None:
        self.pdf.add_page()
        self.pdf.print_page_number = False
        with self.pdf.table() as table:
            row = table.row()
            row.cell("Song")
            row.cell("Page")
            for song, page in self.index.items():
                row = table.row()
                row.cell(song)
                row.cell(str(page))

    def output(self, name: str) -> None:
        self.pdf.output(name)
