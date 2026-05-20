from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIndexSchema,
)


class TAtoParteImovelIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, data: TAtoParteImovelIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """
                SELECT
                    TAP.ATO_PARTEIMOVEL_ID,
                    TAP.ATO_VINCULOPARTE_ID,
                    TAP.ATO_VINCULOIMOVEL_ID,
                    TAP.ATO_ID,
                    TAP.PARTICIPACAO,
                    TAP.TIPO_PROPRIETARIO,
                    TAP.QUALIFICACAO_ONR,
                    -- Dados da Parte
                    TAV.PESSOA_NOME,
                    TAV.REQUERENTE,
                    TAV.ASSINATURA_TIPO,
                    TAV.PESSOA_CPF,
                    -- Descrição do tipo da parte
                    TAPART.DESCRICAO AS ATO_PARTETIPO_DESCRICAO,
                    -- Dados do Imóvel (Via Vínculo Direto da Parte)
                    TI.NUMERO AS IMOVEL_MATRICULA,
                    TIU.NUMERO_UNIDADE,
                    TIU.QUADRA,
                    TIU.AREA,
                    TIU.LOGRADOURO
                FROM T_ATO_PARTEIMOVEL TAP
                -- 1. Liga à Parte (Quem é a pessoa)
                LEFT JOIN T_ATO_VINCULOPARTE TAV
                    ON TAV.ATO_VINCULOPARTE_ID = TAP.ATO_VINCULOPARTE_ID
                -- 2. Liga ao Tipo da Parte (Outorgante, Outorgado, etc)
                LEFT JOIN T_ATO_PARTETIPO TAPART
                    ON TAPART.ATO_PARTETIPO_ID = TAV.ATO_PARTETIPO_ID
                -- 3. CORREÇÃO: Liga ao Vínculo do Imóvel específico desta linha de TAP
                LEFT JOIN T_ATO_VINCULOIMOVEL TAVI
                    ON TAVI.ATO_VINCULOIMOVEL_ID = TAP.ATO_VINCULOIMOVEL_ID
                -- 4. Detalhes da Unidade
                LEFT JOIN T_IMOVEL_UNIDADE TIU
                    ON TIU.IMOVEL_UNIDADE_ID = TAVI.IMOVEL_UNIDADE_ID
                -- 5. Detalhes do Imóvel Mestre
                LEFT JOIN T_IMOVEL TI
                    ON TI.IMOVEL_ID = TIU.IMOVEL_ID
                WHERE
                    TAP.ATO_ID = :ato_id
              """

        # ----------------------------------------------------
        # Preenchimento dos parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
