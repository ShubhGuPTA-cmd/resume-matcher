import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF resume."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return clean_text(text)

def clean_text(text):
    """Basic cleanup: lowercase, collapse whitespace."""
    text = text.lower()
    text = " ".join(text.split())
    return text

if __name__ == "__main__":
    resume_text = extract_text_from_pdf("sample_resume.pdf")
    print(resume_text[:500])  # preview first 500 chars