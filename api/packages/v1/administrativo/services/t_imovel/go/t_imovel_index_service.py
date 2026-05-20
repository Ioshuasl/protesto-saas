from packages.v1.administrativo.actions.t_imovel.t_imovel_index_action import (
    TImovelIndexAction,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIndexSchema
from fastapi import HTTPException, status


class TImovelIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_index_schema: TImovelIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        t_imovel_index_action = TImovelIndexAction()

        # Executa a busca de todas as ações
        data = t_imovel_index_action.execute(t_imovel_index_schema)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os registros de T_IMOVEL_UNIDADE",
            )

        # Retorna as informações localizadas
        return data
