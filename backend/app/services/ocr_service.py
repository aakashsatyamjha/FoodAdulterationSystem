"""
Computer Vision & OCR Preprocessing Service
Enhances image contrast and clarity for ingredient labels,
and extracts ingredient text using OpenCV and OCR engine.
"""

import io
import re
import cv2
import numpy as np
from typing import Dict, Any
from PIL import Image

# Try locating Tesseract if installed
try:
    import pytesseract
    # Check common Windows install locations if default fails
    import shutil
    if not shutil.which("tesseract"):
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\lapto\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        ]
        import os
        for p in common_paths:
            if os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                break
except Exception:
    pytesseract = None

def preprocess_image_cv(image_bytes: bytes) -> np.ndarray:
    """
    Applies computer vision filters: grayscale, contrast enhancement (CLAHE),
    denoising, and adaptive thresholding for optimal OCR text recognition.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image.")

    # Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize if too small for better OCR character recognition
    h, w = gray.shape
    if w < 800:
        scaling = 800.0 / w
        gray = cv2.resize(gray, None, fx=scaling, fy=scaling, interpolation=cv2.INTER_CUBIC)

    # Apply Contrast Limited Adaptive Histogram Equalization (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Bilateral filter to smooth texture while preserving sharp text edges
    denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

    # Adaptive Gaussian Thresholding
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 4
    )

    return thresh

def extract_text_from_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extracts text from an ingredient label image using OpenCV preprocessing
    and OCR.
    """
    extracted_text = ""
    engine_used = "OpenCV Preprocessor + Regex Parser"
    success = False

    try:
        processed_img = preprocess_image_cv(image_bytes)

        if pytesseract is not None:
            try:
                # Custom OCR configuration for ingredient paragraphs
                custom_config = r'--oem 3 --psm 6'
                extracted_text = pytesseract.image_to_string(processed_img, config=custom_config)
                if extracted_text and len(extracted_text.strip()) > 5:
                    engine_used = "Tesseract OCR (Native Engine) + OpenCV CLAHE"
                    success = True
            except Exception as ocr_err:
                print(f"[OCR] Pytesseract execution fallback: {ocr_err}")

        # If Tesseract produced nothing or is not installed
        if not extracted_text:
            extracted_text = ""
            engine_used = "WebAssembly Tesseract.js / Client Engine Ready"

    except Exception as e:
        print(f"[OCR] Processing error: {e}")

    # Clean up common OCR noise
    cleaned_text = clean_ocr_text(extracted_text)

    return {
        "raw_text": extracted_text,
        "cleaned_text": cleaned_text,
        "extracted_text": cleaned_text or extracted_text,
        "engine": engine_used,
        "success": bool(cleaned_text and len(cleaned_text) > 5)
    }

def clean_ocr_text(text: str) -> str:
    """Normalizes OCR text, fixes punctuation, and isolates ingredients block."""
    if not text:
        return ""
    
    # Replace weird glyphs
    t = text.replace("|", "I").replace("—", "-").replace(";", ",")
    # Remove lines with pure non-alphanumeric noise
    lines = [line.strip() for line in t.split("\n") if len(line.strip()) > 2]
    joined = " ".join(lines)
    
    # Isolate ingredient section if 'Ingredients:' keyword exists
    match = re.search(r"(ingredients|ingredient list|composition)\s*[:\-](.*)", joined, re.IGNORECASE)
    if match:
        joined = match.group(2).strip()

    return joined
