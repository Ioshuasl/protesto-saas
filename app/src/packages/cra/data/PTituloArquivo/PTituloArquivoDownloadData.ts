"use server";

import { PARQUIVO_TITULO_ENDPOINTS } from "@/packages/cra/data/PTituloArquivo/pTituloArquivoDataConfig";
import { parseFilenameFromContentDisposition } from "@/packages/cra/data/PTituloArquivo/pArquivoTituloDownloadUtils";
import TokenGet from "@/shared/actions/token/TokenGet";

export type PArquivoTituloDownloadResult =
  | {
      success: true;
      filename: string;
      contentBase64: string;
    }
  | {
      success: false;
      message: string;
      status?: number;
    };

function buildDownloadUrl(arquivoTituloId: number): string {
  const primaryUrl =
    process.env.NEXT_PUBLIC_ORIUS_APP_API_URL ||
    process.env.NEXT_PUBLIC_ORIUS_APP_API_SECONDARY_URL ||
    "http://localhost:8000";
  const prefix = `${process.env.NEXT_PUBLIC_ORIUS_APP_API_PREFIX || "api/v1"}/`;
  const base = primaryUrl.endsWith("/") ? primaryUrl : `${primaryUrl}/`;
  return `${base}${prefix}${PARQUIVO_TITULO_ENDPOINTS.download(arquivoTituloId)}`;
}

export async function PTituloArquivoDownloadData(
  arquivoTituloId: number,
  fallbackFilename?: string,
): Promise<PArquivoTituloDownloadResult> {
  const token = await TokenGet();
  const url = buildDownloadUrl(arquivoTituloId);

  const response = await fetch(url, {
    method: "GET",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: "no-store",
  });

  if (!response.ok) {
    let message = "Não foi possível baixar o arquivo.";
    try {
      const json = (await response.json()) as { message?: string; detail?: string };
      message = json.message ?? json.detail ?? message;
    } catch {
      // resposta não é JSON (ex.: HTML de proxy)
    }
    return { success: false, message, status: response.status };
  }

  const buffer = await response.arrayBuffer();
  const filename =
    parseFilenameFromContentDisposition(response.headers.get("Content-Disposition")) ??
    fallbackFilename?.trim() ??
    `arquivo_titulo_${arquivoTituloId}.rem`;

  return {
    success: true,
    filename,
    contentBase64: Buffer.from(buffer).toString("base64"),
  };
}
