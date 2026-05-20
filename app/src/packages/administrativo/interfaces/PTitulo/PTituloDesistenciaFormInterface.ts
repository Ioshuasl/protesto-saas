export interface PTituloDesistenciaFormInterface {
  ocorrencia_id: number;
  motivo_cancelamento_id: number;
  data_desistencia: string;
  servico_gratuito: "S" | "N";
}
