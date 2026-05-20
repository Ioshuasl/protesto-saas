import re


class Email:

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if email has a valid structure"""
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))