import io
from pypdf import PdfReader
from docx import Document


def extract_text_from_resume(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        pdf = PdfReader(io.BytesIO(uploaded_file.getvalue()))

        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif file_name.endswith(".docx"):
        document = Document(
            io.BytesIO(uploaded_file.getvalue())
        )

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    else:
        return ""
