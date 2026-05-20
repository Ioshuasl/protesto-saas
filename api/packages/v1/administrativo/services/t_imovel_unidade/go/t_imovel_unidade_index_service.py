from packages.v1.administrativo.actions.t_imovel_unidade.t_imovel_unidade_index_action import (
    TImovelUnidadeIndexAction,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIndexSchema,
)
from fastapi import HTTPException, status


class TImovelUnidadeIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_index_schema: TImovelUnidadeIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        t_imovel_unidade_index_action = TImovelUnidadeIndexAction()

        # Executa a busca de todas as ações
        data = t_imovel_unidade_index_action.execute(t_imovel_unidade_index_schema)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os registros de T_IMOVEL_UNIDADE",
            )

        # Retorna as informações localizadas
        return data
