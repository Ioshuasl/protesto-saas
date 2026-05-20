import { useState } from "react";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import {
  isPCertidaoSaveResult,
  type PCertidaoSavePayload,
} from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import { PCertidaoSaveService } from "@/packages/certidao/service/PCertidao/PCertidaoSaveService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const usePCertidaoSaveHook = () => {
  const { setResponse } = useResponse();
  const [pCertidao, setPCertidao] = useState<PCertidaoInterface | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const saveCertidao = async (data: PCertidaoSavePayload) => {
    setIsSaving(true);
    try {
      const response = await PCertidaoSaveService(data);

      if (isPCertidaoSaveResult(response)) {
        setPCertidao(response);
      }

      setResponse(
        isPCertidaoSaveResult(response)
          ? {
              status: data.certidao_id ? 200 : 201,
              message: data.certidao_id ? "Certidão atualizada com sucesso" : "Certidão criada com sucesso",
            }
          : {
              status: (response as { status?: number }).status,
              message: (response as { message?: string }).message,
              error: (response as { message?: string }).message,
            },
      );

      return response;
    } finally {
      setIsSaving(false);
    }
  };

  return { pCertidao, isSaving, saveCertidao };
};
