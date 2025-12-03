from chatbot import *
from pdf_creater import *
from pdf_loader import *
from csv_creater import CSV_Creater
from config import *
import os


class DocuQuizAI:
    def __init__(self, pdf_files:list, reset_vectorstore:bool=True):
        # Don't create the Chatbot until we have a token_count from the PDF loader
        self.pdf_files = pdf_files
        self.reset_vectorstore = reset_vectorstore
        self.bot = None
        self.token_count = None

    def quiz_creater(self, token_count):
        query = "Make me a quiz based on the document." 
        response = self.bot.query(query, token_count)
        print("Answer:", response)
        return response
    
    def pdf_loader(self):
        choose_pic_pdf = input("Is your file an picture or PDF? (pic/pdf/exit): ")
        if choose_pic_pdf.lower() not in ['pic', 'pdf', 'exit']:
            print("Invalid choice. Please enter 'pic', 'pdf', or 'exit'.")
            return None
        elif choose_pic_pdf.lower() == 'exit':
            exit()

        elif choose_pic_pdf.lower() == 'pdf':
            file_path = select_file_path('pdf')
            pdf_loader_class = PDFLoader(
                pdf_path=file_path,
                file_path=file_path,   # <-- point to the actual PDF file
                tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                output_pdf_path=r"data_sets\document.pdf",
                pdf_or_pic = 'pdf'
            )
            choose_service = input("Is your PDF computer based (meaning no pictures or/and handwritten texts)? (y/n/exit): ")

            # OCR AND GOOGLE VISION ARE USED HERE
            if choose_service.lower() == 'n':
                print("Using OCR and Google Vision AI to extract text from PDF...")
                text, token_count = pdf_loader_class.extract_text_ocr(prefer_google_vision=True)
                # Implement OCR extraction and PDF conversion here
                pdf_loader_class.text_to_pdf(text)
                return text, token_count


            # TESSERACT IS USED HERE and DIRECT EXTRACTION IS USED HERE
            elif choose_service.lower() == 'y':
                # For PDFs with embedded text, use direct extraction (much more accurate)
                # if choose_pic_pdf.lower() == 'pdf':
                #     text, token_count = pdf_loader_class.extract_text_direct(file_path)
                # else:
                #     # For image files, use Tesseract
                #     text, token_count = pdf_loader_class.extract_text_tesseract()
                print("Using direct text extraction from PDF...")
                text, token_count = pdf_loader_class.extract_text_direct(file_path)
                pdf_loader_class.text_to_pdf(text)
                return text, token_count
            
            elif choose_service.lower() == 'exit':
                exit()
            else: 
                exit()



        elif choose_pic_pdf.lower() == 'pic':
            file_path = select_file_path('pic')
            turn_into_pdf = input("Do you want to convert the picture into a PDF for maxinium accuracy? (y/n): ")
            if turn_into_pdf.lower() == 'y':
                turning_test = convert_pics_to_pdf(file_path, r"pdf_and_pics\docuquiz-ai-user-pdf.pdf")
                print(turning_test)
            elif turn_into_pdf.lower() == 'n':
                print("Sorry, DocuQuiz AI requires a PDF or picture converted to PDF to proceed.")
                exit()
            
            pdf_loader_class = PDFLoader(
                pdf_path=r"pdf_and_pics\docuquiz-ai-user-pdf.pdf",
                file_path=r"pdf_and_pics\docuquiz-ai-user-pdf.pdf",   # <-- point to the actual PDF file
                tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                output_pdf_path=r"data_sets\document.pdf",
                pdf_or_pic = 'pdf'
            )
            choose_service = input("Does your PDF have selectable computer based text (meaning no pictures or/and handwritten texts)? (y/n/exit): ")

            # OCR AND GOOGLE VISION ARE USED HERE
            if choose_service.lower() == 'n':
                print("Using OCR and Google Vision AI to extract text from PDF...")
                text, token_count = pdf_loader_class.extract_text_ocr(prefer_google_vision=True)
                # Implement OCR extraction and PDF conversion here
                pdf_loader_class.text_to_pdf(text)
                return text, token_count


            # TESSERACT IS USED HERE and DIRECT EXTRACTION IS USED HERE
            elif choose_service.lower() == 'y':
                # For PDFs with embedded text, use direct extraction (much more accurate)
                # if choose_pic_pdf.lower() == 'pdf':
                #     text, token_count = pdf_loader_class.extract_text_direct(file_path)
                # else:
                #     # For image files, use Tesseract
                #     text, token_count = pdf_loader_class.extract_text_tesseract()
                print("Using direct text extraction from PDF...")
                text, token_count = pdf_loader_class.extract_text_direct(file_path)
                pdf_loader_class.text_to_pdf(text)
                return text, token_count


        # Ingnore for Now!
        if choose_pic_pdf.lower() == 'pdf':
            file_path = select_file_path('pdf')
            pdf_loader_class = PDFLoader(
                pdf_path=file_path,
                file_path=file_path,   # <-- point to the actual PDF file
                tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                output_pdf_path=r"data_sets\document.pdf",
                pdf_or_pic = 'pdf'
            )
            choose_service = input("Is your PDF computer based (meaning no pictures or/and handwritten texts)? (y/n/exit): ")

            # OCR AND GOOGLE VISION ARE USED HERE
            if choose_service.lower() == 'google':
                text, token_count = pdf_loader_class.extract_text_ocr(prefer_google_vision=True)
                # Implement OCR extraction and PDF conversion here
                pdf_loader_class.text_to_pdf(text)
                return text, token_count
            # DIRECT EXTRACTION IS USED HERE

            # TESSERACT IS USED HERE
            elif choose_service.lower() == 'tes':
                # For PDFs with embedded text, use direct extraction (much more accurate)
                # if choose_pic_pdf.lower() == 'pdf':
                #     text, token_count = pdf_loader_class.extract_text_direct(file_path)
                # else:
                #     # For image files, use Tesseract
                #     text, token_count = pdf_loader_class.extract_text_tesseract()
                text, token_count = pdf_loader_class.extract_text_direct(file_path)
                pdf_loader_class.text_to_pdf(text)
                return text, token_count

        elif choose_pic_pdf.lower() == 'pic':
            file_path = select_file_path('pic')   
            pdf_loader_class = PDFLoader(
                pdf_path=file_path,
                file_path=file_path, 
                tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                output_pdf_path=r"data_sets\document.pdf",
                pdf_or_pic = 'pic'
            )
            
            choose_service = input("Do you want to use Tesseract or EasyOCR? (tes/ocr/exit): ")

            # OCR AND GOOGLE VISION ARE USED HERE
            if choose_service.lower() == 'ocr':
                text, token_count = pdf_loader_class.extract_text_ocr(prefer_google_vision=False)
                # Implement OCR extraction and PDF conversion here
                pdf_loader_class.text_to_pdf(text)
                return text, token_count
            # DIRECT EXTRACTION IS USED HERE

            # TESSERACT IS USED HERE
            elif choose_service.lower() == 'tes':
                # For PDFs with embedded text, use direct extraction (much more accurate)
                if choose_pic_pdf.lower() == 'pdf':
                    text, token_count = pdf_loader_class.extract_text_direct()
                else:
                    # For image files, use Tesseract
                    text, token_count = pdf_loader_class.extract_text_tesseract()
                pdf_loader_class.text_to_pdf(text)
                return text, token_count

        elif choose_pic_pdf.lower() == 'exit':
            exit()

    def pdf_creater(self, text_use):
        output_folder = select_output_pdf_path()
        if output_folder:
            # Combine folder path with filename
            output_pdf_path = os.path.join(output_folder, "docuquiz_quiz.pdf")
            pdf_creator = PDFCreator(
                output_pdf_path=output_pdf_path,
                logo_path=r"logo\docuquiz_logo_transparent.png",
                text=text_use,
            )
            pdf_creator.create_pdf_with_unicode_text()
            print(f"PDF saved to: {output_pdf_path}")
        else:
            print("No folder selected. PDF not saved.")
    
    def csv_creater(self, data):
        csv_creator = CSV_Creater()
        output_folder = select_output_pdf_path()
        if output_folder:
            # Combine folder path with filename
            output_csv_path = os.path.join(output_folder, "docuquiz_quiz.csv")
            csv_creator.create_csv(data, output_csv_path)
            print(f"CSV saved to: {output_csv_path}")
        else:
            print("No folder selected. CSV not saved.")
    
    def main(self):
        self.quiz_creater()

if __name__ == "__main__":
    # Create app (do not create Chatbot yet)
    app = DocuQuizAI(pdf_files=[r"data_sets\document.pdf"], reset_vectorstore=True)

    # Load the PDF (or image), convert to PDF and get text + token count
    result = app.pdf_loader()
    if result is None:
        print("No document loaded. Exiting.")
        exit()
    text_content, tokens_count = result

    choose_pdf_csv = input("Do you want to create a PDF or CSV? (pdf/csv): ")
    if choose_pdf_csv.lower() == 'csv':
        csv_or_pdf = 'csv'
        app.bot = Chatbot(app.pdf_files, app.reset_vectorstore, tokens_count, csv_or_pdf)
        app.bot.initialize()

        # Generate quiz using the actual token count
        quiz_text = app.quiz_creater(tokens_count)
        app.csv_creater(quiz_text)
    else:
        csv_or_pdf = 'pdf'
        app.bot = Chatbot(app.pdf_files, app.reset_vectorstore, tokens_count, csv_or_pdf)
        app.bot.initialize()

        # Generate quiz using the actual token count
        quiz_text = app.quiz_creater(tokens_count)
        app.pdf_creater(quiz_text)

    # Create Chatbot now that we have the token count

