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
		'top_secret.pdf'
	)

	pdf_reader = PdfFileReader(str(pdf_path))
	pdf_writter = PdfFileWriter()

	pdf_writter.appendPagesFromReader(pdf_reader)

	pdf_writter.encrypt(user_pwd='Unguessable')

	with open('top_secret_encrypted.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)