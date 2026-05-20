from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_ato_partetipo.t_ato_partetipo_save_repository import (
    TAtoParteTipoSaveRepository,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoSaveSchema,
)


class TAtoParteTipoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_censec_qualidade.
    """

    def execute(self, t_ato_partetipo_save_schema: TAtoParteTipoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_partetipo_schema (TCensecQualidadeSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        t_ato_partetipo_save_repository = TAtoParteTipoSaveRepository()

        # Execução do repositório
        response = t_ato_partetipo_save_repository.execute(t_ato_partetipo_save_schema)

        # Retorno da informação
        return response
