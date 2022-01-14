import qrcode
import json
from PyPDF2 import PdfFileWriter, PdfFileReader
import fitz
import os
import math
import barcode
from barcode.writer import ImageWriter


def split_files():
	f = open('50000_barcodes_1_05_2022.json')
	data = json.load(f)

	# 99 for 100 barcodes
	num_in_file = 100
	pdf_page = 1
	codes = []

	for index, i in enumerate(data):

		codes.append(i)
		
		if (index+1) % num_in_file == 0:

			o = open('output/V_json/QR_V_batch_' + str(pdf_page) + '.json', 'w') 
			json.dump(codes, o)
			pdf_page += 1
			codes = []

def V_to_pdf_multiple():
	file_number, footer_page  = 1,1 
	# in_dir = 'output/V_json/'
	# out_dir = 'F:/Microbiology_forms/MSBI/Verbosity/V_Barcode/'
	in_dir = 'output/test/'
	out_dir = 'output/test/'
	#get all files in this directory
	for filename in os.listdir(in_dir):
			x, y = 0, 0 

			if ".json" in filename:
				f = open(in_dir	 + filename)
				data = json.load(f)
				input_file = "x50.pdf"
				file1 = PdfFileReader(open(input_file, "rb"))
				output = PdfFileWriter()

				#calculate # of pages needed and append template page #s
				pages = math.ceil(len(data)/50)
				for page in range(0,pages):
					output.addPage(file1.getPage(0))

				outputStream = open(out_dir + "V_Barcode_PDF_" + str(file_number) + '.pdf', "wb")

				output.write(outputStream)
				outputStream.close()
				file_handle = fitz.open(outputStream)

				#page incrementing
				pdf_page = 0 
				
				# item count and value in the json file 
				for index, i in enumerate(data):

					if index != 0 and index % 50 == 0 :
						pdf_page += 1
						footer_page += 1

					options = {
		    			'module_height': 12,
					    'quiet_zone': 1,
					    'text_distance': 1,
					    'font_size': 12
					    }	

					png = i + '.png'
					first_page = file_handle[pdf_page]	
					code = barcode.get('code128', i,  writer = ImageWriter())
					filename = code.save(i, options = options)

					if index != 0 and index % 5 == 0:
						y =(72*math.floor((index - (50*pdf_page)) / 5))
						x = 0 + index % 5

					image_rectangle = fitz.Rect(-10+(115*x) ,46 + y , 205+(100*x), 106 + y)
					first_page.insert_image(image_rectangle, filename=png)
					first_page.insert_text(point = ('50','780'), text='Filename: V_Barcode_PDF_' + str(file_number), fontsize=10, fontfile=None, fontname = "Times-Roman", color=None, fill=None, render_mode=0, border_width=1, rotate=0, morph=None, stroke_opacity=0.5, fill_opacity=0.5, overlay=True, oc=0)
					first_page.insert_text(point = ('500','780'), text= 'Page: ' + str(footer_page), fontsize=10, fontfile=None, fontname = "Times-Roman", color=None, fill=None, render_mode=0, border_width=1, rotate=0, morph=None, stroke_opacity=0.5, fill_opacity=0.5, overlay=False, oc=0)
			
					x += 1
					os.remove(png)

				file_handle.saveIncr()

				# incrementing file number for QR PDF
				file_number += 1 	
				footer_page += 1

def qr_to_pdf_multiple():
	file_number, footer_page  = 1,1 

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

		outputStream = open("output/V_QR/V_QR_PDF_" + str(file_number) + '.pdf', "wb")
		output.write(outputStream)
		outputStream.close()
		file_handle = fitz.open(outputStream)

		#page incrementing
		pdf_page = 0 

		# item count and value in the json file 
		for index, i in enumerate(data):
					
			if index != 0 and index % 10 == 0 :
				pdf_page += 1		

			first_page = file_handle[pdf_page]	
			
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
			first_page.insert_text(point = ('50','780'), text='Filename: V_Barcode_PDF_' + str(file_number), fontsize=10, fontfile=None, fontname = "Times-Roman", color=None, fill=None, render_mode=0, border_width=1, rotate=0, morph=None, stroke_opacity=0.5, fill_opacity=0.5, overlay=True, oc=0)
			first_page.insert_text(point = ('500','780'), text= 'Page: ' + str(footer_page), fontsize=10, fontfile=None, fontname = "Times-Roman", color=None, fill=None, render_mode=0, border_width=1, rotate=0, morph=None, stroke_opacity=0.5, fill_opacity=0.5, overlay=False, oc=0)
			os.remove(png)
			
		file_handle.saveIncr()

		# incrementing file number for QR PDF
		file_number += 1 
		footer_page += 1
		
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
