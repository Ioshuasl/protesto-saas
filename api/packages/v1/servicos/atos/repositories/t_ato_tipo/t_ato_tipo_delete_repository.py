from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoIdSchema,
)


class TAtoTipoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_ATO_TIPO
        com base no ID informado.

        Args:
            t_ato_tipo_id_schema (TAtoTipoIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO_TIPO TA
                WHERE TA.ATO_TIPO_ID = :ato_tipo_id
            """

            # Preenchimento dos parâmetros
            params = {
                "ato_tipo_id": t_ato_tipo_id_schema.ato_tipo_id
            }

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_ATO_TIPO: {e}",
            )
