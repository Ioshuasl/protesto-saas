export function parseFilenameFromContentDisposition(
  header: string | null | undefined,
): string | null {
  if (!header) return null;

  const utf8Match = /filename\*=UTF-8''([^;\s]+)/i.exec(header);
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1]);
    } catch {
      return utf8Match[1];
    }
  }

  const quotedMatch = /filename="([^"]+)"/i.exec(header);
  if (quotedMatch?.[1]) return quotedMatch[1];

  const plainMatch = /filename=([^;\s]+)/i.exec(header);
  return plainMatch?.[1]?.trim() || null;
}

export function triggerBrowserFileDownload(
  contentBase64: string,
  filename: string,
  mimeType = "text/plain;charset=iso-8859-1",
): void {
  const binary = atob(contentBase64);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }

  const blob = new Blob([bytes], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.rel = "noopener noreferrer";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
