import { PTituloIndexData } from "@/packages/administrativo/data/PTitulo/PTituloIndexData";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import {
  type PCertidaoConsultaApresentantePayload,
  type PCertidaoConsultaApresentanteResult,
} from "@/packages/certidao/interface/PCertidao/PCertidaoConsultaApresentanteInterface";
import {
  PCERTIDAO_FAKE_ENDPOINTS,
  usePCertidaoMockData,
} from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import { withClientErrorHandler } from "@/shared/actions/withClientErrorHandler/withClientErrorHandler";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

function normalizeDigits(value?: string): string {
  return (value ?? "").replace(/\D/g, "");
}

function normalizeName(value: string): string {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

function namesMatch(a?: string, b?: string): boolean {
  if (!a?.trim() || !b?.trim()) return false;
  return normalizeName(a) === normalizeName(b);
}

function docsMatch(docA?: string, docB?: string): boolean {
  const da = normalizeDigits(docA);
  const db = normalizeDigits(docB);
  return Boolean(da.length && db.length && da === db);
}

function getDateOnly(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function getTituloReferenceDate(t: TituloListItem): Date | null {
  const raw = t.data_protesto ?? t.data_intimacao ?? t.data_apontamento;
  if (!raw) return null;
  const d = new Date(raw as string | Date);
  return Number.isNaN(d.getTime()) ? null : d;
}

function isInSearchPeriod(ref: Date | null, dataInicio?: string, dataFim?: string): boolean {
  if (!ref || !dataInicio) return false;
  const from = getDateOnly(new Date(`${dataInicio}T00:00:00`));
  const to = getDateOnly(new Date(`${(dataFim || dataInicio)}T00:00:00`));
  const d = getDateOnly(ref);
  return d >= from && d <= to;
}

function isProtestoAtivoParaCertidao(status?: string): boolean {
  const s = (status ?? "").toLowerCase();
  if (!s.trim()) return false;
  if (/pago|liquidad|cancelad|desist|pendente/.test(s)) return false;
  return true;
}

export async function PCertidaoConsultaApresentanteData(
  payload: PCertidaoConsultaApresentantePayload,
): Promise<PCertidaoConsultaApresentanteResult> {
  if (!usePCertidaoMockData()) {
    const params = new URLSearchParams();
    params.set("apresentante", payload.apresentante.trim());
    params.set("cpfcnpj", payload.cpfcnpj.trim());
    if (payload.data_inicio) params.set("data_inicio", payload.data_inicio);
    if (payload.data_fim) params.set("data_fim", payload.data_fim);

    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: `${PCERTIDAO_FAKE_ENDPOINTS.consultaApresentante}?${params.toString()}`,
      }),
    );
    const response = await apiCall();
    if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
      return response.data as PCertidaoConsultaApresentanteResult;
    }
  }

  const titulos = await PTituloIndexData();
  const base = titulos.filter((t) => {
    const ref = getTituloReferenceDate(t);
    if (!isInSearchPeriod(ref, payload.data_inicio, payload.data_fim)) return false;
    return isProtestoAtivoParaCertidao(t.status_descricao);
  });

  const titulosPorDocumento = base.filter((t) => docsMatch(t.devedor_cpfcnpj, payload.cpfcnpj));
  const docMatchIds = new Set(titulosPorDocumento.map((t) => t.titulo_id));
  const candidatosHomonimia = base.filter(
    (t) =>
      !docMatchIds.has(t.titulo_id) &&
      namesMatch(t.devedor_nome, payload.apresentante) &&
      !docsMatch(t.devedor_cpfcnpj, payload.cpfcnpj),
  );

  return { titulosPorDocumento, candidatosHomonimia };
}
