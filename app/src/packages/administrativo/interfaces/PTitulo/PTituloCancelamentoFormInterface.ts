export interface PTituloCancelamentoFormInterface {
  ocorrencia_id: number;
  motivo_cancelamento_id: number;
  data_cancelamento: string;
  servico_gratuito: "S" | "N";
}
