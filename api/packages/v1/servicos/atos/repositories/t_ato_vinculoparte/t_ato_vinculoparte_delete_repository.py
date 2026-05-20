from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_ATO_VINCULOPARTE.
    """

    def execute(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_ATO_VINCULOPARTE
        com base no ID informado.

        Args:
            t_ato_vinculoparte_id_schema (TAtoVinculoParteIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO_VINCULOPARTE TA
                WHERE TA.ATO_VINCULOPARTE_ID = :ato_vinculoparte_id
            """

            # Preenchimento dos parâmetros
            params = {
                "ato_vinculoparte_id": t_ato_vinculoparte_id_schema.ato_vinculoparte_id
            }

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_ATO_VINCULOPARTE: {e}",
            )
