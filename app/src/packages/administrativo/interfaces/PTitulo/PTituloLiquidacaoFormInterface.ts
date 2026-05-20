export interface PTituloLiquidacaoFormInterface {
  ocorrencia_id: number;
  motivo_cancelamento_id: number;
  data_liquidacao: string;
  servico_gratuito: "S" | "N";
}
