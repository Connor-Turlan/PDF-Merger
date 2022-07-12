#!/usr/bin/python3

from PyPDF2 import PdfFileReader
from pathlib import Path as path

if __name__ == '__main__':
	
	# set the pdf path.
	pdf_path = (
		"creating-and-modifying-pdfs/practice_files/zen.pdf"
	)

	# load the pdf object.
	pdf = PdfFileReader(str(pdf_path))

	first_page = pdf.getPage(0)
	print(first_page.extractText())