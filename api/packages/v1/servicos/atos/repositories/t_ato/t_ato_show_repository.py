from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoShowRepository(BaseRepository):

    def execute(self, t_ato_id_schema: TAtoIdSchema):

        try:
            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                SELECT
                    TA.ATO_ID,
                    TA.ATO_TIPO_ID,
                    TA.ESCREVENTE_ATO_ID,
                    TA.ESCREVENTE_ASSINA_ID,
                    TA.LIVRO_ANDAMENTO_ID,
                    TLA.LIVRO_NATUREZA_ID,
                    TLA.USUARIO_ID AS livro_andamento_usuario_id,
                    TLA.FOLHA_ATUAL,
                    TLA.NUMERO_LIVRO,
                    TLA.NUMERO_LIVRO_LETRA,
                    TLA.DATA_ABERTURA AS livro_andamento_data_abertura,
                    TLA.DATA_FECHAMENTO,
                    TLA.NUMERO_FOLHAS,
                    TLA.ANTIGO,
                    TLA.C_ATO_FRENTEVERSO_ATUAL,
                    TLA.CHAVE_IMPORTACAO AS livro_andamento_chave_importacao,
                    TA.DATA_ABERTURA,
                    TA.DATA_LAVRATURA,
                    TA.USUARIO_ID,
                    TA.PROTOCOLO,
                    TA.ALIENACAO_DATA,
                    TA.QUALIFICACAO_IMOVEL_ID,
                    TA.FOLHA_INICIAL,
                    TA.FOLHA_FINAL,
                    TA.FOLHA_TOTAL,
                    TA.ALIENACAO_FORMA,
                    TA.GRS_NUMERO,
                    TA.NATUREZA_ID,
                    TA.VALOR_PAGAMENTO,
                    TA.SITUACAO_ATO,
                    TA.CANCELADO_DATA,
                    TA.CANCELADO_MOTIVO,
                    TA.CANCELADO_OBSERVACAO,
                    TA.CANCELADO_USUARIO_ID,
                    TA.DATA_CANCELAMENTO,
                    TA.ALIENACAO_DATALAVRATURA,
                    TA.ATO_ANTIGO,
                    TA.FOLHA_LETRA,
                    TA.QTD_IMOVEL,
                    TA.MINUTA_PROTEGIDA,
                    TA.HAVIDO_MARCACAO_ID,
                    TA.OBSERVACAO,
                    TA.SELO_LIVRO_ID,
                    TA.USAR_TABELA_AUXILIAR,
                    TA.ATO_ANTIGO_OCORRENCIA,
                    TA.FONTE_TAMANHO,
                    TA.SELO_RECUO,
                    TA.ATO_ANTIGO_PROTOCOLO,
                    TA.ATO_ANTERIOR_ORIGEM,
                    TA.ATO_ANTERIOR_LIVRO,
                    TA.ATO_ANTERIOR_FINICIAL,
                    TA.ATO_ANTERIOR_TB_CARTORIO_ID,
                    TA.ATO_ANTERIOR_OUTORGANTE,
                    TA.ATO_ANTERIOR_OBSERVACAO,
                    TA.ATO_ANTERIOR_ATO_ID,
                    TA.ATO_ANTERIOR_DATA,
                    TA.ATO_ANTERIOR_ANOTACAO_ADICIONAL,
                    TA.ATO_ANTERIOR_ATO_TIPO_ID,
                    TA.ATO_ANTERIOR_VALOR_DOCUMENTO,
                    TA.CADASTRAR_IMOVEL,
                    TA.FILHO_MAIOR_QTD,
                    TA.FILHO_MAIOR_DESCRICAO,
                    TA.FILHO_MENOR_QTD,
                    TA.FILHO_MENOR_DESCRICAO,
                    TA.CASAMENTO_DATA,
                    TA.CASAMENTO_TB_REGIME_ID,
                    TA.ATO_ANTERIOR_FFINAL,
                    TA.RESP_FILHOS_MAIORES,
                    TA.RESP_FILHOS_MENORES,
                    TA.CENSEC_NATUREZALITIGIO_ID,
                    TA.CENSEC_ACORDO,
                    TA.NLOTE,
                    TA.ESPECIE_PAGAMENTO,
                    TA.FORA_CARTORIO,
                    TA.NFSE_ID,
                    TA.ACAO,
                    TA.DATA_PROTOCOLO,
                    TA.FRENTE_VERSO,
                    TA.LAVRATURA_ONLINE,
                    TA.DATA_PREVISTA_ENTREGA,
                    TA.USUARIO_ID_LAVRATURA,
                    TA.ATIVO,
                    TA.CONVALIDACAO,
                    TA.LADO_FOLHA_FIM,
                    TA.ATO_ONEROSO,
                    TA.MNE,
                    TA.EH_RESTRITO
                FROM T_ATO TA
                LEFT JOIN T_LIVRO_ANDAMENTO TLA
                  ON TA.LIVRO_ANDAMENTO_ID = TLA.LIVRO_ANDAMENTO_ID
                JOIN T_ATO_TIPO TAT ON TA.ATO_TIPO_ID = TAT.ATO_TIPO_ID
                WHERE TA.ATO_ID = :ato_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_ato_id_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Execução do SQL
            # ----------------------------------------------------
            result = self.fetch_one(sql, params)

            # ----------------------------------------------------
            # Validação de retorno
            # ----------------------------------------------------
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de T_ATO não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_ATO: {e}",
            )
