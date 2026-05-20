import re


class CPF:

    @staticmethod
    def is_valid_cpf(data: str) -> bool:
        # Remove caracteres não numéricos
        data = re.sub(r'\D', '', data)

        # Verifica se tem 11 dígitos
        if len(data) != 11:
            return False

        # CPFs com todos os dígitos iguais são inválidos
        if data == data[0] * 11:
            return False

        # Calcula o primeiro e segundo dígitos verificadores
        def calcular_digito(digitos, peso):
            soma = sum(int(a) * b for a, b in zip(digitos, peso))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        # Primeiro dígito verificador
        peso1 = range(10, 1, -1)
        digito1 = calcular_digito(data[:9], peso1)

        # Segundo dígito verificador
        peso2 = range(11, 1, -1)
        digito2 = calcular_digito(data[:10], peso2)

        # Verifica se os dígitos batem
        return data[-2:] == digito1 + digito2