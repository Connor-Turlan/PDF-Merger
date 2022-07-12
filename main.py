#!/usr/bin/python3
'''
rotate all the pages within a pdf.
'''

from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pathlib import Path as path
import sys


stack = []


# open a pdf and push it to the stack.
def openPDF(args):
	if len(args) != 2:
		print('read requires 1 argument. open [filename]')
		return 1

	filename = str(args[1])
	try:
		reader = PdfFileReader(filename)
		stack.append(reader)

		print('%s openned successfully!' % filename)
	except FileIOException:
		print('error openning file: %s.' % filename)

def writePDF(args):
	if len(args) != 2:
		print('write requires 1 argumene. save [filename]')
		return 1
	
	if len(stack) < 1:
		print('no items on stack to write!')
		return 1

	filename = str(args[1])
	writer = PdfFileWriter()
	file = stack.pop()
	writer.appendPagesFromReader(file)
	with open(filename, 'wb') as file_out:
		writer.write(file_out)
	
	print('%s saved successfully!' % filename)

def saveAllPDFs(args):
	if len(args) < 1:
		print('idfk what went wrong...')
		return
	
	prefix = args[1] if len(args) > 1 else ''
	
	for i in range(len(stack)):
		filename = prefix + str(i) + '.pdf'
		writePDF(('save', filename))

def mergePDF(args):
	if len(stack) < 2:
		print('not enough files on stack to merge.')
		return 1

	merger = PdfFileWriter()
	for file in stack[-2:]:
		merger.appendPagesFromReader(file)
	
	del stack[-2:]
	stack.append(merger)
	
	print('merged successfully!')

def mergeAllPDF(args):
	while len(stack) > 1:
		mergePDF(args)

def extractPages(args):
	if len(args) < 3:
		print('not enough args to extract pages.')
	
	pass

def insertPDF(args):
	if len(args) < 2:
		print('not enough args for insert. insert [index] ([len])')

	file, insert = stack[-2:]
	
	index = int(args[1])

	pdf_writter = PdfFileWriter()
	pdf_writter.appendPagesFromReader(file)

	for i in range(insert.getNumPages()):
		page = insert.getPage(i)
		pdf_writter.insertPage(page, index + i)
	
	del stack[-2:]
	stack.append(pdf_writter)

	print('pdf inserted successfully!')

def splitPDFeveryN(n):
	# pop the most recent file.
	file = stack.pop()

	# iterate over every page splitting after every n-th page.
	substack = []
	for i in range(file.getNumPages()):
		page = file.getPage(i)

		if i % n == 0:
			substack.append(PdfFileWriter())
			pdf_writter = substack[-1]
		
		pdf_writter.addPage(page)
	
	# reverse the substack and extend the stack.
	substack.reverse()
	stack.extend(substack)

def splitPDFafterN(n):
	# pop the most recent file.
	file = stack.pop()

	# iterate over every page splitting after every n-th page.
	substack = []
	for i in range(file.getNumPages()):
		page = file.getPage(i)

		if i == 0 or i in n:
			substack.append(PdfFileWriter())
			pdf_writter = substack[-1]
		
		pdf_writter.addPage(page)
	
	# reverse the substack and extend the stack.
	substack.reverse()
	stack.extend(substack)

def splitPDF(args):
	if len(args) < 2:
		print('not enough args to split pdf.')
		return 1
	
	if args[1] == 'every':
		n = 1 if len(args) < 3 else int(args[2])
		splitPDFeveryN(n)
	elif args[1] == 'after':
		splitPDFafterN([int(n) for n in args[2:]])

def encryptPDF(args):
	if len(args) < 2:
		print('not enough arguments. encrypt [user_password] ([owner_password])')
		return 1

	stack[-1].encrypt(user_pwd=args[1])

def decryptPDF(args):
	if len(args) < 2:
		print('not enough arguments. encrypt [user_password] ([owner_password])')
		return 1

	status = stack[-1].decrypt(password=args[1])

	if status == 0:
		print('incorrect password.')
	elif status == 1:
		print('user password accepted.')
	elif status == 2:
		print('owner password accepted.')
	return status

def printStack(args):
	print('%d items on the stack.' % len(stack))
	print('START')
	for item in stack:
		print(item)
	print('END')

def printHelp(args):
	print(', '.join(list(commands.keys())))

def parseFile(args):
	if len(args) < 2:
		print('not enough arguments.')
		return 1
	
	filename = args[1]

	print('reading commands from file: %s' % filename)
	with open(filename) as file:
		for line in file:
			parseLine(line.strip())


commands = {
	'run':	parseFile,
	'open':	openPDF,
	'save':	writePDF,
	'save-all':	saveAllPDFs,
	'insert':	insertPDF,
	'merge':	mergePDF,
	'split':	splitPDF,
	'extract':	extractPages,
	'encrypt':	encryptPDF,
	'decrypt':	decryptPDF,
	'help':	printHelp,
	'stack':	printStack,
	'exit':	exit
}


def parseLine(line):
	args = line.split()
	if args[0] in commands:
		commands[args[0]](args)
	else:
		print('unknown command, for available commands type "help"')



if __name__ == '__main__':
	print('pdf merger.py')

	# if a file was read from the 
	if len(sys.argv) > 1:
		parseFile(sys.argv)

	line = input('>_ ')
	while line:
		parseLine(line)
		line = input('>_ ')
