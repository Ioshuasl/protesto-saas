from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import TServicoEtiquetaServicoTipoIdSchema
from packages.v1.administrativo.repositories.t_servico_etiqueta.t_servico_etiqueta_show_servico_tipo_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela T_SERVICO_ETIQUETA.
    """

    def execute(self, servico_tipo_schema: TServicoEtiquetaServicoTipoIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            servico_etiqueta_schema (TServicoEtiquetaServicoTipoIdSchema): O esquema com o ID (SERVICO_TIPO_ID) do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(servico_tipo_schema)

        # Retorno da informação
        return response