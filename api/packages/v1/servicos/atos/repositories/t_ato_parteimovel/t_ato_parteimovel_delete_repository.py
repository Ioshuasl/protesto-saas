from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIdSchema,
)


class TAtoParteImovelDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_id_schema: TAtoParteImovelIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_ATO_PARTEIMOVEL
        com base no ID informado.

        Args:
            t_ato_parteimovel_id_schema (TAtoParteImovelIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO_PARTEIMOVEL TA
                WHERE TA.ATO_PARTEIMOVEL_ID = :ato_parteimovel_id
                RETURNING ato_parteimovel_id
            """

            # Preenchimento dos parâmetros
            params = {
                "ato_parteimovel_id": t_ato_parteimovel_id_schema.ato_parteimovel_id
            }

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_ATO_PARTEIMOVEL: {e}",
            )
