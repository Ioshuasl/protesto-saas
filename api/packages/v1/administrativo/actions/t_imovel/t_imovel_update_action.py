from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel.t_imovel_update_repository import (
    TImovelUpdateRepository,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelUpdateSchema


class TImovelUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_update_schema: TImovelUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_imovel_unidade_id (int): O ID do registro a ser atualizado.
            t_imovel_update_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        t_imovel_update_repository = TImovelUpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return t_imovel_update_repository.execute(t_imovel_update_schema)
