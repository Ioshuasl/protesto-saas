from packages.v1.administrativo.actions.t_minuta.t_minuta_update_texto_action import TMinutaUpdateTextoAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaUpdateTextoSchema

class TMinutaUpdateTextoService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_minuta.
    """
    def execute(self, data: TMinutaUpdateTextoSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            minuta_schema (TMinutaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """

        # Retorna o resultado da operação
        return TMinutaUpdateTextoAction().execute(data)