from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoIndexSchema


class THistoricoIndexRepository(BaseRepository):
    """
    Repositório responsável pela listagem de registros
    da tabela T_HISTORICO.
    """

    def execute(self, data: THistoricoIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Lista de registros encontrados.
        """
        sql = """
            SELECT
                TH.HISTORICO_ID,
                TH.CAMPO,
                TH.OBSERVACAO,
                TH.OPERACAO,
                TH.DATA
            FROM T_HISTORICO TH
            WHERE TH.TABELA LIKE :tabela
            AND TH.ID = :id
            ORDER BY TH.DATA DESC
        """

        # ----------------------------------------------------
        # Preenchimento dos parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
