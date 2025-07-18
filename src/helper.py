import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # Load environment variables from .env file

# Load the GROQ_API_KEY from environment variables
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set")

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)


def extract_text_from_pdf(pdf):
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.
    """

    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    # doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text


def ask_groq(prompt, max_tokens=1000):
    """
    Send a prompt to the Groq API and return the response.

    Args:
        prompt (str): The prompt to send to the Groq API.

    Returns:
        str: The response from the Groq API.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_completion_tokens=max_tokens,
        top_p=1,
        stop=None,
    )

    response = completion.choices[0].message.content
    return response

    # Placeholder for Groq API call
    # Implement the actual API call here


if __name__ == "__main__":
    # Example usage
    pdf_path = "example.pdf"  # Replace with your PDF file path
    try:
        text = extract_text_from_pdf(pdf_path)
        print("Extracted Text:", text)

        prompt = "What is the main topic of the document?"
        response = ask_groq(prompt)
        print("Groq Response:", response)
    except Exception as e:
        print(f"An error occurred: {e}")
