from abstracts.repository import BaseRepository
from packages.v1.administrativo.controllers.g_usuario_controller import (
    GUsuarioIndexSchema,
)


class IndexRepository(BaseRepository):

    def execute(self, g_usuario_index_schema: GUsuarioIndexSchema):

        # Montagem do sql
        sql = """
        SELECT
            GU.USUARIO_ID,
            GU.TROCARSENHA,
            GU.LOGIN,
            GU.SENHA,
            GU.SITUACAO,
            GU.NOME_COMPLETO,
            GU.FUNCAO,
            GU.ASSINA,
            GU.SIGLA,
            GU.USUARIO_TAB,
            GU.ULTIMO_LOGIN,
            GU.ULTIMO_LOGIN_REGS,
            GU.DATA_EXPIRACAO,
            GU.SENHA_ANTERIOR,
            GU.ANDAMENTO_PADRAO,
            GU.LEMBRETE_PERGUNTA,
            GU.LEMBRETE_RESPOSTA,
            GU.ANDAMENTO_PADRAO2,
            GU.RECEBER_MENSAGEM_ARROLAMENTO,
            GU.EMAIL,
            GU.ASSINA_CERTIDAO,
            GU.RECEBER_EMAIL_PENHORA,
            GU.FOTO,
            GU.NAO_RECEBER_CHAT_TODOS,
            GU.PODE_ALTERAR_CAIXA,
            GU.RECEBER_CHAT_CERTIDAO_ONLINE,
            GU.RECEBER_CHAT_CANCELAMENTO,
            GU.CPF,
            GU.SOMENTE_LEITURA,
            GU.RECEBER_CHAT_ENVIO_ONR,
            GU.TIPO_USUARIO,
            GU.DISTRIBUIR_PROTOCOLO_RI,
            GU.ULTIMO_PROTOCOLO_RI
        FROM G_USUARIO GU
        """

        # lista de condições (já evita registros excluídos)
        where = ["GU.SITUACAO <> 'D'"]

        # Filtro por assinatura
        if getattr(g_usuario_index_schema, "assina", None):
            where.append("GU.ASSINA LIKE :assina")

        # Filtro por situação
        if getattr(g_usuario_index_schema, "situacao", None):
            where.append("GU.SITUACAO LIKE :situacao")

        # Aplica WHERE
        if where:
            sql += " WHERE " + " AND ".join(where)

        # Ordenação padrão
        sql += " ORDER BY GU.NOME_COMPLETO ASC"

        # Parâmetros da consulta
        params = g_usuario_index_schema.model_dump(exclude_unset=True)

        # Execução da consulta
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response