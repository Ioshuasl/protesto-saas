import re


class CNPJ:

    @staticmethod
    def validate(data: str) -> bool:

        # Remove caracteres não numéricos
        data = re.sub(r'\D', '', data)

        # Verifica se tem 14 dígitos
        if len(data) != 14:
            return False

        # CNPJs com todos os dígitos iguais são inválidos
        if data == data[0] * 14:
            return False

        # Calcula os dois dígitos verificadores
        def calcular_digito(data, peso):
            soma = sum(int(a) * b for a, b in zip(data, peso))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        # Primeiro dígito verificador
        peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        digito1 = calcular_digito(data[:12], peso1)

        # Segundo dígito verificador
        peso2 = [6] + peso1
        digito2 = calcular_digito(data[:12] + digito1, peso2)

        # Verifica se os dígitos batem
        return data[-2:] == digito1 + digito2
