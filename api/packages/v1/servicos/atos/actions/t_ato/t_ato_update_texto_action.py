from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato.t_ato_update_texo_repository import TAtoUpdateTextoRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoUpdateTextoSchema


class TAtoUpdateTextoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TAtoUpdateTextoSchema):
        """
        Executa a operação de atualização.

        Args:
            t_ato_update_schema (TAtoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = TAtoUpdateTextoRepository().execute(data)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
