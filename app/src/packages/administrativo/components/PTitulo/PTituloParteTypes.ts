"use client";

export interface PTituloParteItem {
  pessoa_id?: number;
  tipo: string;
  descricao: string;
  nome?: string;
  cpfcnpj?: string;
}

export const pTituloParteRoleOptions = [
  { value: "A", label: "Apresentante" },
  { value: "D", label: "Devedor" },
  { value: "R", label: "Credor" },
  { value: "C", label: "Cedente" },
  { value: "E", label: "Endossante" },
  { value: "V", label: "Avalista" },
  { value: "S", label: "Sacador" },
  { value: "P", label: "Portador" },
  { value: "O", label: "Outros" },
] as const;

export const pTituloParteRoleLabelMap: Map<string, string> = new Map(
  pTituloParteRoleOptions.map((item) => [item.value, item.label]),
);
