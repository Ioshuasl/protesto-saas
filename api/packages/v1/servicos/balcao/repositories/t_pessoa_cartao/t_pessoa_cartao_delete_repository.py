from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIdSchema,
)


class TPessoaCartaoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    TPessoaCartao.
    """

    def execute(self, TPessoaCartao_id_schema: TPessoaCartaoIdSchema):
        """
        Executa a exclusão de um registro específico da tabela TPessoaCartao
        com base no ID informado.

        Args:
            TPessoaCartao_id_schema (TPessoaCartaoIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM t_pessoa_cartao tpc
                WHERE tpc.pessoa_cartao_id = :pessoa_cartao_id
                RETURNING pessoa_cartao_id
            """

            # Preenchimento dos parâmetros
            params = {"pessoa_cartao_id": TPessoaCartao_id_schema.pessoa_cartao_id}

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de TPessoaCartao: {e}",
            )
