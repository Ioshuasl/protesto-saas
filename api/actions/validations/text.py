import html
import re


class Text:

    # Remove as mascaras de números
    @staticmethod
    def just_numbers(data: str) -> str:
        """ Mantêm apenas os numeros """
        data = re.sub(r"[^\d]", "", data)
        return data
    
    # Verifica se um e-mail é válido
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Check if email has a valid structure"""
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))
    

    """
    Sanitiza entradas de texto contra XSS e SQL Injection básicos.
    - Remove espaços extras
    - Escapa entidades HTML
    - Remove padrões suspeitos de XSS e SQL Injection
    - Normaliza múltiplos espaços em um só
    """
    @staticmethod
    def sanitize_input(data: str) -> str:

        if not data:
            return data

        # 1) Remove espaços no início e no fim
        data = data.strip()

        # 2) Escapa entidades HTML (< > & ")
        data = html.escape(data)

        # 3) Remove múltiplos espaços seguidos
        data = re.sub(r"\s+", " ", data)

        # 4) Remove tags <script> (com atributos)
        data = re.sub(r'<\s*script[^>]*>', '', data, flags=re.IGNORECASE)
        data = re.sub(r'<\s*/\s*script\s*>', '', data, flags=re.IGNORECASE)

        # 5) Remove javascript: de links
        data = re.sub(r'javascript\s*:', '', data, flags=re.IGNORECASE)

        # 6) Remove palavras-chave SQL Injection comuns
        blacklist = [
            "--", ";", "/*", "*/", "@@",
            "char(", "nchar(", "varchar(",
            "alter", "drop", "exec", "insert",
            "delete", "update", "union", "select",
            "from", "where"
        ]
        for word in blacklist:
            # Verificar se 'word' é uma string não vazia e válida para a regex
            if word:
                data = re.sub(re.escape(word), "", data, flags=re.IGNORECASE)

        return data