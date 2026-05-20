import { useState } from "react";
import type {
  CraImportacaoSavePayload,
  CraImportacaoSaveResult,
} from "@/packages/cra/interface/CraImportacao/CraImportacaoSaveInterface";
import { isCraImportacaoSaveResult } from "@/packages/cra/interface/CraImportacao/CraImportacaoSaveInterface";
import { CraImportacaoSaveService } from "@/packages/cra/service/CraImportacao/CraImportacaoSaveService";
import { useResponse } from "@/shared/components/response/ResponseContext";

export const useCraImportacaoSaveHook = () => {
  const { setResponse } = useResponse();
  const [craImportacao, setCraImportacao] = useState<CraImportacaoSaveResult | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const saveCraImportacao = async (data: CraImportacaoSavePayload) => {
    setIsSaving(true);
    try {
      const response = await CraImportacaoSaveService(data);

      if (isCraImportacaoSaveResult(response)) {
        setCraImportacao(response);
      }

      setResponse(
        isCraImportacaoSaveResult(response)
          ? {
              status: 201,
              message: `${response.imported_count} título(s) importado(s) com sucesso`,
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

  return { craImportacao, isSaving, saveCraImportacao };
};
