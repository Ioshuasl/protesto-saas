from packages.v1.administrativo.actions.t_ato_partetipo.t_ato_partetipo_update_action import (
    TAtoParteTipoUpdateAction,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoUpdateSchema,
)


class TAtoParteTipoUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_censec_qualidade.
    """

    def execute(self, t_ato_partetipo_update_schema: TAtoParteTipoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_partetipo_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        t_ato_partetipo_update_action = TAtoParteTipoUpdateAction()

        # Retorna o resultado da operação
        return t_ato_partetipo_update_action.execute(t_ato_partetipo_update_schema)
