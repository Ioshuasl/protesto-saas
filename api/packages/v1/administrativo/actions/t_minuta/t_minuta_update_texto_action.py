from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_minuta.t_minuta_update_texto_repository import TMinutaUpdateTextoRepository
from packages.v1.administrativo.schemas.t_minuta_schema import  TMinutaUpdateTextoSchema


class TMinutaUpdateTextoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela t_minuta.
    """

    def execute(self, data: TMinutaUpdateTextoSchema):
        """
        Executa a operação de atualização.

        Args:
            minuta_id (int): O ID do registro a ser atualizado.
            minuta_schema (TMinutaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Chama o método de execução do repositório para realizar a atualização
        return TMinutaUpdateTextoRepository().execute(data)