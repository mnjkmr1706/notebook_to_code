import re
from typing import List

def check_pii(content: str) -> List[str]:
    """
    Scans the provided content for Personally Identifiable Information (PII).
    Returns a list of detected PII types/warnings.
    """
    warnings = []
    
    # Email Regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if re.search(email_pattern, content):
        warnings.append("Detected potential Email Address")
        
    # Phone Number Regex (Simple US/International format)
    phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})\b'
    if re.search(phone_pattern, content):
        warnings.append("Detected potential Phone Number")
        
    # IPv4 Address Regex
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    if re.search(ip_pattern, content):
        warnings.append("Detected potential IP Address")
        
    # Credit Card Regex (Simple check for 13-19 digits)
    cc_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    # Refine to avoid matching simple long numbers if possible, but keeping it simple for now
    # This is a broad check
    if re.search(cc_pattern, content):
        warnings.append("Detected potential Credit Card Number")
        
    return warnings
