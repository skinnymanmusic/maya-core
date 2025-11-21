"""
OMEGA Core v3.0 - AES-256 Encryption Service
Fernet-based encryption for PII data
"""
from cryptography.fernet import Fernet
from app.config import get_settings

settings = get_settings()

# Initialize Fernet cipher
_cipher = None


def _get_cipher() -> Fernet:
    """Get or create Fernet cipher instance"""
    global _cipher
    if _cipher is None:
        key = settings.encryption_key.encode() if isinstance(settings.encryption_key, str) else settings.encryption_key
        _cipher = Fernet(key)
    return _cipher


def encrypt(data: str) -> str:
    """
    Encrypt PII data using AES-256 (Fernet)
    
    Args:
        data: Plaintext data to encrypt
        
    Returns:
        Encrypted data (base64-encoded)
    """
    if not data:
        return ""
    cipher = _get_cipher()
    return cipher.encrypt(data.encode()).decode()


def decrypt(encrypted_data: str) -> str:
    """
    Decrypt PII data
    
    Args:
        encrypted_data: Encrypted data (base64-encoded)
        
    Returns:
        Decrypted plaintext
    """
    if not encrypted_data:
        return ""
    cipher = _get_cipher()
    return cipher.decrypt(encrypted_data.encode()).decode()

