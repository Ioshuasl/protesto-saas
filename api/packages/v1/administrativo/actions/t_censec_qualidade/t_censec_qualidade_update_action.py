from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeUpdateSchema
from packages.v1.administrativo.repositories.t_censec_qualidade.t_censec_qualidade_update_repository import UpdateRepository


class UpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, censec_qualidade_id: int, censec_qualidade_schema: TCensecQualidadeUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            censec_qualidade_id (int): O ID do registro a ser atualizado.
            censec_qualidade_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(censec_qualidade_id, censec_qualidade_schema)