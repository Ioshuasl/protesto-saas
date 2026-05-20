export default interface ConfirmDialogInterface {
  /** Controla a abertura do modal */
  isOpen: boolean;

  /** Título principal do alerta */
  title: string;

  /** Descrição adicional do alerta */
  description?: string;

  /** Mensagem do corpo do alerta */
  message: string;

  /** Texto do botão de confirmação */
  confirmText?: string;

  /** Texto do botão de cancelamento */
  cancelText?: string;

  /** Função executada ao confirmar */
  onConfirm: () => void;

  /** Função executada ao cancelar */
  onCancel: () => void;
}
