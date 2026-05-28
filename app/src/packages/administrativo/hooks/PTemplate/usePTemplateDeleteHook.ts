import { useState } from 'react';

import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import { PTemplateDeleteData } from '@/packages/administrativo/data/PTemplate/PTemplateDeleteData';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const usePTemplateDeleteHook = () => {
  const { setResponse } = useResponse();

  const [pTemplate, setPTemplate] = useState<PTemplateInterface>();

  const deleteTemplate = async (id: number) => {
    const response = await PTemplateDeleteData(id);

    setPTemplate({ template_id: id, descricao: '' } as PTemplateInterface);

    setResponse(response);
    return response;
  };

  return { pTemplate, deleteTemplate };
};
