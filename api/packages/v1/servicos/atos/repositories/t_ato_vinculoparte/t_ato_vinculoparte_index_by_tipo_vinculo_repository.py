from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexByTipoVinculoSchema,
)


class TAtoVinculoParteIndexByTipoVinculoRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, data: TAtoVinculoParteIndexByTipoVinculoSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """
                 SELECT
                    TAV.*,
                    TP.EMAIL AS PESSOA_EMAIL,
                    TP.SEXO AS PESSOA_SEXO,
                    GMT.DESCRICAO AS MARCACAO_TIPO_DESCRICAO,
                    TAP.DESCRICAO AS ATO_PARTETIPO_DESCRICAO
                FROM
                    T_ATO_VINCULOPARTE TAV
                JOIN T_PESSOA TP ON
                    TP.PESSOA_ID = TAV.PESSOA_ID
                LEFT JOIN G_MARCACAO_TIPO GMT ON
                    TAV.MARCACAO_TIPO_ID = GMT.MARCACAO_TIPO_ID
                LEFT JOIN T_ATO_PARTETIPO TAP ON
                    TAV.ATO_PARTETIPO_ID = TAP.ATO_PARTETIPO_ID
                WHERE
                    TAV.ato_id = :ato_id
                AND tav.tipo_vinculo = :tipo_vinculo
              """

        # ----------------------------------------------------
        # Preenchimento dos parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
