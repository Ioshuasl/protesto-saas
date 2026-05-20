export interface ViaCepResponse {
  cep?: string;
  logradouro?: string;
  complemento?: string;
  unidade?: string;
  bairro?: string;
  localidade?: string;
  uf?: string;
  estado?: string;
  regiao?: string;
  ibge?: string;
  gia?: string;
  ddd?: string;
  siafi?: string;
  erro?: boolean;
}

const VIA_CEP_BASE_URL = "/api/viacep/ws";

export function sanitizeCep(value: string): string {
  return value.replace(/\D/g, "");
}

export async function consultarCep(cep: string): Promise<ViaCepResponse> {
  const cepLimpo = sanitizeCep(cep);

  if (cepLimpo.length !== 8) {
    throw new Error("CEP inválido. Informe 8 dígitos.");
  }

  const response = await fetch(`${VIA_CEP_BASE_URL}/${cepLimpo}/json`);

  if (!response.ok) {
    throw new Error(`Falha ao consultar CEP (HTTP ${response.status}).`);
  }

  const data = (await response.json()) as ViaCepResponse;

  if (data.erro) {
    throw new Error("CEP não encontrado.");
  }

  return data;
}
