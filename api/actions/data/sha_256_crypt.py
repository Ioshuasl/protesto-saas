import hashlib


class Sha256Crypt:
    @staticmethod
    def execute(value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("O valor informado deve ser uma string.")
        return hashlib.sha256(value.encode("utf-8")).hexdigest()
