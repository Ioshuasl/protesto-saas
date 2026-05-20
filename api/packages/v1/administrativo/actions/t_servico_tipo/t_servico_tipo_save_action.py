from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoSaveSchema,
)
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_save_repository import (
    SaveRepository,
)


class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela T_SERVICO_TIPO.
    """

    def execute(self, servico_tipo_schema: TServicoTipoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            servico_tipo_schema (TServicoTipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(servico_tipo_schema)

        # Retorno da informação
        return response
