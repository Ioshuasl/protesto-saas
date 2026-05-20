from packages.v1.administrativo.actions.t_imovel_unidade.t_imovel_unidade_show_action import (
    TImovelUnidadeShowAction,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIdSchema,
)
from fastapi import HTTPException, status


class TImovelUnidadeShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_imovel_unidade_schema (TCensecQualidadeIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        t_imovel_unidade_show_action = TImovelUnidadeShowAction()

        # Executa a ação em questão
        data = t_imovel_unidade_show_action.execute(t_imovel_unidade_id_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_IMOVEL_UNIDADE",
            )

        # Retorno da informação
        return data
