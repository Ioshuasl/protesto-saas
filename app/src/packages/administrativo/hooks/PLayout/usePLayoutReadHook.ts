import { useCallback, useState } from "react";

import type { PLayoutInterface } from "@/packages/administrativo/interfaces/PLayout/PLayoutInterface";
import { PLayoutIndexService } from "@/packages/administrativo/services/PLayout/PLayoutIndexService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePLayoutReadHook = () => {
  const { setResponse } = useResponse();
  const [layouts, setLayouts] = useState<PLayoutInterface[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchLayouts = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await PLayoutIndexService();
      if (Array.isArray(response)) {
        setLayouts(response);
        setResponse({
          status: 200,
          message: "Layouts listados com sucesso",
        });
      } else {
        setLayouts([]);
        setResponse({
          status: response.status,
          message: response.message,
          error: response.message,
        });
      }
      return response;
    } finally {
      setIsLoading(false);
    }
  }, [setResponse]);

  return { layouts, setLayouts, isLoading, fetchLayouts };
};
