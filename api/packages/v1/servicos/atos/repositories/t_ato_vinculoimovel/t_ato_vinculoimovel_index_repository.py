from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIndexSchema,
)


class TAtoVinculoImovelIndexRepository(BaseRepository):

    def execute(self, data: TAtoVinculoImovelIndexSchema):

        # Montagem do SQL
        sql = """
                SELECT
                    -- Colunas da T_ATO_VINCULOIMOVEL
                    tav.ATO_VINCULOIMOVEL_ID,
                    tav.ATO_ID,
                    tav.REGISTRO_NUMERO,
                    tav.IMOVEL_UNIDADE_ID,
                    tav.VALOR_AVALIACAO,
                    tav.VALOR_ALIENACAO,
                    tav.VALOR_ALIQUOTA,
                    tav.IMOVEL_ID,
                    tav.VALOR_MAIOR,
                    tav.REGISTRO_DATA,
                    tav.CHAVE_IMPORTACAO,
                    tav.TIPO_ATO_ONR,
                    tav.VALORTRANSMISSAO,
                    tav.VALORVENAL,
                    tav.VALORFINANCIAMENTO,
                    tav.VALORLEILAO,
                    tav.RECURSOSPROPRIOS,
                    tav.RECURSOSFINANCIADO,
                    tav.PRIMEIRAAQUISICAO,
                    tav.OBSERVACOESGERAIS,
                    tav.DESCREVER,
                    tav.VALOR_PAGO_DATA_ATO,
                    tav.PERMUTA_BENS,
                    tav.PAGAMENTO_EM_DINHEIRO,
                    tav.VALOR_PAGO_EM_DINHEIRO,
                    tav.DATA_ULTIMA_PARCELA,

                    -- Colunas selecionadas da T_IMOVEL_UNIDADE
                    iu.NUMERO_UNIDADE,
                    iu.QUADRA,
                    iu.AREA,
                    iu.LOGRADOURO,
                    iu.COMPLEMENTO,
                    iu.TIPO_IMOVEL,
                    iu.TIPO_CONSTRUCAO,
                    iu.IPTU,
                    iu.INSCRICAO_MUNICIPAL,

                    -- Colunas selecionadas da T_IMOVEL
                    i.CIDADE          AS IMOVEL_CIDADE,
                    i.UF              AS IMOVEL_UF,
                    i.TB_BAIRRO_ID    AS IMOVEL_TB_BAIRRO_ID,
                    i.LIVRO           AS IMOVEL_LIVRO,
                    i.CARTORIO        AS IMOVEL_CARTORIO,
                    i.NUMERO          AS IMOVEL_MATRICULA
                FROM
                    T_ATO_VINCULOIMOVEL tav
                    LEFT JOIN T_IMOVEL_UNIDADE iu
                        ON iu.IMOVEL_UNIDADE_ID = tav.IMOVEL_UNIDADE_ID
                    LEFT JOIN T_IMOVEL i
                        ON i.IMOVEL_ID = iu.IMOVEL_ID
                WHERE
                    tav.ATO_ID = :ato_id
              """

        # Preenchimento dos parâmetros
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
