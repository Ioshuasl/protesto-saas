from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoIdSchema


class ShowRepository(BaseRepository):

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):
        """
        Executa a operação de busca de um registro na tabela G_TB_TXMODELOGRUPO por ID.

        Args:
            txmodelogrupo_schema (GTbTxmodelogrupoIdSchema): O esquema com o ID a ser buscado.

        Returns:
            Um dicionário representando o registro encontrado ou None.

        Raises:
            HTTPException: Se ocorrer um erro durante a execução da consulta.
        """
        try:
            # Montagem do SQL para buscar o registro pelo ID
            sql = """
                SELECT
                    TB_TXMODELOGRUPO_ID,
                    DESCRICAO,
                    SITUACAO,
                    SISTEMA_ID
                FROM G_TB_TXMODELOGRUPO
                WHERE TB_TXMODELOGRUPO_ID = :tb_txmodelogrupo_id
            """

            # Preenchimento de parâmetros
            params = {
                "tb_txmodelogrupo_id": txmodelogrupo_schema.tb_txmodelogrupo_id
            }

            # Execução do SQL e retorno do resultado
            return self.fetch_one(sql, params)

        except Exception as e:
            # Levanta uma exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em G_TB_TXMODELOGRUPO: {e}"
            )