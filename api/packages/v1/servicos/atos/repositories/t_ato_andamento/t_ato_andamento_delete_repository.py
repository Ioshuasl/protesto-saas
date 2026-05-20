from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIdSchema,
)


class TAtoAndamentoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_ATO_ANDAMENTO.
    """

    def execute(self, t_ato_andamento_id_schema: TAtoAndamentoIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_ATO_ANDAMENTO
        com base no ID informado.

        Args:
            t_ato_andamento_id_schema (TAtoAndamentoIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO_ANDAMENTO TA
                WHERE TA.ATO_ANDAMENTO_ID = :ato_andamento_id
            """

            # Preenchimento dos parâmetros
            params = {
                "ato_andamento_id": t_ato_andamento_id_schema.ato_andamento_id
            }

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_ATO_ANDAMENTO: {e}",
            )
