export default interface FilesViewDialogInterface {
  isOpen: boolean;
  onClose: (open: boolean) => void;
  /** URL ou caminho do arquivo. Quando null/undefined, exibe estado vazio. */
  filePath?: string | null;
  /** Título do dialog. Se omitido, usa o nome do arquivo extraído do path. */
  title?: string;
  /** Chamado ao clicar em Baixar; se omitido, abre filePath em nova aba. */
  onDownload?: () => void;
  /** Exibe o botão Baixar no rodapé. Padrão true. */
  showDownloadButton?: boolean;
}
