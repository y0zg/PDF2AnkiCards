# PDF to Anki Card generator

The PDF to Anki Card Generator is designed to convert text from PDF files into Anki flashcards. It processes the PDF content in chunks and utilizes OpenAI's GPT models to generate question-answer pairs suitable for flashcard-based learning.

# Environment Setup
In order to set your environment up to run the code here, first install all requirements:

## Install Dependencies
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configure OpenAPI Key
```shell
export OPENAI_API_KEY=your_api_key_here
```

## Set Custom File Paths (Optional)

```shell
export PDF_FILE_PATH=/path/to/your/pdf.pdf
export FLASHCARDS_FILE_PATH=/path/to/your/flashcards.txt
```

# Generating Flash Cards

1. Prepare PDF File: Place your PDF file(s) in the SOURCE_DOCUMENTS folder. If you've set a custom PDF_FILE_PATH, ensure your PDF is located at that path.

2. Run the Script `python pdf2anki.py`

3. Import generated txt file into Anki

# Important Notes
- The script divides the PDF into smaller chunks for processing. Depending on the length and complexity of your PDF, the script may take some time to execute.
- The format of generated flashcards depends on the responses from the OpenAI API. You might need to adjust the prompts or post-process the output for your specific needs.
- Ensure your OpenAI API key has sufficient quota and permissions for GPT model usage.
