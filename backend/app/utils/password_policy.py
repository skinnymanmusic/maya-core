"""
OMEGA Core v3.0 - Password Policy Enforcement
"""
import re
from typing import Tuple, Optional
from passlib.context import CryptContext

# Common weak passwords to block
COMMON_PASSWORDS = {
    "password", "password123", "12345678", "qwerty", "abc123",
    "letmein", "welcome", "admin", "root", "passw0rd"
}

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password against policy
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    if password.lower() in COMMON_PASSWORDS:
        return False, "Password is too common. Please choose a stronger password"
    
    return True, None


class PasswordPolicyService:
    """Password policy service with hashing"""
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)

