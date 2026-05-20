from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_ato_partetipo.t_ato_partetipo_update_repository import (
    TAtoParteTipoUpdateRepository,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoUpdateSchema,
)


class TAtoParteTipoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_ato_partetipo_update_schema: TAtoParteTipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_ato_partetipo_unidade_id (int): O ID do registro a ser atualizado.
            t_ato_partetipo_update_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        t_ato_partetipo_update_repository = TAtoParteTipoUpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return t_ato_partetipo_update_repository.execute(t_ato_partetipo_update_schema)
