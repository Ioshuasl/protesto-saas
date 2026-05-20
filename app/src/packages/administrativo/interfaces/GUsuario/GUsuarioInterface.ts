/**
 * Interface gerada para a tabela G_USUARIO
 */
export interface GUsuarioInterface {
  andamento_padrao2?: number;
  andamento_padrao?: number;
  data_expiracao?: Date;
  ultimo_login_regs?: Date;
  ultimo_login?: Date;
  usuario_id: number;
  login?: string;
  usuario_tab?: number;
  foto?: string;
  sigla?: string;
  senha_anterior?: string;
  lembrete_resposta?: string;
  lembrete_pergunta?: string;
  senha?: string;
  nome_completo?: string;
  funcao?: string;
  email?: string;
  receber_mensagem_arrolamento?: string;
  trocarsenha?: string;
  situacao?: string;
  assina?: string;
  assina_certidao?: string;
  receber_email_penhora?: string;
  nao_receber_chat_todos?: string;
  pode_alterar_caixa?: string;
  receber_chat_certidao_online?: string;
  receber_chat_cancelamento?: string;
  cpf?: string;
  somente_leitura?: string;
  receber_chat_envio_onr?: string;
  tipo_usuario?: string;
  distribuir_protocolo_ri?: string;
  ultimo_protocolo_ri?: number;
  adm_distribuir_protocolo_ri?: string;
  senha_api?: string;
}
