class CEP:

    @staticmethod
    def validate(data: str) -> bool:

        # Valida e retorna a informação
        return len(data) == 8
