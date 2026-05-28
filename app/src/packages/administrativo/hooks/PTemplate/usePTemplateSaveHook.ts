import { useState } from 'react';

import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { PTemplateSaveCreateService } from '@/packages/administrativo/services/PTemplate/PTemplateSaveCreateService';
import { PTemplateSaveUpdateService } from '@/packages/administrativo/services/PTemplate/PTemplateSaveUpdateService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTemplateSaveHook = () => {
  const { setResponse } = useResponse();
  const [pTemplate, setPTemplate] = useState<PTemplateInterface | null>(null);

  const saveTemplate = async (
    data: Omit<PTemplateInterface, 'template_id'>,
    selected: PTemplateInterface | null,
  ) => {
    const response = selected
      ? await PTemplateSaveUpdateService(selected.template_id, data)
      : await PTemplateSaveCreateService(data);

    if (response && typeof response === 'object' && 'template_id' in response) {
      setPTemplate(response as PTemplateInterface);
    }

    setResponse(
      response && typeof response === 'object' && 'template_id' in response
        ? {
            status: selected ? 200 : 201,
            message: selected ? 'Template atualizado com sucesso' : 'Template criado com sucesso',
          }
        : {
            status: (response as { status?: number }).status,
            message: (response as { message?: string }).message,
            error: (response as { message?: string }).message,
          },
    );

    return response;
  };

  return { pTemplate, saveTemplate };
};
