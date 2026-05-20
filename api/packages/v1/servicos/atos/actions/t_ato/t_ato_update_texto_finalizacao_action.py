from abstracts.action import BaseAction
from packages.v1.docx.services.docx_save_service import TAtoTextoFinalizacaoUpdateSchema
from packages.v1.servicos.atos.repositories.t_ato.t_ato_update_texo_finalizacao_repository import TAtoUpdateTextoFinalizacaoRepository
from packages.v1.servicos.atos.repositories.t_ato.t_ato_update_texo_repository import TAtoUpdateTextoRepository


class TAtoUpdateTextoFinalizacaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TAtoTextoFinalizacaoUpdateSchema):
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
        response = TAtoUpdateTextoFinalizacaoRepository().execute(data)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
