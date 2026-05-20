from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel_unidade.t_imovel_unidade_save_repository import (
    TImovelUnidadeSaveRepository,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeSaveSchema,
)


class TImovelUnidadeSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_save_schema: TImovelUnidadeSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_imovel_unidade_schema (TCensecQualidadeSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        t_imovel_unidade_save_repository = TImovelUnidadeSaveRepository()

        # Execução do repositório
        response = t_imovel_unidade_save_repository.execute(
            t_imovel_unidade_save_schema
        )

        # Retorno da informação
        return response
