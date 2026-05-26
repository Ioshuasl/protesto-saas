export type PCertidaoIndexQuery = {
  tipo_certidao?: "P" | "N";
  data_certidao?: string;
  data_inicio?: string;
  data_fim?: string;
  status?: "A" | "C";
  busca?: string;
  page?: number;
  per_page?: number;
};
