from packages.v1.administrativo.actions.t_imovel.t_imovel_show_action import (
    TImovelShowAction,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIdSchema
from fastapi import HTTPException, status


class TImovelShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_id_schema: TImovelIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_imovel_schema (TCensecQualidadeIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        t_imovel_show_action = TImovelShowAction()

        # Executa a ação em questão
        data = t_imovel_show_action.execute(t_imovel_id_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_IMOVEL_UNIDADE",
            )

        # Retorno da informação
        return data
