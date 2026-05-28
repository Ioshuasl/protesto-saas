import { useState } from 'react';

import { PTemplateOpenEditorService } from '@/packages/administrativo/services/PTemplate/PTemplateOpenEditorService';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import type { PTemplateOnlyOfficeConfig } from '@/packages/administrativo/interfaces/PTemplate/PTemplateOnlyOfficeConfig';
import { useResponse } from '@/shared/components/response/ResponseContext';

function isOnlyOfficeConfig(value: unknown): value is PTemplateOnlyOfficeConfig {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof (value as PTemplateOnlyOfficeConfig).document === 'object' &&
    typeof (value as PTemplateOnlyOfficeConfig).editorConfig === 'object'
  );
}

export const usePTemplateOnlyOfficeHook = () => {
  const { setResponse } = useResponse();
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<PTemplateInterface | null>(null);
  const [config, setConfig] = useState<PTemplateOnlyOfficeConfig | null>(null);

  const openEditor = async (template: PTemplateInterface, mode: 'edit' | 'view' = 'edit') => {
    console.info('[PTemplateOnlyOfficeHook] openEditor acionado', {
      templateId: template.template_id,
      mode,
    });
    setIsLoading(true);
    setSelectedTemplate(template);
    try {
      const response = await PTemplateOpenEditorService(template.template_id, mode);
      if (isOnlyOfficeConfig(response)) {
        console.info('[PTemplateOnlyOfficeHook] configuração do editor recebida', {
          templateId: template.template_id,
          documentKey: response.document?.key,
          callbackEndpoint: response.editorConfig?.orius_api_endpoint,
        });
        setConfig(response);
        setIsEditorOpen(true);
        setResponse({
          status: 200,
          message: 'Editor carregado com sucesso',
        });
        return response;
      }

      setResponse({
        status: response.status,
        message: response.message,
        error: response.message,
      });
      console.error('[PTemplateOnlyOfficeHook] falha ao abrir editor', response);
      return response;
    } catch (error) {
      console.error('[PTemplateOnlyOfficeHook] exceção ao abrir editor', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const closeEditor = () => {
    setIsEditorOpen(false);
    setConfig(null);
    setSelectedTemplate(null);
  };

  return {
    isEditorOpen,
    isLoading,
    selectedTemplate,
    config,
    openEditor,
    closeEditor,
    setIsEditorOpen,
  };
};

