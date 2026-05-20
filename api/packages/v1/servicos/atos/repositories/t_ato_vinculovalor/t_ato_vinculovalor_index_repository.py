from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIndexSchema,
)


class TAtoVinculoValorIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, data: TAtoVinculoValorIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """
                SELECT
                    TAV.ATO_VINCULOVALOR_ID,
                    TAV.ATO_ID,
                    TAV.EMOLUMENTO,
                    TAV.TAXA_JUDICIARIA,
                    TAV.EMOLUMENTO_ID,
                    TAV.FUNDESP,
                    TAV.VALOR_TOTAL,
                    TAV.EMOLUMENTO_DESCONTO,
                    TAV.NATUREZA_TITULO_ID,
                    TAV.VALOR_DOCUMENTO,
                    TAV.QUANTIDADE,
                    TAV.TIPO_COBRANCA,
                    TAV.ITEM_PADRAO,
                    TAV.VALOR_OUTRA_TAXA1,
                    TAV.ITEM_COMPLEMENTAR,
                    TAV.ITEM_MANUAL,
                    TAV.EMOLUMENTO_CORRETOR,
                    TAV.EMOLUMENTO_ITEM_ID,
                    TAV.VALOR_ADICIONAL,
                    TAV.DIFERENCA_SITUACAO,
                    TAV.DIFERENCA_DESCRICAO,
                    TAV.DIFERENCA_TIPO,
                    TAV.VALOR_ISS,
                    TAV.ID_ATO_ISENTADO,
                    TAV.ISENTO_EMOLUMENTO_ID,
                    TAV.MOTIVO_ISENCAO,
                    TAV.ATO_VINCULOIMOVEL_ID,
                    TAV.NLOTE,
                    TAV.EMOL_PRINCIPAL,
                    TAV.MOTIVO_ISENCAO_ID,
                    TAV.VALOR_INFORMACOES_CENTRAIS,
                    TAV.SITUACAO_DIFERIDO,
                    TAV.MOTIVO_DIFERIDO,
                    TAV.SIGLA_NUMERO,
                    TAV.VALOR_BENS,
                    TAV.EMOLUMENTO_ACRESCE,
                    TAV.TAXA_ACRESCE,
                    TAV.FUNCIVIL_ACRESCE,
                    TAV.CHAVE_IMPORTACAO,
                    TAV.COD_FATOR,
                    TAV.QTD_KM,
                    TAV.VALOR_AVALIACAO,
                    TAV.DISTRIBUICAO,
                    TAV.FUNDO_SELO,
                    TAV.VRCEXT,
                    GEI.SELO_GRUPO_ID,
                    GE.DESCRICAO AS EMOLUMENTO_DESCRICAO,
                    GNT.DESCRICAO AS NATUREZA_TITULO_DESCRICAO
                FROM
                    T_ATO_VINCULOVALOR TAV
                LEFT JOIN G_EMOLUMENTO GE
                    ON GE.EMOLUMENTO_ID = TAV.EMOLUMENTO_ID
                LEFT JOIN G_EMOLUMENTO_ITEM GEI
                    ON GEI.EMOLUMENTO_ITEM_ID = TAV.EMOLUMENTO_ITEM_ID
                LEFT JOIN G_NATUREZA_TITULO GNT
                    ON GNT.NATUREZA_TITULO_ID = TAV.NATUREZA_TITULO_ID
                WHERE
                    TAV.ATO_ID = :ato_id
              """

        # ----------------------------------------------------
        # Preenchimento dos parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
