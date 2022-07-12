#!/usr/bin/python3
'''
merge two pdfs with the append() method.
'''

from PyPDF2 import PdfFileMerger
from pathlib import Path as path

if __name__ == '__main__':
	
	pdf_path = (
		path.cwd()	/
		'practice_files'
	)

	pdf_1 = pdf_path / 'merge1.pdf'
	pdf_2 = pdf_path / 'merge2.pdf'

	pdf_merger = PdfFileMerger()

	pdf_merger.append(str(pdf_1))
	pdf_merger.append(str(pdf_2))

	with open('concat.pdf', 'wb') as file_out:
		pdf_merger.write(file_out)