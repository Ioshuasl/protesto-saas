from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIdSchema,
)
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_show_repository import (
    ShowRepository,
)


class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela T_SERVICO_TIPO.
    """

    def execute(self, servico_tipo_schema: TServicoTipoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            servico_tipo_schema (TServicoTipoIdSchema): O esquema com o ID (SERVICO_TIPO_ID) do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(servico_tipo_schema)

        # Retorno da informação
        return response
