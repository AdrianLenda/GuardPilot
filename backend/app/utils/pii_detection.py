"""
Utilities for detecting personally identifiable information (PII) in text using spaCy and regex.
"""

from typing import List
import re

try:
    import spacy
except ImportError:
    spacy = None  # type: ignore

# Compile regex patterns for emails, Polish national identification numbers (PESEL), and VAT numbers
EMAIL_PATTERN = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
PESEL_PATTERN = re.compile(r"\b\d{11}\b")
# Polish VAT numbers typically start with 'PL' followed by 10 digits
VAT_PATTERN = re.compile(r"\bPL\d{10}\b", re.IGNORECASE)


_nlp_model = None

def _load_model():
    """Lazily load the spaCy model for entity recognition."""
    global _nlp_model
    if _nlp_model is None:
        if spacy is not None:
            try:
                _nlp_model = spacy.load("xx_ent_wiki_sm")  # multilingual small model
            except Exception:
                _nlp_model = spacy.blank("xx")  # fallback blank model
        else:
            _nlp_model = None
    return _nlp_model

def detect_pii(text: str) -> List[str]:
    """
    Detect PII (emails, PESEL numbers, VAT numbers and names) in the given text.
    Returns a list of detected strings. An empty list indicates no PII.
    """
    detected: List[str] = []

    # Find e-mail addresses
    detected.extend(EMAIL_PATTERN.findall(text))

    # Find PESEL numbers (11 digit numbers)
    detected.extend(PESEL_PATTERN.findall(text))

    # Find VAT numbers
    detected.extend(VAT_PATTERN.findall(text))

    # Use spaCy to detect person names if model is available
    nlp = _load_model()
    if nlp is not None:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_.upper() == "PERSON":
                detected.append(ent.text)

    return detected
