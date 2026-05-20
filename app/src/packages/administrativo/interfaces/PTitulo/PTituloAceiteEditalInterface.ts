import type { PTituloTipoAceite } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";

export interface PTituloAceiteEditalDevedorInterface {
  pessoa_vinculo_id: number;
  devedor_tipo_aceite: PTituloTipoAceite;
  devedor_data_aceite: string;
}

export interface PTituloAceiteEditalInterface {
  devedores: PTituloAceiteEditalDevedorInterface[];
}

