import re

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioCpfSchema, GUsuarioSchema

class GetByUsuarioCpfRepository(BaseRepository):

    @staticmethod
    def limpar_cpf(cpf: str) -> str:
        """Remove caracteres não numéricos de uma string de CPF."""
        return re.sub(r'\D', '', cpf)

    @staticmethod
    def aplicar_mascara_cpf(cpf: str) -> str:
        """Aplica a máscara no CPF, assumindo que a string contém apenas dígitos."""
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf # Retorna o original se o comprimento for inválido

    def execute(self, g_usuario_schema: GUsuarioCpfSchema) -> GUsuarioSchema:
        
        # 1. Limpa o CPF de entrada (remove pontos e traços)
        cpf_limpo = self.limpar_cpf(g_usuario_schema.cpf)

        # 2. Cria uma versão do CPF com a máscara (para buscar registros com máscara)
        cpf_mascarado = self.aplicar_mascara_cpf(cpf_limpo)

        # 3. Define a consulta SQL com a lógica OR para buscar ambos os formatos
        sql = """
            SELECT * FROM g_usuario gu
            WHERE gu.cpf = :cpf_limpo
            OR gu.cpf = :cpf_mascarado
        """

        # 4. Preenche os parâmetros SQL com os dois valores
        params = {
            'cpf_limpo': cpf_limpo,
            'cpf_mascarado': cpf_mascarado
        }

        # 5. Executa a instrução SQL
        result = self.fetch_one(sql, params)

        # 6. Retorna o resultado no formato GUsuarioSchema ou None
        if result:
            return GUsuarioSchema(**result)
        return None