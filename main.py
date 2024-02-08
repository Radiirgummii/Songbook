from fpdf import FPDF

class Songbook:
    def __init__(self, title: str): 
        self.title = title
        self.pdf = FPDF()
    def add_title_page(self):
        self.pdf.add_page()
        self.pdf.set_font("times", "", 60)
        self.pdf.cell(0, 10, self.title, 0, 0, "C")
    def output(self, name: str):
        self.pdf.output(name)


if __name__ == "__main__":
    songbook = Songbook("Ameisenliederbuch")
    songbook.add_title_page()
    songbook.output("tmp_test.pdf")
