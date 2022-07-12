#!/usr/bin/python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from pdf2image import convert_from_path
from pathlib import Path as path



app = QApplication([])
tmp_dir = (
	path.cwd()
	/	'tmp'
)



def openFile():
	global pdf_filename
	dialog = QFileDialog()
	pdf_filename = dialog.getOpenFileName()

	generatePDFImages(pdf_filename[0])

def generatePDFImages(filename):
	
	output_dir = tmp_dir

	images = convert_from_path(filename)

	for i, image in enumerate(images):
		file = output_dir / (str(i) + '.jpg')
		image.save(file)
	
	showPreview()

index = 0

def showPreview():
	preview.show()
	pixmap = QPixmap(str(tmp_dir) + '/' + str(index) + '.jpg')
	p_picture.setPixmap(pixmap)
	#app.resize(pixmap.width(), pixmap.height())

def nextImage():
	global index
	index += 1
	p_picture.pixmap.load(str(tmp_dir) + '/' + str(index) + '.jpg')

def prevImage():
	global index
	index -= 1
	p_picture.pixmap.load(str(tmp_dir) + '/' + str(index) + '.jpg')



if __name__ == '__main__':
	
	window = QWidget()

	layout = QVBoxLayout()
	top_buttom = QPushButton('select PDFs...')
	top_buttom.clicked.connect(openFile)
	layout.addWidget(top_buttom)

	window.setLayout(layout)
	window.show()

	preview = QWidget()
	p_layout = QVBoxLayout()
	b_next = QPushButton('next')
	b_next.clicked.connect(nextImage)

	b_prev = QPushButton('previous')
	b_prev.clicked.connect(prevImage)

	p_layout.addWidget(b_next)
	p_layout.addWidget(b_prev)

	p_picture = QLabel('img')
	p_layout.addWidget(p_picture)
	preview.setLayout(p_layout)
	
	app.exec()

	while True:
		pass