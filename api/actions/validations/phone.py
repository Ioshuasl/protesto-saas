
class Phone:

    @staticmethod
    def validate_cellphone(data: str) -> bool:
        # Verifica e retorna se o numero de celular é igual a 11
        return len(data) == 11

    @staticmethod
    def validate_telephone(data: str) -> bool:
        # Verifica e retorna se o numero de telefone é igual a 11
        return len(data) == 10