'use server';

import { PTEMPLATE_ENDPOINTS } from '@/packages/administrativo/data/PTemplate/pTemplateDataConfig';
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
  };
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
    },
  };
}

async function executePTemplateOpenEditorData(
  templateId: number,
  mode: 'edit' | 'view' = 'edit',
): Promise<PTemplateOnlyOfficeConfig> {
  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: PTEMPLATE_ENDPOINTS.openEditor(templateId, mode),
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return toOnlyOfficeConfig(response.data as PTemplateOpenEditorResponse);
  }

  throw new Error(response?.message ?? 'Erro ao abrir editor da minuta');
}

export const PTemplateOpenEditorData = withClientErrorHandler(executePTemplateOpenEditorData);

