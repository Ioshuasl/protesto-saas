from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel.t_imovel_save_repository import (
    TImovelSaveRepository,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelSchema


class TImovelSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_schema: TImovelSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_imovel_schema (TCensecQualidadeSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        t_imovel_save_repository = TImovelSaveRepository()

        # Execução do repositório
        response = t_imovel_save_repository.execute(t_imovel_schema)

        # Retorno da informação
        return response
