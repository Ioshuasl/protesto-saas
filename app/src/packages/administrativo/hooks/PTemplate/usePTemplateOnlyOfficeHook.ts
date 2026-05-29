import { useState } from 'react';

import { PTemplateOpenEditorService } from '@/packages/administrativo/services/PTemplate/PTemplateOpenEditorService';
import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import type { PTemplateMarkerLegend } from '@/packages/administrativo/interfaces/PTemplate/PTemplateMarkerLegend';
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
  const [markerLegend, setMarkerLegend] = useState<PTemplateMarkerLegend | null>(null);

  const openEditor = async (template: PTemplateInterface, mode: 'edit' | 'view' = 'edit') => {
    console.info('[PTemplateOnlyOfficeHook] openEditor acionado', {
      templateId: template.template_id,
      mode,
    });
    setIsLoading(true);
    setSelectedTemplate(template);
    try {
      const response = await PTemplateOpenEditorService(template.template_id, mode);
      if (response && isOnlyOfficeConfig(response.config)) {
        console.info('[PTemplateOnlyOfficeHook] configuração do editor recebida', {
          templateId: template.template_id,
          documentKey: response.config.document?.key,
          callbackEndpoint: response.config.editorConfig?.orius_api_endpoint,
        });
        setConfig(response.config);
        setMarkerLegend(response.markerLegend ?? null);
        setIsEditorOpen(true);
        setResponse({
          status: 200,
          message: 'Editor carregado com sucesso',
        });
        return response.config;
      }

      setResponse({
        status: (response as { status?: number })?.status,
        message: (response as { message?: string })?.message,
        error: (response as { message?: string })?.message,
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
    setMarkerLegend(null);
    setSelectedTemplate(null);
  };

  return {
    isEditorOpen,
    isLoading,
    selectedTemplate,
    config,
    markerLegend,
    openEditor,
    closeEditor,
    setIsEditorOpen,
  };
};

