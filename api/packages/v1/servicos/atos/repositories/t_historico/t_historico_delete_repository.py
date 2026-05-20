from abstracts.repository import BaseRepository
from fastapi import HTTPException, status
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoIdSchema,
)


class THistoricoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de um registro
    da tabela T_HISTORICO.
    """

    def execute(self, data: THistoricoIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_HISTORICO
        com base no ID informado.

        Args:
            t_historico_id_schema (THtoVinculoParteIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_HISTORICO TH
                WHERE TH.HISTORICO_ID = :historico_id
            """

            # Preenchimento dos parâmetros
            params = {"historico_id": data.historico_id}

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_HISTORICO: {e}",
            )
