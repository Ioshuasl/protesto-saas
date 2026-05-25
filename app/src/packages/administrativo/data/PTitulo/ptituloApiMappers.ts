import { sortPTituloSelosVinculados } from '@/packages/administrativo/data/PTitulo/ptituloSelosUtils';
import type { PTituloIndexItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloIndexItem';
import type { PTituloInterface } from '@/packages/administrativo/interfaces/PTitulo/PTituloInterface';
import type { PTituloSeloVinculadoItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloSeloVinculadoItem';
import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import {
  formatPPessoaVinculoTipoLabel,
  normalizePPessoaVinculoTipo,
} from '@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoTipoEnum';

type PessoaVinculoApi = {
  pessoa_vinculo_id?: number;
  titulo_id?: number;
  pessoa_id?: number;
  nome?: string;
  cpfcnpj?: string;
  tipo_vinculo?: string;
  devedor_microempresa?: unknown;
  devedor_tipo_aceite?: string;
  devedor_data_aceite?: Date | string;
  pessoa?: { pessoa_id?: number; nome?: string; cpfcnpj?: string; micro_empresa?: unknown };
};

function resolveTipoVinculo(tipo?: string): string {
  return normalizePPessoaVinculoTipo(tipo) ?? (tipo ?? '').trim().toUpperCase();
}

function resolveStatusDescricao(titulo: {
  situacao_aceite?: string;
  ocorrencia?: { descricao?: string } | null;
}): string | undefined {
  if (titulo.situacao_aceite?.trim()) return titulo.situacao_aceite.trim();
  return titulo.ocorrencia?.descricao?.trim() || undefined;
}

function mapPessoaVinculosToPartes(vinculos: PessoaVinculoApi[]) {
  return vinculos.map((v) => {
    const tipo = resolveTipoVinculo(v.tipo_vinculo);
    const pessoa = v.pessoa;
    return {
      tipo,
      descricao: formatPPessoaVinculoTipoLabel(tipo),
      pessoa_vinculo_id: v.pessoa_vinculo_id,
      devedor_tipo_aceite: v.devedor_tipo_aceite,
      devedor_microempresa: v.devedor_microempresa,
      devedor_data_aceite: v.devedor_data_aceite
        ? new Date(v.devedor_data_aceite as string | Date)
        : undefined,
      nome: v.nome ?? pessoa?.nome,
      cpfcnpj: v.cpfcnpj ?? pessoa?.cpfcnpj,
      micro_empresa: pessoa?.micro_empresa,
    };
  });
}

export function mapIndexItemToTituloListItem(row: PTituloIndexItem): TituloListItem {
  const statusDescricao = resolveStatusDescricao({
    ocorrencia: row.ocorrencia ?? undefined,
  });
  const vinculosPartes = mapPessoaVinculosToPartes(row.pessoa_vinculos ?? []);

  return {
    titulo_id: row.titulo_id,
    data_intimacao: row.data_intimacao ? new Date(row.data_intimacao) : undefined,
    data_protesto: row.data_protesto ? new Date(row.data_protesto) : undefined,
    data_aceite: row.data_aceite ? new Date(row.data_aceite) : undefined,
    data_apontamento: row.data_apontamento ? new Date(row.data_apontamento) : undefined,
    data_cancelamento: row.data_cancelamento ? new Date(row.data_cancelamento) : undefined,
    data_emissao_titulo: row.data_emissao_titulo ? new Date(row.data_emissao_titulo) : undefined,
    data_cadastro: row.data_cadastro ? new Date(row.data_cadastro) : undefined,
    data_sustado: row.data_sustado ? new Date(row.data_sustado) : undefined,
    data_pago: row.data_pago ? new Date(row.data_pago) : undefined,
    livro_id_protesto: row.livro_id_protesto,
    folha_protesto: row.folha_protesto,
    numero_titulo: row.numero_titulo,
    nosso_numero: row.nosso_numero,
    numero_apontamento: row.numero_apontamento,
    especie_id: row.especie_id,
    valor_titulo: row.valor_titulo,
    ocorrencia_id: row.ocorrencia_id ?? row.ocorrencia?.ocorrencias_id,
    banco_id: row.banco_id ?? row.banco?.banco_id,
    apresentante_nome: row.apresentante_nome,
    apresentante_cpfcnpj: row.apresentante_cpfcnpj,
    especie: row.especie ?? null,
    especie_sigla: row.especie?.especie,
    status_descricao: statusDescricao,
    vinculos_partes: vinculosPartes,
    partes_label: row.apresentante_nome ? `Apresentante: ${row.apresentante_nome}` : '',
    partes_documentos: row.apresentante_cpfcnpj ?? '',
  };
}

export function enrichTituloFromApi(
  titulo: PTituloInterface & {
    pessoa_vinculos?: PessoaVinculoApi[];
    vinculos_selos?: PTituloSeloVinculadoItem[];
    ocorrencia?: { ocorrencias_id?: number; descricao?: string };
    especie?: { especie_id?: number; descricao?: string; especie?: string };
    banco?: { banco_id?: number; descricao?: string; codigo_banco?: string };
  },
): TituloListItem {
  const vinculos = titulo.pessoa_vinculos ?? [];

  const vinculosPartes = mapPessoaVinculosToPartes(vinculos);

  const findByTipo = (tipo: string) => vinculosPartes.find((v) => v.tipo === tipo);

  const devedor = findByTipo('DEVEDOR') ?? vinculosPartes[0];
  const apresentante = findByTipo('APRESENTANTE');
  const credor = findByTipo('CREDOR');
  const cedente = findByTipo('CEDENTE');

  const partesLabel = vinculosPartes.map((p) => `${p.descricao}: ${p.nome ?? '-'}`).join(' | ');
  const partesDocumentos = vinculosPartes
    .map((p) => p.cpfcnpj)
    .filter(Boolean)
    .join(' | ');

  return {
    ...titulo,
    especie_id: titulo.especie_id ?? titulo.especie?.especie_id,
    banco_id: titulo.banco_id ?? titulo.banco?.banco_id,
    ocorrencia_id: titulo.ocorrencia_id ?? titulo.ocorrencia?.ocorrencias_id,
    especie: titulo.especie ?? null,
    banco: titulo.banco ?? null,
    devedor_nome: devedor?.nome,
    devedor_cpfcnpj: devedor?.cpfcnpj,
    apresentante_nome: apresentante?.nome,
    apresentante_cpfcnpj: apresentante?.cpfcnpj,
    credor_nome: credor?.nome,
    cedente_nome: cedente?.nome,
    partes_label: partesLabel,
    partes_documentos: partesDocumentos,
    vinculos_partes: vinculosPartes,
    vinculos_selos: Array.isArray(titulo.vinculos_selos)
      ? sortPTituloSelosVinculados(titulo.vinculos_selos)
      : undefined,
    especie_sigla: titulo.especie?.especie ?? titulo.especie?.descricao,
    status_descricao: resolveStatusDescricao(titulo),
  };
}
