'use client';

import { DocumentEditor } from '@onlyoffice/document-editor-react';
import { useEffect, useState } from 'react';

import GetDocumentUrl from './actions/GetDocumentUrl';
import GetServerUrl from './actions/GetServerUrl';
import { usePrepareOnlyOfficeEditorHook } from './hooks/usePrepareOnlyOfficeEditorHook';
import { useTokenOnlyOfficeEditorHook } from './hooks/useTokenOnlyOfficeEditorHook';
import OnlyOfficeInteface from './interface/OnlyOfficeInterface';

export default function OnlyOfficeEditor({ id, config }: OnlyOfficeInteface) {
  const { tokenOnlyOfficeEditorHook } = useTokenOnlyOfficeEditorHook();
  const { prepareOnlyOfficeEditorHook } = usePrepareOnlyOfficeEditorHook();
  const [serverUrl, setServerUrl] = useState<string | null>(null);
  const [editorConfig, setEditorConfig] = useState<any>(null);

  async function prepare() {
    try {
      const response = await prepareOnlyOfficeEditorHook();
      const data = structuredClone(config);

      setServerUrl(GetServerUrl(response.data));

      // 🔥 DEBUG 1: Validação da URL do Documento
      const docUrl = GetDocumentUrl(response.data) + '/temp/' + data.document.title;
      data.document.url = docUrl;
      console.log('URL do Documento (verifique se acessível):', docUrl);
      // DICA: Tente abrir esta URL no seu navegador para ver se o arquivo baixa.

      data.editorConfig.user = {
        id: response.data.user.usuario_id,
        name: response.data.user.nome,
      };
      data.editorConfig.mode = 'edit';
      data.editorConfig.lang = 'pt-BR';
      data.editorConfig.callbackUrl =
        response.data.orius_onllyoffice_document_url + '/' + data.editorConfig.orius_api_endpoint;

      // 🔥 DEBUG 2: Logar o CallbackUrl
      console.log('Callback URL (verifique seu backend):', data.editorConfig.callbackUrl);

      data.token = await tokenOnlyOfficeEditorHook(data);

      // 🔥 DEBUG 3: Logar a configuração final antes de carregar
      console.log('Configuração Final do Editor:', data);

      setEditorConfig(data);
    } catch (error) {
      console.error('Erro ao preparar o editor:', error);
    }
  }

  useEffect(() => {
    prepare();
  }, [id, config]);

  return (
    <>
      {serverUrl && editorConfig && (
        <div className="h-full w-full">
          <DocumentEditor
            id={id}
            documentServerUrl={serverUrl}
            config={editorConfig}
            height="100%"
            width="100%"
            // 🔥 DEBUG 4: Evento de erro do OnlyOffice
            onDocumentError={(event) => {
              console.error('Erro detalhado do OnlyOffice:', event);
              // Referência: https://api.onlyoffice.com/docs/docs-api/get-started/how-it-works/lifecycle-of-opening-editor/#message
            }}
          />
        </div>
      )}
    </>
  );
}
