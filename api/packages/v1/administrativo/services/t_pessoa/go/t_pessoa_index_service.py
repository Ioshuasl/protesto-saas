from packages.v1.administrativo.actions.t_pessoa.t_pessoa_index_action import (
    TPessoaIndexAction,
)
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaTipoSchema


class TPessoaIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_tipo_schema: TPessoaTipoSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        t_pessoa_index_action = TPessoaIndexAction()

        # Executa a busca de todas as ações
        data = t_pessoa_index_action.execute(t_pessoa_tipo_schema)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar as pessoas",
            )

        # Retorna as informações localizadas
        return data
