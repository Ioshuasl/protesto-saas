'use server';

import { PBANCO_ENDPOINTS } from '@/packages/administrativo/data/PBanco/pbancoDataConfig';
import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import { parsePBancoRecord } from '@/packages/administrativo/utils/parsePBancoRecord';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

function buildCodigoCandidates(codigoBanco: string): string[] {
  const normalized = codigoBanco.trim().toUpperCase();
  if (!normalized) return [];

  const candidates = new Set<string>([normalized]);
  if (/^\d+$/.test(normalized)) {
    const stripped = normalized.replace(/^0+/, '') || '0';
    candidates.add(stripped);
    candidates.add(normalized.padStart(3, '0'));
  }

  return [...candidates];
}

async function fetchBancoByCodigo(api: API, codigo: string): Promise<PBancoInterface | undefined> {
  const response = await api.send({
    method: Methods.GET,
    endpoint: PBANCO_ENDPOINTS.showByCodigo(codigo),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300) {
    const parsed = parsePBancoRecord(response?.data ?? response);
    if (parsed) return parsed;
  }

  return undefined;
}

async function executePBancoShowByCodigoData(
  codigoBanco: string,
): Promise<PBancoInterface | undefined> {
  const candidates = buildCodigoCandidates(codigoBanco);
  if (candidates.length === 0) return undefined;

  const api = new API();
  for (const codigo of candidates) {
    const banco = await fetchBancoByCodigo(api, codigo);
    if (banco) return banco;
  }

  return undefined;
}

export const PBancoShowByCodigoData = withClientErrorHandler(executePBancoShowByCodigoData);
