import type { PTituloTipoAceite } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";

export interface PTituloShowDevedoresItem {
  titulo_id: number;
  pessoa_vinculo_id: number;
  devedor_nome?: string;
  devedor_cpfcnpj?: string;
  devedor_tipo_aceite?: PTituloTipoAceite;
  devedor_data_aceite?: Date;
}

