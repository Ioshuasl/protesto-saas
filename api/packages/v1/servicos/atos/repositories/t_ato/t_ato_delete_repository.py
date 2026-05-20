from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_ATO.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_ATO
        com base no ID informado.

        Args:
            t_ato_id_schema (TAtoIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO TA
                WHERE TA.ATO_ID = :ato_id
            """

            # Preenchimento dos parâmetros
            params = {"ato_id": t_ato_id_schema.ato_id}

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_ATO: {e}",
            )
