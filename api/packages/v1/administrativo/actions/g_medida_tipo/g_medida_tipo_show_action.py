from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoIdSchema
from packages.v1.administrativo.repositories.g_medida_tipo.g_medida_tipo_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_medida_tipo.
    """

    def execute(self, medida_tipo_schema: GMedidaTipoIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            medida_tipo_schema (GMedidaTipoIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instanciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(medida_tipo_schema)

        # Retorno da informação
        return response