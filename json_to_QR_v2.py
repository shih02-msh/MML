import qrcode
import json
from PyPDF2 import PdfFileWriter, PdfFileReader
import fitz
import os
import math
import barcode
from barcode.writer import ImageWriter
import io

def split_files():
	f = open('50000_barcodes_1_05_2022.json')
	data = json.load(f)

	# 99 for 100 barcodes
	num_in_file = 100
	p = 1
	codes = []

	for index, i in enumerate(data):

		codes.append(i)
		
		if (index+1) % num_in_file == 0:

			o = open('output/V_json/QR_V_batch_' + str(p) + '.json', 'w') 
			json.dump(codes, o)
			p += 1
			codes = []

def V_to_pdf_multiple():
	c = 1

	#get all files in this directory
	for filename in os.listdir('output/test/'):

		f = open('output/test/' + filename)
		data = json.load(f)
		input_file = "x10.pdf"
		file1 = PdfFileReader(open(input_file, "rb"))
		output = PdfFileWriter()

		#calculate # of pages needed and append template page #s
		pages = math.ceil(len(data)/10)
		for page in range(0,pages):
			output.addPage(file1.getPage(0))

		outputStream = open("output/test/V_QR_PDF_" + str(c) + '.pdf', "wb")
		output.write(outputStream)
		outputStream.close()
		file_handle = fitz.open(outputStream)

		#page incrementing
		p = 0 

		# item count and value in the json file 
		for index, i in enumerate(data):
					
			if index != 0 and index % 10 == 0 :
				p += 1		

			first_page = file_handle[p]	
			fp = io.BytesIO()
			barcode.generate('code128', i, writer=ImageWriter(), output=fp)

			#x-left, y-up, x-right, y-down
			if index % 2 == 0:
				x = [190,280]
			else:
				x = [490,580]
			
			y = int(145 * math.floor((index%10) / 2))
			
			image_rectangle = fitz.Rect(x[0],60+y,x[1],150+y)
			first_page.insert_image(image_rectangle, stream=fp)
		
		file_handle.saveIncr()

		# incrementing file number for QR PDF
		c += 1 

def qr_to_pdf_multiple():
	c = 1

	#get all files in this directory
	for filename in os.listdir('output/V_json/'):

		f = open('output/V_json/' + filename)
		data = json.load(f)
		input_file = "x10.pdf"
		file1 = PdfFileReader(open(input_file, "rb"))
		output = PdfFileWriter()

		#calculate # of pages needed and append template page #s
		pages = math.ceil(len(data)/10)
		for page in range(0,pages):
			output.addPage(file1.getPage(0))
			# output.addPage(first_page)

		outputStream = open("output/V_QR/V_QR_PDF_" + str(c) + '.pdf', "wb")
		output.write(outputStream)
		outputStream.close()
		file_handle = fitz.open(outputStream)

		#page incrementing
		p = 0 

		# item count and value in the json file 
		for index, i in enumerate(data):
					
			if index != 0 and index % 10 == 0 :
				p += 1		

			first_page = file_handle[p]	
			
			img = qrcode.make(i)
			img.save(i+'.png')
			png = i + '.png'
			
			#x-left, y-up, x-right, y-down
			if index % 2 == 0:
				x = [190,280]
			else:
				x = [490,580]
			
			y = int(145 * math.floor((index%10) / 2))
			
			image_rectangle = fitz.Rect(x[0],60+y,x[1],150+y)
			first_page.insert_image(image_rectangle, filename=png)
			os.remove(png)
		
		file_handle.saveIncr()

		# incrementing file number for QR PDF
		c += 1 

def qr_to_pdf_single():
	#single PDFs
	f = open('SAMPLE_QR_CODES.json')
	data = json.load(f)
	input_file = "test.pdf"

	for i in data:
		img = qrcode.make(i)
		img.save(i+'.png')
		
		output_file = i + ".pdf"
		png = i + '.png'
		img = qrcode.make(i)
		img.save(i + '.png')
		image_rectangle = fitz.Rect(850,190,1350,690)

		# retrieve the first page of the PDF
		file_handle = fitz.open(input_file)
		first_page = file_handle[0]

		# add the image
		first_page.insert_image(image_rectangle, filename=png)
		file_handle.save(output_file)
		os.remove(png)

if __name__ == '__main__':
	V_to_pdf_multiple()
