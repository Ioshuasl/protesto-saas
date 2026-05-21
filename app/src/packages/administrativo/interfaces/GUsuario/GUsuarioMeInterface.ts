/** Payload em `data` da rota `administrativo/g_usuario/me` */
export default interface GUsuarioMe {
  usuario_id: number;
  trocarsenha: string | null;
  login: string | null;
  senha: string | null;
  situacao: string | null;
  nome_completo: string | null;
  funcao: string | null;
  assina: string | null;
  sigla: string | null;
  usuario_tab: string | null;
  ultimo_login: string | null;
  ultimo_login_regs: string | null;
  data_expiracao: string | null;
  senha_anterior: string | null;
  andamento_padrao: string | null;
  lembrete_pergunta: string | null;
  lembrete_resposta: string | null;
  andamento_padrao2: string | null;
  receber_mensagem_arrolamento: string | null;
  email: string | null;
  assina_certidao: string | null;
  receber_email_penhora: string | null;
  foto: string | null;
  nao_receber_chat_todos: string | null;
  pode_alterar_caixa: string | null;
  receber_chat_certidao_online: string | null;
  receber_chat_cancelamento: string | null;
  cpf: string | null;
  somente_leitura: string | null;
  receber_chat_envio_onr: string | null;
  tipo_usuario: string | null;
  distribuir_protocolo_ri: string | null;
  ultimo_protocolo_ri: string | null;
  senha_api: string | null;
}
