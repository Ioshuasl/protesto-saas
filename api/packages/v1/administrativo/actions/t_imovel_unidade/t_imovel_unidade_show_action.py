from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel_unidade.t_imovel_unidade_show_repository import (
    TImovelUnidadeShowRepository,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIdSchema,
)


class TImovelUnidadeShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_imovel_unidade_schema (TCensecQualidadeIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        t_imovel_unidade_show_repository = TImovelUnidadeShowRepository()

        # Execução do repositório
        response = t_imovel_unidade_show_repository.execute(t_imovel_unidade_id_schema)

        # Retorno da informação
        return response
