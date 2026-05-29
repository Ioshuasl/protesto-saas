'use server';

import { P_TEMPLATE_ONLYOFFICE_CUSTOMIZATION } from '@/packages/administrativo/constants/pTemplateOnlyOfficeCustomization';
import { PTEMPLATE_ENDPOINTS } from '@/packages/administrativo/data/PTemplate/pTemplateDataConfig';
import type { PTemplateMarkerLegend } from '@/packages/administrativo/interfaces/PTemplate/PTemplateMarkerLegend';
import type { PTemplateOnlyOfficeConfig } from '@/packages/administrativo/interfaces/PTemplate/PTemplateOnlyOfficeConfig';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

type PTemplateOpenEditorResponse = {
  template_id: number;
  document?: {
    fileType?: string;
    key?: string;
    title?: string;
    url?: string;
  };
  editorConfig?: {
    callbackUrl?: string;
    mode?: string;
    lang?: string;
    customization?: typeof P_TEMPLATE_ONLYOFFICE_CUSTOMIZATION;
  };
  markerLegend?: PTemplateMarkerLegend;
};

export type PTemplateOpenEditorResult = {
  config: PTemplateOnlyOfficeConfig;
  markerLegend?: PTemplateMarkerLegend;
};

function basenameFromUrl(urlValue: string | undefined): string | undefined {
  if (!urlValue) return undefined;
  try {
    const parsed = new URL(urlValue);
    const parts = parsed.pathname.split('/').filter(Boolean);
    return parts[parts.length - 1];
  } catch {
    const parts = urlValue.split('/').filter(Boolean);
    return parts[parts.length - 1];
  }
}

function toRelativeEndpoint(callbackUrl: string | undefined): string | undefined {
  if (!callbackUrl) return undefined;
  try {
    const parsed = new URL(callbackUrl);
    return `${parsed.pathname.replace(/^\//, '')}${parsed.search || ''}`;
  } catch {
    return callbackUrl.replace(/^\//, '');
  }
}

function toOnlyOfficeConfig(payload: PTemplateOpenEditorResponse): PTemplateOnlyOfficeConfig {
  const fileUrl = payload.document?.url;
  const callbackUrl = payload.editorConfig?.callbackUrl;
  const fileNameFromUrl = basenameFromUrl(fileUrl);
  const title = fileNameFromUrl || payload.document?.title || `template_${payload.template_id}.docx`;
  const callbackEndpoint = toRelativeEndpoint(callbackUrl);

  return {
    documentType: 'word',
    document: {
      fileType: payload.document?.fileType || 'docx',
      key: payload.document?.key || `p_template_${payload.template_id}`,
      title,
      url: fileUrl,
      permissions: {
        edit: true,
        download: true,
      },
    },
    editorConfig: {
      mode: payload.editorConfig?.mode || 'edit',
      lang: payload.editorConfig?.lang || 'pt-BR',
      orius_api_endpoint: callbackEndpoint,
      customization:
        payload.editorConfig?.customization ?? P_TEMPLATE_ONLYOFFICE_CUSTOMIZATION,
    },
  };
}

async function executePTemplateOpenEditorData(
  templateId: number,
  mode: 'edit' | 'view' = 'edit',
): Promise<PTemplateOpenEditorResult> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PTEMPLATE_ENDPOINTS.openEditor(templateId, mode),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    const payload = response.data as PTemplateOpenEditorResponse;
    return {
      config: toOnlyOfficeConfig(payload),
      markerLegend: payload.markerLegend,
    };
  }

  throw new Error(response?.message ?? 'Erro ao abrir editor da minuta');
}

export const PTemplateOpenEditorData = withClientErrorHandler(executePTemplateOpenEditorData);

