export interface ReceitaWsAtividade {
  code: string;
  text: string;
}

export interface ReceitaWsQsa {
  nome: string;
  qual: string;
}

export interface ReceitaWsResponse {
  abertura?: string;
  situacao?: string;
  tipo?: string;
  nome?: string;
  fantasia?: string;
  porte?: string;
  natureza_juridica?: string;
  atividade_principal?: ReceitaWsAtividade[];
  atividades_secundarias?: ReceitaWsAtividade[];
  qsa?: ReceitaWsQsa[];
  logradouro?: string;
  numero?: string;
  complemento?: string;
  municipio?: string;
  bairro?: string;
  uf?: string;
  cep?: string;
  email?: string;
  telefone?: string;
  data_situacao?: string;
  cnpj?: string;
  ultima_atualizacao?: string;
  status?: string;
  efr?: string;
  motivo_situacao?: string;
  situacao_especial?: string;
  data_situacao_especial?: string;
  capital_social?: string;
  simples?: {
    optante?: boolean;
    data_opcao?: string;
    data_exclusao?: string | null;
    ultima_atualizacao?: string;
  };
  simei?: {
    optante?: boolean;
    data_opcao?: string;
    data_exclusao?: string | null;
    ultima_atualizacao?: string;
  };
  extra?: Record<string, unknown>;
  billing?: {
    free?: boolean;
    database?: boolean;
  };
  message?: string;
}

const RECEITA_WS_BASE_URL = "/api/receitaws/v1/cnpj";

export function sanitizeCnpj(value: string): string {
  return value.replace(/\D/g, "");
}

export async function consultarCnpj(cnpj: string): Promise<ReceitaWsResponse> {
  const cnpjLimpo = sanitizeCnpj(cnpj);

  if (cnpjLimpo.length !== 14) {
    throw new Error("CNPJ inválido. Informe 14 dígitos.");
  }

  const response = await fetch(`${RECEITA_WS_BASE_URL}/${cnpjLimpo}`);

  if (!response.ok) {
    throw new Error(`Falha ao consultar CNPJ (HTTP ${response.status}).`);
  }

  const data = (await response.json()) as ReceitaWsResponse;

  if (data.status && data.status.toUpperCase() !== "OK") {
    throw new Error(data.message || "ReceitaWS retornou erro na consulta de CNPJ.");
  }

  return data;
}
