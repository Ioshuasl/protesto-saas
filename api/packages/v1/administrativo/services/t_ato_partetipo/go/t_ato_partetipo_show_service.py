from packages.v1.administrativo.actions.t_ato_partetipo.t_ato_partetipo_show_action import (
    TAtoParteTipoShowAction,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoIdSchema,
)
from fastapi import HTTPException, status


class TAtoParteTipoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_partetipo_schema (TCensecQualidadeIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        t_ato_partetipo_show_action = TAtoParteTipoShowAction()

        # Executa a ação em questão
        data = t_ato_partetipo_show_action.execute(t_ato_partetipo_id_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_IMOVEL_UNIDADE",
            )

        # Retorno da informação
        return data
