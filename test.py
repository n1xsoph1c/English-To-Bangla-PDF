from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from deep_translator import GoogleTranslator
import tempfile
import PyPDF2
from converter import Unicode

def translate_pdf(input_pdf, output_pdf, source_lang, target_lang):
    # Initialize the translator
    translator = GoogleTranslator(source=source_lang, target=target_lang)

    # Register the font with ReportLab
    pdfmetrics.registerFont(TTFont('SutonnyMJ Regular', 'ANSI.ttf'))  # Replace 'Font.ttf' with the actual font file path

    # Create a PdfFileWriter object to write the translated content to the output PDF file
    writer = PyPDF2.PdfFileWriter()
    test = Unicode()

    # Open the input PDF file
    with open(input_pdf, 'rb') as input_stream:
        # Create a PdfFileReader object to read the content from the input PDF file
        reader = PyPDF2.PdfFileReader(input_stream)

        # Loop through each page
        for page_num in range(5):
            print(f"Working on page {page_num} / {5}")

            # Extract and translate the text from the page
            text = reader.getPage(page_num).extractText()
            translated_text = translator.translate(text)

            # Create a temporary PDF file to store the translated text
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Create a PDF canvas with the same size as the original page
                c = canvas.Canvas(temp_file.name, pagesize=letter)
                # Set the font and encoding
                c.setFont("SutonnyMJ Regular", 12)

                # Use ReportLab's Paragraph to apply formatting
                styles = getSampleStyleSheet()
                paragraph_style = ParagraphStyle('CustomStyle', parent=styles['Normal'], fontName='SutonnyMJ Regular', fontSize=12)
                te = translated_text.split("\n")
                # Convert the translated text to Bijoy format
                for t in range(len(te)):
                    bijoy_text = test.convertUnicodeToBijoy(te[t])
                    formatted_text = Paragraph(bijoy_text, paragraph_style)

                     # Draw the formatted text on the canvas
                    formatted_text.wrapOn(c, 400, 100)
                    formatted_text.drawOn(c, 50, 750 - (16 * t))

                # Save the canvas
                c.save()
                
                # Create a new PdfFileReader object for the temporary PDF file
                temp_reader = PyPDF2.PdfFileReader(open(temp_file.name, 'rb'))
                new_page = reader.getPage(page_num)
                temp_reader.getPage(0).merge_page(new_page)

                # Add the new page to the translated PDF
                writer.addPage(temp_reader.getPage(0))
                
                # Save the translated PDF to a file
                with open(output_pdf, 'wb') as output_stream:
                    writer.write(output_stream)
                

            print(f" √ Done working on page {page_num + 1} / {reader.numPages}")
            print(f"BEFORE: \n{text}\nAFTER:{translated_text}\n")



    # Remove the temporary PDF file
    tempfile.NamedTemporaryFile().close()

input_pdf = 'Lecture_1.pdf'
output_pdf = 'output.pdf'
source_lang = 'en'
target_lang = 'bn'
translate_pdf(input_pdf, output_pdf, source_lang, target_lang)

# from fpdf import FPDF
# from deep_translator import GoogleTranslator
# import tempfile
# import PyPDF2

# def translate_pdf(input_pdf, output_pdf, source_lang, target_lang):
#     # Initialize the translator
#     translator = GoogleTranslator(source=source_lang, target=target_lang)

#     # Create an FPDF object
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # Set font with UTF-8 support (replace 'path/to/Bengali.ttf' with the actual path)
#     pdf.add_font("Bengali", '', 'kalpurush.ttf', uni=True)
#     pdf.set_font("Bengali", size=12)

#     # Open the input PDF file
#     with open(input_pdf, 'rb') as input_stream:
#         # Create a PdfFileReader object to read the content from the input PDF file
#         reader = PyPDF2.PdfFileReader(input_stream)

#         # Loop through each page
#         for page_num in range(5):
#             print(f"Working on page {page_num + 1} / {5}")

#             # Extract and translate the text from the page
#             text = reader.getPage(page_num).extractText()
#             translated_text = translator.translate(text)

#             # Add translated text to the PDF
#             pdf.multi_cell(0, 10, translated_text)

#             print(f" √ Done working on page {page_num + 1} / {reader.numPages}")
#             print(f"BEFORE: \n{text}\nAFTER:{translated_text}\n")

#     # Output the translated PDF to a file
#     pdf.output(output_pdf)

# input_pdf = 'Lecture_1.pdf'
# output_pdf = 'output.pdf'
# source_lang = 'en'
# target_lang = 'bn'
# translate_pdf(input_pdf, output_pdf, source_lang, target_lang)
