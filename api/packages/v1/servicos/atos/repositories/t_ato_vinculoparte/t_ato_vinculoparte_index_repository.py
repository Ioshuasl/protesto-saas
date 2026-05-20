from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexSchema,
)


class TAtoVinculoParteIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, data: TAtoVinculoParteIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """
                 SELECT
                    TAV.ATO_VINCULOPARTE_ID,
                    TAV.PESSOA_ID,
                    TAV.ATO_ID,
                    TAV.ATO_PARTETIPO_ID,
                    TAV.TB_ESTADOCIVIL_ID,
                    TAV.TB_PROFISSAO_ID,
                    TAV.MARCACAO_TIPO_ID,
                    TAV.PESSOA_NOME,
                    TAV.TIPO_VINCULO,
                    TAV.PARTICIPACAO,
                    TAV.ASSINATURA_TIPO,
                    TAV.PESSOA_CONJUGE_ID,
                    TAV.VINCULO_CONJUGE,
                    TAV.AUXILIAR_ID,
                    TAV.ORDEM,
                    TAV.PESSOA_CPF,
                    TAV.TIPO_VINCULO_AUXILIAR,
                    TAV.TEXTO_COMPLEMENTAR,
                    TAV.TB_REGIMECOMUNHAO_ID,
                    TAV.REQUERENTE,
                    TAV.CHAVE_IMPORTACAO,
                    TAV.DESCREVER,
                    TAV.AUTORIZACAO,
                    TAV.DECLARACAO,
                    TAV.VBOTAO,
                    TAV.NUMERO,
                    TAV.TIPOREGISTRO,
                    TAV.ORGAO,
                    TAV.FORMAREGISTRO,
                    TAV.NUMEROLIVRO,
                    TAV.FOLHA,
                    TAV.NUMEROREGISTRO,
                    TAV.DATAREGISTRO,
                    TAV.QUALIFICACAO_ONR,
                    TP.EMAIL AS PESSOA_EMAIL,
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
              """

        # ----------------------------------------------------
        # Preenchimento dos parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
