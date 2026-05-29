import { useCallback, useState } from "react";
import { toast } from "sonner";
import { triggerBrowserFileDownload } from "@/packages/cra/data/PTituloArquivo/pArquivoTituloDownloadUtils";
import type { PArquivoTituloDownloadResult } from "@/packages/cra/data/PTituloArquivo/PTituloArquivoDownloadData";
import { PTituloArquivoDownloadService } from "@/packages/cra/service/PTituloArquivo/PTituloArquivoDownloadService";

function isPArquivoTituloDownloadResult(
  value: unknown,
): value is PArquivoTituloDownloadResult {
  return (
    typeof value === "object" &&
    value !== null &&
    "success" in value &&
    typeof (value as PArquivoTituloDownloadResult).success === "boolean"
  );
}

export function usePArquivoTituloDownload() {
  const [downloadingId, setDownloadingId] = useState<number | null>(null);

  const downloadArquivo = useCallback(
    async (arquivoTituloId: number, nomeArquivo?: string) => {
      if (downloadingId != null) return;

      setDownloadingId(arquivoTituloId);
      try {
        const response = await PTituloArquivoDownloadService(
          arquivoTituloId,
          nomeArquivo?.trim() || undefined,
        );

        if (!isPArquivoTituloDownloadResult(response)) {
          toast.error("Falha ao baixar o arquivo", {
            description: (response as { message?: string })?.message,
          });
          return;
        }

        if (!response.success) {
          toast.error("Falha ao baixar o arquivo", { description: response.message });
          return;
        }

        triggerBrowserFileDownload(response.contentBase64, response.filename);
        toast.success("Download iniciado", { description: response.filename });
      } finally {
        setDownloadingId(null);
      }
    },
    [downloadingId],
  );

  const isDownloading = (arquivoTituloId: number) => downloadingId === arquivoTituloId;

  return { downloadArquivo, isDownloading, isDownloadingAny: downloadingId != null };
}
