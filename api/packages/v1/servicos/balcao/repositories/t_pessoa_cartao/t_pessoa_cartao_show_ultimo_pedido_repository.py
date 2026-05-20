from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
)


class TPessoaCartaoShowUltimoPedidoRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_PESSOA_CARTAO.
    """

    def execute(self, data: TPessoaCartaoIndexchema):

        # ----------------------------------------------------
        # Montagem do SQL
        # ----------------------------------------------------
        sql = """
                SELECT FIRST 1 * FROM T_PESSOA_CARTAO TPC WHERE TPC.PESSOA_ID = :pessoa_id ORDER BY TPC.PESSOA_CARTAO_ID DESC
            """

        # ----------------------------------------------------
        # Preenchimento de parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # ----------------------------------------------------
        # Execução do SQL
        # ----------------------------------------------------
        result = self.fetch_one(sql, params)

        # ----------------------------------------------------
        # Validação de retorno
        # ----------------------------------------------------
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de T_PESSOA_CARTAO não encontrado.",
            )

        return result
