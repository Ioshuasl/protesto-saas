import db from "@/db.json";
import { pbancoListRef } from "@/packages/administrativo/data/PBanco/pbancoInMemory";
import { ptituloListRef } from "@/packages/administrativo/data/PTitulo/ptituloInMemory";
import type { PEspecieInterface } from "@/packages/administrativo/interfaces/PEspecie/PEspecieInterface";
import type {
  PTituloInterface,
  PTituloTipoAceite,
  PTituloTipoEndosso,
} from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import { mockDbDelay } from "@/packages/administrativo/shared/mockDbDelay";
import type {
  CraImportacaoSavePayload,
  CraImportacaoSaveResult,
} from "@/packages/cra/interface/CraImportacao/CraImportacaoSaveInterface";
import { pArquivoTituloListRef } from "@/packages/cra/data/PTituloArquivo/pArquivoTituloInMemory";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import { CRAIMPORTACAO_FAKE_ENDPOINTS, useCraImportacaoMockData } from "@/packages/cra/data/CraImportacao/craImportacaoDataConfig";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

const especies: PEspecieInterface[] = [...(db.especies as unknown as PEspecieInterface[])];

function parseIsoDate(value?: string): Date | undefined {
  if (!value) return undefined;
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) return undefined;
  return date;
}

function resolveEspecieId(especieSigla: string): number | undefined {
  const normalized = especieSigla.trim().toUpperCase();
  if (!normalized) return undefined;
  return especies.find((item) => (item.especie ?? "").trim().toUpperCase() === normalized)?.especie_id;
}

function mapTipoAceite(tipoAceite: string): PTituloTipoAceite {
  return tipoAceite === "A" ? "A" : "E";
}

function mapTipoEndosso(tipoEndosso: string): PTituloTipoEndosso {
  return tipoEndosso === "T" ? "T" : "M";
}

export async function CraImportacaoSaveData(
  data: CraImportacaoSavePayload,
): Promise<CraImportacaoSaveResult> {
  if (!useCraImportacaoMockData()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.POST,
        endpoint: CRAIMPORTACAO_FAKE_ENDPOINTS.save,
        body: data,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as CraImportacaoSaveResult;
    }
  }

  await mockDbDelay(700);

  const list = ptituloListRef.current;
  const maxId = list.length > 0 ? Math.max(...list.map((item) => item.titulo_id)) : 0;

  const createdTitulos = data.remessa.transacoes.map((transacao, index) => {
    const tituloId = maxId + index + 1;
    const valorTitulo = transacao.valorTituloCentavos / 100;
    const valorSaldo = transacao.saldoTituloCentavos / 100;

    const titulo: PTituloInterface = {
      titulo_id: tituloId,
      banco_id: data.banco_id,
      ocorrencia_id: 1,
      situacao_aceite: "Apontado",
      status_importacao: "E",
      especie_id: resolveEspecieId(transacao.especie),
      agencia_codigo_cedente: transacao.agenciaCodigoCedente || undefined,
      numero_titulo: transacao.numeroTitulo || undefined,
      numero_titulo_banco: transacao.numeroTitulo || undefined,
      nosso_numero: transacao.nossoNumero || undefined,
      tipo_endosso: mapTipoEndosso(transacao.tipoEndosso),
      tipo_aceite: mapTipoAceite(transacao.tipoAceite),
      valor_titulo: valorTitulo,
      valor_total: valorSaldo,
      praca_pagamento: transacao.pracaProtesto || undefined,
      data_emissao_titulo: parseIsoDate(transacao.dataEmissao),
      data_vencimento_titulo: parseIsoDate(transacao.dataVencimento),
      data_cadastro: new Date(),
    };

    return titulo;
  });

  list.push(...createdTitulos);

  const result: CraImportacaoSaveResult = {
    importacao_id: `CRA-${Date.now()}`,
    banco_id: data.banco_id,
    file_name: data.remessa.fileName,
    imported_count: createdTitulos.length,
    titulo_ids: createdTitulos.map((titulo) => titulo.titulo_id),
    nosso_numeros: createdTitulos.map((titulo) => titulo.nosso_numero ?? ""),
  };

  const banco = pbancoListRef.current.find((item) => item.banco_id === data.banco_id);
  const arquivoList = pArquivoTituloListRef.current;
  const nextArquivoId =
    arquivoList.length > 0 ? Math.max(...arquivoList.map((item) => item.arquivo_titulo_id)) + 1 : 1;

  const importedFileRecord: PArquivoTituloInterface = {
    arquivo_titulo_id: nextArquivoId,
    data_importacao: new Date(),
    quantidade: createdTitulos.length,
    data_movimento: data.remessa.header.dataMovimento,
    numero_sequencial: String(data.remessa.header.sequenciaRemessa),
    qtde_registros: String(data.remessa.header.quantidadeRegistros),
    qtde_titulos: String(data.remessa.header.quantidadeTitulos),
    qtde_indicacoes: String(data.remessa.header.quantidadeIndicacoes),
    qtde_originais: String(data.remessa.header.quantidadeOriginais),
    soma_vlr_remessa: data.remessa.trailer.somaValoresCentavos / 100,
    soma_qtde_remessa: createdTitulos.length,
    nome_arquivo: data.remessa.fileName,
    portador_nome: banco?.descricao ?? data.remessa.header.nomePortador,
    portador_codigo: banco?.codigo_banco ?? data.remessa.header.codigoPortador,
    codigo_praca: data.remessa.header.codigoIbgeMunicipio,
    sequencial_header: String(data.remessa.header.sequenciaRegistro),
    sequencial_footer: String(data.remessa.trailer.sequenciaRegistro),
    id_transacao_remetente: data.remessa.header.remetente,
    id_transacao_destinatario: data.remessa.header.destinatario,
    id_transacao_tipo: data.remessa.header.tipoTransacao,
    versao_layout: data.remessa.header.versaoLayout,
    complemento_header: `Importação CRA com ${createdTitulos.length} título(s)`,
  };
  pArquivoTituloListRef.current.unshift(importedFileRecord);

  return result;
}
