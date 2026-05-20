export default interface ConfirmDialogSimpleInterface {
  /** Título principal do alerta */
  title: string;

  /** Descrição adicional do alerta */
  description: string;

  /** Mensagem do corpo do alerta */
  message: string;

  /** Texto do botão de confirmação */
  confirm: string;

  /** Texto do botão de cancelamento */
  cancel: string;
}
