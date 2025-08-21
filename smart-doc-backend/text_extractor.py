import os
import base64
import logging
import pytesseract
import pdfplumber
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

# ---------- Setup ----------
load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or exit("OPENAI_API_KEY missing"))

# Tesseract path (Windows only - adjust if needed)
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

logger = logging.getLogger("text_extractor")
logger.setLevel(logging.INFO)


# ---------- AI extraction for Images ----------
def extract_with_ai(file_path: str) -> str:
    """Try AI-based OCR (OpenAI Vision)."""
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an OCR assistant. Extract all visible text from this image."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract the text."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                    ]
                }
            ],
            max_tokens=1000
        )

        # New SDK returns list of dicts
        msg_content = response.choices[0].message.content
        if isinstance(msg_content, list):
            text = " ".join([c.get("text", "") for c in msg_content if c["type"] == "text"])
        else:
            text = str(msg_content)

        return text.strip()
    except Exception as e:
        logger.error(f"AI extraction failed: {e}")
        return ""


# ---------- OCR fallback ----------
def extract_with_ocr(file_path: str) -> str:
    """OCR fallback with Tesseract."""
    try:
        if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
            return pytesseract.image_to_string(Image.open(file_path)) 
    except Exception as e:
        logger.error(f"OCR failed: {e}")
    return ""


# ---------- PDF extractor ----------
def extract_pdf_text(file_path: str) -> str:
    """Extract text from PDF using pdfplumber."""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return ""


# ---------- Master extractor ----------
def extract_text(file_path: str) -> dict:
    """
    Unified extractor:
    - Images → AI, fallback OCR
    - PDFs → pdfplumber, fallback OCR
    - TXT → read directly
    """
    ext = file_path.lower().split(".")[-1]

    # Images
    if ext in ["jpg", "jpeg", "png"]:
        text = extract_with_ai(file_path)
        if text and text.strip():
            return {"source": "AI", "text": text}

        text = extract_with_ocr(file_path)
        if text and text.strip():
            return {"source": "OCR", "text": text}

        return {"source": "None", "text": ""}

    # PDFs
    if ext == "pdf":
        text = extract_pdf_text(file_path)
        if text and text.strip():
            return {"source": "pdfplumber", "text": text}

        text = extract_with_ocr(file_path)
        if text and text.strip():
            return {"source": "OCR", "text": text}

        return {"source": "None", "text": ""}

    # TXT
    if ext == "txt":
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return {"source": "txt", "text": f.read()}
        except Exception as e:
            logger.error(f"TXT extraction failed: {e}")
            return {"source": "txt", "text": ""}

    return {"source": "unknown", "text": ""}
