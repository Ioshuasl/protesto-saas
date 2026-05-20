from abstracts.repository import BaseRepository

# Adaptação do Schema para GEmolumentoItem. Assumindo o uso de um Schema de ID de Sistema
# ou, mais tipicamente para itens, um Schema de ID do Emolumento pai (EMOLUMENTO_ID).
# Para manter a similaridade do original, vamos usar um 'SistemaIdSchema' adaptado,
# mas o SQL será ajustado para o campo EMOLUMENTO_ID.
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemValorSchema,
)


class ValorRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela G_EMOLUMENTO_ITEM, possivelmente filtrados por EMOLUMENTO_ID.
    """

    # Mantendo o padrão de nome de método do arquivo original
    def execute(self, emolumento_item_schema: GEmolumentoItemValorSchema):
        """
        Executa a consulta SQL para buscar todos os registros de G_EMOLUMENTO_ITEM,
        incluindo todos os campos da DDL fornecida.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL com TODOS os campos da DDL fornecida
        sql = """ SELECT VALOR_EMOLUMENTO,
                         EMOLUMENTO_ITEM_ID,
                         EMOLUMENTO_ID,
                         VALOR_INICIO,
                         VALOR_FIM,
                         VALOR_TAXA_JUDICIARIA,
                         EMOLUMENTO_PERIODO_ID,
                         CODIGO,
                         PAGINA_EXTRA,
                         VALOR_PAGINA_EXTRA,
                         VALOR_OUTRA_TAXA1,
                         CODIGO_SELO,
                         VALOR_FUNDO_RI,
                         CODIGO_TABELA,
                         SELO_GRUPO_ID,
                         CODIGO_KM,
                         EMOLUMENTO_ACRESCE,
                         TAXA_ACRESCE,
                         FUNCIVIL_ACRESCE,
                         VALOR_FRACAO,
                         VALOR_POR_EXCEDENTE_EMOL,
                         VALOR_POR_EXCEDENTE_TJ,
                         VALOR_POR_EXCEDENTE_FUNDO,
                         VALOR_LIMITE_EXCEDENTE_EMOL,
                         VALOR_LIMITE_EXCEDENTE_TJ,
                         VALOR_LIMITE_EXCEDENTE_FUNDO,
                         FUNDO_SELO,
                         DISTRIBUICAO,
                         VRCEXT
                  FROM G_EMOLUMENTO_ITEM
                  WHERE
                    EMOLUMENTO_ID = :emolumento_id
                    AND :valor BETWEEN VALOR_INICIO AND VALOR_FIM
                    AND EMOLUMENTO_PERIODO_ID = (
                        SELECT MAX(EI2.EMOLUMENTO_PERIODO_ID)
                        FROM G_EMOLUMENTO_ITEM EI2
                        WHERE EI2.EMOLUMENTO_ID = :emolumento_id
                    )
                    ORDER BY EMOLUMENTO_ITEM_ID; """

        # Preenchimento de parâmetros.
        # Adaptando o nome do parâmetro para refletir a coluna da DDL (EMOLUMENTO_ID).
        # Assumimos que o campo 'emolumento_id' do schema está sendo usado para passar este valor.
        params = {
            "emolumento_id": emolumento_item_schema.emolumento_id,
            "valor": emolumento_item_schema.valor,
        }

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
