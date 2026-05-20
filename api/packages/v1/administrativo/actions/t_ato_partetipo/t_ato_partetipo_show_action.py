from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_ato_partetipo.t_ato_partetipo_show_repository import (
    TAtoParteTipoShowRepository,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoIdSchema,
)


class TAtoParteTipoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_ato_partetipo_schema (TCensecQualidadeIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        t_ato_partetipo_show_repository = TAtoParteTipoShowRepository()

        # Execução do repositório
        response = t_ato_partetipo_show_repository.execute(t_ato_partetipo_id_schema)

        # Retorno da informação
        return response
