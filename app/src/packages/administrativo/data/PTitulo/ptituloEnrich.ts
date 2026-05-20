import db from "@/db.json";
import type { PEspecieInterface } from "@/packages/administrativo/interfaces/PEspecie/PEspecieInterface";
import type { POcorrenciasInterface } from "@/packages/administrativo/interfaces/POcorrencias/POcorrenciasInterface";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import { pPessoaVinculoListRef } from "@/packages/administrativo/data/PTitulo/ptituloPessoasVinculoInMemory";

const especies: PEspecieInterface[] = [...(db.especies as unknown as PEspecieInterface[])];
const ocorrencias: POcorrenciasInterface[] = [...(db.ocorrencias as unknown as POcorrenciasInterface[])];
const pessoas: PPessoaInterface[] = [...(db.pessoas as unknown as PPessoaInterface[])];
function resolveStatus(titulo: PTituloInterface): string {
  if (titulo.situacao_aceite) return titulo.situacao_aceite;
  const ocorrencia = ocorrencias.find((o) => o.ocorrencias_id === titulo.ocorrencia_id);
  return ocorrencia?.descricao ?? "Sem status";
}

export function mapStatusToOcorrencia(status: string): number | undefined {
  const statusLower = status.toLowerCase();
  if (statusLower.includes("protest")) return 3;
  if (statusLower.includes("liquid") || statusLower.includes("pago")) return 4;
  if (statusLower.includes("cancel") || statusLower.includes("desist")) return 5;
  if (statusLower.includes("tríduo") || statusLower.includes("triduo") || statusLower.includes("intima")) return 2;
  if (statusLower.includes("apont")) return 1;
  return undefined;
}

export function enrichTitulo(titulo: PTituloInterface): TituloListItem {
  const especie = especies.find((e) => e.especie_id === titulo.especie_id);

  const vinculosDoTitulo = pPessoaVinculoListRef.current.filter((v) => v.titulo_id === titulo.titulo_id);
  const tipoDescricaoMap: Record<string, string> = {
    A: "Apresentante",
    D: "Devedor",
    C: "Cedente",
    R: "Credor",
    E: "Endossante",
    V: "Avalista",
    S: "Sacador",
    P: "Portador",
  };

  const vinculosPartes = vinculosDoTitulo.map((v) => {
    const pessoa = pessoas.find((p) => p.pessoa_id === v.pessoa_id);
    const tipo = (v.tipo_vinculo ?? "").toUpperCase();
    return {
      tipo,
      descricao: tipoDescricaoMap[tipo] ?? "Outro Vínculo",
      pessoa_vinculo_id: v.pessoa_vinculo_id,
      devedor_tipo_aceite: v.devedor_tipo_aceite,
      devedor_data_aceite: v.devedor_data_aceite,
      nome: v.nome ?? pessoa?.nome,
      cpfcnpj: v.cpfcnpj ?? pessoa?.cpfcnpj,
    };
  });

  const devedorVinculo =
    vinculosDoTitulo.find((v) => (v.tipo_vinculo ?? "").toUpperCase() === "D") ?? vinculosDoTitulo[0];
  const apresentanteVinculo = vinculosDoTitulo.find((v) => (v.tipo_vinculo ?? "").toUpperCase() === "A");
  const credorVinculo = vinculosDoTitulo.find((v) => (v.tipo_vinculo ?? "").toUpperCase() === "R");
  const cedenteVinculo = vinculosDoTitulo.find((v) => (v.tipo_vinculo ?? "").toUpperCase() === "C");

  const devedorPessoa = pessoas.find((p) => p.pessoa_id === devedorVinculo?.pessoa_id);
  const apresentantePessoa = pessoas.find((p) => p.pessoa_id === apresentanteVinculo?.pessoa_id);
  const credorPessoa = pessoas.find((p) => p.pessoa_id === credorVinculo?.pessoa_id);
  const cedentePessoa = pessoas.find((p) => p.pessoa_id === cedenteVinculo?.pessoa_id);

  const partesLabel = vinculosPartes.map((p) => `${p.descricao}: ${p.nome ?? "-"}`).join(" | ");

  const partesDocumentos = vinculosPartes
    .map((p) => p.cpfcnpj)
    .filter(Boolean)
    .join(" | ");

  return {
    ...titulo,
    devedor_nome: devedorVinculo?.nome ?? devedorPessoa?.nome,
    devedor_cpfcnpj: devedorVinculo?.cpfcnpj ?? devedorPessoa?.cpfcnpj,
    apresentante_nome: apresentanteVinculo?.nome ?? apresentantePessoa?.nome,
    apresentante_cpfcnpj: apresentanteVinculo?.cpfcnpj ?? apresentantePessoa?.cpfcnpj,
    credor_nome: credorVinculo?.nome ?? credorPessoa?.nome,
    cedente_nome: cedenteVinculo?.nome ?? cedentePessoa?.nome,
    partes_label: partesLabel,
    partes_documentos: partesDocumentos,
    vinculos_partes: vinculosPartes,
    especie_sigla: especie?.especie,
    status_descricao: resolveStatus(titulo),
  };
}
