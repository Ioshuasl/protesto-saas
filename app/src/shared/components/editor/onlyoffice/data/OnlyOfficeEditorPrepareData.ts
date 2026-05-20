import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import ApiResponseInterface from '@/shared/services/api/interfaces/ApiResponseInterface';

async function executeOnlyOfficeEditorPrepareData(): Promise<ApiResponseInterface> {
  return {
    status: 200,
    message: 'Dados carregados com sucesso',
    data: {
      orius_onllyoffice_document_url: process.env.NEXT_PUBLIC_ORIUS_ONLYOFFICE_DOCUMENT_URL,
      orius_onllyoffice_url: process.env.NEXT_PUBLIC_ORIUS_ONLYOFFICE_URL,
      orius_app_api_url: process.env.NEXT_PUBLIC_ORIUS_APP_API_URL,
      orius_app_api_prefix_api: process.env.NEXT_PUBLIC_ORIUS_APP_API_PREFIX,
    },
  };
}

export const OnlyOfficeEditorPrepareData = withClientErrorHandler(
  executeOnlyOfficeEditorPrepareData,
);
