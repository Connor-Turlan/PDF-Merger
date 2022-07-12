#!/usr/bin/python3
'''
rotate all the pages within a pdf.
'''

from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path as path

if __name__ == '__main__':
	
	pdf_path = (
		path.cwd()	/
		'practice_files'	/
		'split_and_rotate.pdf'
	)

	pdf_reader = PdfFileReader(str(pdf_path))
	pdf_writter = PdfFileWriter()

	for page in pdf_reader.pages:
		page.rotateCounterClockwise(90)
		pdf_writter.addPage(page)

	with open('rotated.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)