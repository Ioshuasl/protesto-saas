import { useState } from 'react';

import type { GEmolumentoInterface } from '@/packages/administrativo/interfaces/GEmolumento/GEmolumentoInterface';
import { GEmolumentoDeleteService } from '@/packages/administrativo/services/GEmolumento/GEmolumentoDeleteService';
import { useResponse } from '@/shared/components/response/ResponseContext';

export const useGEmolumentoDeleteHook = () => {
  const { setResponse } = useResponse();

  const [gEmolumento, setGEmolumento] = useState<GEmolumentoInterface>();

  const deleteEmolumento = async (id: number) => {
    const response = await GEmolumentoDeleteService({ emolumento_id: id } as GEmolumentoInterface);

    setGEmolumento({ emolumento_id: id } as GEmolumentoInterface);

    setResponse(response);
    return response;
  };

  return { gEmolumento, deleteEmolumento };
};
