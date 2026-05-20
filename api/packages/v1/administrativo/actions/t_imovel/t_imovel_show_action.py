from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel.t_imovel_show_repository import (
    TImovelShowRepository,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIdSchema


class TImovelShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_id_schema: TImovelIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_imovel_schema (TCensecQualidadeIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        t_imovel_show_repository = TImovelShowRepository()

        # Execução do repositório
        response = t_imovel_show_repository.execute(t_imovel_id_schema)

        # Retorno da informação
        return response
