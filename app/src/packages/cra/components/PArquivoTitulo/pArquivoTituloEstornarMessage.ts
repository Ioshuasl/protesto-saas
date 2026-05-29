import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";

function formatNumerosApontamentoLista(
  titulos: PArquivoTituloInterface["titulos"],
): string {
  if (!titulos?.length) {
    return "nenhum título vinculado";
  }

  const numeros = titulos
    .map((titulo) => titulo.numero_apontamento)
    .filter((numero): numero is number => numero != null);

  if (numeros.length === 0) {
    return "sem número de apontamento";
  }

  return numeros.join(", ");
}

export function buildEstornarRemessaConfirmMessage(
  arquivo: PArquivoTituloInterface,
): string {
  const listaNumerosApontamento = formatNumerosApontamentoLista(arquivo.titulos);

  return `Você realmente deseja estornar essa remessa? Os títulos (${listaNumerosApontamento}) e os selos também serão estornados automaticamente.`;
}
