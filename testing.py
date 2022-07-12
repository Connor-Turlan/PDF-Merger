#!/usr/bin/python3

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pathlib import Path as path
import copy

def OpeningAPDF():
	# set the pdf path.
	pdf_path = (
		"example.pdf"
	)

	# load the pdf object.
	pdf = PdfFileReader(str(pdf_path))

	# output the pdf's details.
	print('document has:', pdf.getNumPages())
	print(pdf.documentInfo)
	print('document title:', pdf.documentInfo.title)

	# get the text from the first page.
	first_page = pdf.getPage(0)
	print(first_page.extractText())


def ExtractingPages():
	# create the pdf writter class and create a blank page that is a 1 inch square.
	pdf_writter = PdfFileWriter()
	page = pdf_writter.addBlankPage(width=72, height=72)

	# write the file to disk.
	with open('blank.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)

	pdf_path = 'practice_files/Pride_and_Prejudice.pdf'
	input_pdf = PdfFileReader(str(pdf_path))


	# add pages with iterative enumeration.
	pdf_writter = PdfFileWriter()
	
	for n in range(1, 4):
		page = input_pdf.getPage(n)
		pdf_writter.addPage(page)

	with open('firstpage.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)

	# add pages with slice notation.
	pdf_writter = PdfFileWriter()

	for page in input_pdf.pages[1:4]:
		pdf_writter.addPage(page)
	
	with open('first_chapter.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)


	# get the last page of pride and prejudice.
	pdf_writter = PdfFileWriter()

	page = input_pdf.pages[-1]
	#page = input_pdf.getPage(input_pdf.getNumPages()-1)
	pdf_writter.addPage(page)
	
	with open('lastPage.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)


def ConcatPDFs():
	# cat with append.
	reports_dir = path('practice_files/expense_reports')
	reports = list(reports_dir.glob('*.pdf'))
	reports.sort()
		
	pdf_merger = PdfFileMerger()

	for report in reports:
		pdf_merger.append(str(report))

	with open('append_merged.pdf', 'wb') as file_out:
		pdf_merger.write(file_out)



def MergingPDFs():
	# get current directory.
	reports_dir = (
		path.cwd()	/
		'practice_files'	/
		'quarterly_report'
	)
	
	report_path = reports_dir / 'report.pdf'
	toc_path = reports_dir / 'toc.pdf'
	
	# prime the merging class
	pdf_merger = PdfFileMerger()
	
	pdf_merger.append(str(report_path))

	# insert the toc as the 1-th page, then write to file.
	pdf_merger.merge(1, str(toc_path))

	with open('full_report.pdf', 'wb') as file_out:
		pdf_merger.write(file_out)


def RotatePages():
	pdf_path = (
		path.cwd()	/
		'practice_files'	/
		'ugly.pdf'
	)

	pdf_reader = PdfFileReader(str(pdf_path))
	pdf_writter = PdfFileWriter()

	# naive approach.
	""" for i in range(pdf_reader.getNumPages()):
		page = pdf_reader.getPage(i)
		if i % 2 == 0:
			page.rotateClockwise(90)
		pdf_writter.addPage(page) """
	
	# informed approach.
	for page in pdf_reader.pages:
		if page['/Rotate'] == -90:
			page.rotateClockwise(90) 
		pdf_writter.addPage(page)
	
	with open('ugly_rotated.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)


def CropPages():
	pdf_path = (
		path.cwd()	/
		'practice_files'	/
		'half_and_half.pdf'
	)

	pdf_writter = PdfFileWriter()
	pdf_reader = PdfFileReader(str(pdf_path))

	first_page = pdf_reader.getPage(0)
	left_side = copy.deepcopy(first_page)

	current_coords = left_side.mediaBox.upperRight
	current_coords = (current_coords[0] / 2, current_coords[1])

	left_side.mediaBox.upperRight = current_coords

	right_side = copy.deepcopy(first_page)

	right_side.mediaBox.upperLeft = current_coords

	pdf_writter.addPage(left_side)
	pdf_writter.addPage(right_side)

	with open('cropped_pages.pdf', 'wb') as file_out:
		pdf_writter.write(file_out)


def EncryptPDF():
	pdf_path = (
		path.cwd()	/
		'practice_files'	/
		'newsletter.pdf'
	)

	pdf_reader = PdfFileReader(str(pdf_path))

	pdf_writter = PdfFileWriter()
	pdf_writter.appendPagesFromReader(pdf_reader)

	pdf_writter.encrypt(user_pwd='SuperSecret', owner_pwd='ReallySuperSecret')

	output_path = path.cwd() / 'newsletter_protected.pdf'
	with output_path.open(mode='wb') as file_out:
		pdf_writter.write(file_out)


def DecryptPDF():
	pdf_path = (
		path.cwd()	/
		'newsletter_protected.pdf'
	)

	pdf_reader = PdfFileReader(str(pdf_path))

	# rtn 0 if incorrect, 1 if user, 2 if owner.
	print(pdf_reader.decrypt(password='ReallySuperSecret'))

	print(pdf_reader.getPage(0))


if __name__ == '__main__':
	#ExtractingPages()
	#MergingPDFs()
	#RotatePages()
	#CropPages()
	#EncryptPDF()
	DecryptPDF()