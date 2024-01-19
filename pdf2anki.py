import PyPDF2
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_PDF_NAME = 'linux-commands-handbook.pdf'
DEFAULT_FLASHCARDS_NAME = 'flashcards.txt'

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# Example:
# export PDF_FILE_PATH=/path/to/your/pdf.pdf
# export FLASHCARDS_FILE_PATH=/path/to/your/flashcards.txt
PDF_FILE_PATH = os.getenv("PDF_FILE_PATH", os.path.join(ROOT_DIRECTORY, 'SOURCE_DOCUMENTS', DEFAULT_PDF_NAME))
FLASHCARDS_FILE_PATH = os.getenv("FLASHCARDS_FILE_PATH", os.path.join(ROOT_DIRECTORY, DEFAULT_FLASHCARDS_NAME))

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    return text

def divide_text(text, section_size):
    sections = []
    start = 0
    end = section_size
    while start < len(text):
        section = text[start:end]
        sections.append(section)
        start = end
        end += section_size
    return sections


def create_anki_cards(pdf_text,batch_size=5):

    SECTION_SIZE = 1000
    divided_sections = divide_text(pdf_text, SECTION_SIZE)
    generated_flashcards = ' '
    open("flashcards.txt", "w", encoding='utf-8').close()
    for i, text in enumerate(divided_sections):
        if i % batch_size == 0:
            print(f"Processing batch starting with section {i}")
            # Reset generated_flashcards for each batch
            generated_flashcards = ''
        
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Create anki flashcards with the provided text using a format: question (at the end add semicolon);answer next line. Then new like again question;answer etc. The questions and answers must be meaninful , person who reads them should get overall understanding what is in the provided text. Keep question first and then the  corresponding answer on the same line {text}"}
                ]

            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages, 
                temperature =0.3,
                max_tokens=1000)
            
            response_from_api = response.choices[0].message.content
            generated_flashcards += response_from_api
                       
        except Exception as e:
            print(f"An error occurred in section {i}: {e}")
            
        if i % batch_size == batch_size - 1 or i == len(divided_sections) - 1:
            print(f"Completed processing up to section {i}")

            with open("flashcards.txt", "a", encoding='utf-8') as f:
                f.write(generated_flashcards)

    print("Finished generating flashcards")

if __name__ == "__main__":

    if not os.path.exists(PDF_FILE_PATH):
        print(f"Error: PDF file not found at {PDF_FILE_PATH}")
    else:
        pdf_text = read_pdf(PDF_FILE_PATH)
        create_anki_cards(pdf_text)