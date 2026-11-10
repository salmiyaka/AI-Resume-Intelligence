import os
from pypdf import PdfReader


def read_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_txt(file_path):
    """
    Read text from a TXT resume.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def read_uploaded_resume(file_path):
    """
    Read a PDF or TXT resume.

    This is the main function used by app.py.
    """

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return read_pdf(file_path)

    elif extension == ".txt":

        return read_txt(file_path)

    else:

        raise ValueError(
            "Unsupported file format. "
            "Please use PDF or TXT."
        )