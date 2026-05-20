export interface PCertidaoFormValues {
  certidao_id?: number;
  apresentante: string;
  cpfcnpj: string;
  tipo_certidao: "P" | "N";
  status: "A" | "C";
  data_certidao?: Date;
  hora_certidao: string;
  usuario_id?: number;
  observacao: string;
  /** Preenchido na emissão guiada quando há resultado positivo. */
  qtd_protestos?: number;
}
