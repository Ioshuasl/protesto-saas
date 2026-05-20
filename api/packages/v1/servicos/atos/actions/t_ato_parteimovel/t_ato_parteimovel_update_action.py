from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_parteimovel.t_ato_parteimovel_update_repository import (
    TAtoParteImovelUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelUpdateSchema,
)


class TAtoParteImovelUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_parteimovel_update_schema: TAtoParteImovelUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_ato_parteimovel_update_schema (TAtoParteImovelUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_ato_parteimovel_update_repository = TAtoParteImovelUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_parteimovel_update_repository.execute(
            t_ato_parteimovel_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
