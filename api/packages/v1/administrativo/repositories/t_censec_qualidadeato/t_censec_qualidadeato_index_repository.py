from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIndexSchema,
)


class TCensecQualidadeAtoIndexRepository(BaseRepository):
    """
    Repositório responsável pela operação de listagem de todos os registros
    na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(
        self, censec_qualidade_ato_index_schema: TCensecQualidadeAtoIndexSchema
    ):
        """
        Executa a consulta SQL para buscar todos os registros da tabela
        T_CENSEC_QUALIDADEATO.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # ----------------------------------------------------
        # Montagem do SQL
        # ----------------------------------------------------
        sql = """
                SELECT
                    TCQA.*,
                    TCQ.DESCRICAO  AS TCQ_DESCRICAO
                FROM
                    T_CENSEC_QUALIDADEATO tcqa
                JOIN T_CENSEC_QUALIDADE tcq ON
                    tcqa.CENSEC_QUALIDADE_ID = tcq.CENSEC_QUALIDADE_ID
                WHERE
                    TCQA.CENSEC_TIPOATO_ID = :censec_tipoato_id
            """

        # ----------------------------------------------------
        # Montagem do parâmetros
        # ----------------------------------------------------
        params = {
            "censec_tipoato_id": censec_qualidade_ato_index_schema.censec_tipoato_id
        }

        # ----------------------------------------------------
        # Execução do SQL
        # ----------------------------------------------------
        response = self.fetch_all(sql, params)

        # ----------------------------------------------------
        # Retorno dos dados localizados
        # ----------------------------------------------------
        return response
