from google.genai import types
from google import genai
import pathlib
import os
import mimetypes

def pdf_summarize_gemini(file_path):
    """
    Summarizes a PDF document using Gemini.

    Args:
        file_path: Path to the PDF file.

    Returns:
        The summarized text in HTML format, or None if an error occurs.  Prints error messages to the console.
    """

    try:
        client = genai.Client(api_key=os.environ['GEMINI_KEY'])

        # Determine MIME type (important for Gemini to handle PDFs correctly)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None or not mime_type.startswith('application/pdf'):
            print(f"Error: File '{file_path}' is not a PDF.")
            return None


        with open(file_path, "rb") as pdf_file:
            sample_file = client.files.upload(file=pdf_file, mime_type=mime_type)  # Explicitly set mime type

            prompt = f"Summarize this document, focusing on the key arguments and conclusions. Provide a summary of no more than 300 words. I want the output to be in the format of HTML."

            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Or another suitable Gemini model
                contents=[sample_file, prompt]
            )
            return response.text

    except Exception as e:
        print(f"An error occurred: {e}")  # Print specific error message
        return None



