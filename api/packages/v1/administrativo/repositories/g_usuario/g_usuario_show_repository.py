from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSchema


class ShowRepository(BaseRepository):

    def execute(self, usuario_schema: GUsuarioSchema):
        
        # Montagem do sql
        # SQL explícito com todas as colunas da tabela
        sql = """
        SELECT
            gu.USUARIO_ID,
            gu.TROCARSENHA,
            gu.LOGIN,
            gu.SENHA,
            gu.SITUACAO,
            gu.NOME_COMPLETO,
            gu.FUNCAO,
            gu.ASSINA,
            gu.SIGLA,
            gu.USUARIO_TAB,
            gu.ULTIMO_LOGIN,
            gu.ULTIMO_LOGIN_REGS,
            gu.DATA_EXPIRACAO,
            gu.SENHA_ANTERIOR,
            gu.ANDAMENTO_PADRAO,
            gu.LEMBRETE_PERGUNTA,
            gu.LEMBRETE_RESPOSTA,
            gu.ANDAMENTO_PADRAO2,
            gu.RECEBER_MENSAGEM_ARROLAMENTO,
            gu.EMAIL,
            gu.ASSINA_CERTIDAO,
            gu.RECEBER_EMAIL_PENHORA,
            gu.FOTO,
            gu.NAO_RECEBER_CHAT_TODOS,
            gu.PODE_ALTERAR_CAIXA,
            gu.RECEBER_CHAT_CERTIDAO_ONLINE,
            gu.RECEBER_CHAT_CANCELAMENTO,
            gu.CPF,
            gu.SOMENTE_LEITURA,
            gu.RECEBER_CHAT_ENVIO_ONR,
            gu.TIPO_USUARIO,
            gu.DISTRIBUIR_PROTOCOLO_RI,
            gu.ULTIMO_PROTOCOLO_RI
        FROM G_USUARIO gu
        WHERE gu.USUARIO_ID = :usuarioId
        """

        # Preenchimento de parâmetros
        params = {
            'usuarioId': usuario_schema.usuario_id
        }

        # Execução do sql
        return self.fetch_one(sql, params)