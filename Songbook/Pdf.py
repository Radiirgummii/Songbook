from fpdf import FPDF
from typing import Any
class Pdf(FPDF):
    def __init__(self) -> None:
        self.print_page_number = True
        self.pagenumber = 1
        super().__init__()
    
    def footer(self) -> None:
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        if self.print_page_number:
            self.cell(0, 10, str(self.pagenumber), align="C")
            self.pagenumber += 1