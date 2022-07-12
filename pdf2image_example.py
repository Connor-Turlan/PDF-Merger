#!/usr/bin/python3

from pdf2image import convert_from_path
from pathlib import Path as path

if __name__ == '__main__':
	pdf_path = (
		path.cwd()	/
		'full_report.pdf'
	)

	out_path = (
		path.cwd()	/
		'full_report'
	)

	images = convert_from_path(str(pdf_path))

	for i, image in enumerate(images):
		path = out_path / (str(i) + '.jpg')
		image.save(path, 'JPEG')

	print('done!')
	while True:
		pass