/**
 * Força o download do arquivo em vez de abrir em nova guia.
 * Usa fetch + blob + object URL para que o atributo download seja respeitado
 * (em URLs cross-origin o navegador ignora download no <a> e abre a guia).
 */
export class FileDownloadActions {
  static async forceDownload(filePath: string, fileName?: string): Promise<void> {
    const name = fileName || 'arquivo';

    try {
      const res = await fetch(filePath, { mode: 'cors', credentials: 'same-origin' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = name;
      link.rel = 'noopener,noreferrer';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch {
      const link = document.createElement('a');
      link.href = filePath;
      link.download = name;
      link.rel = 'noopener,noreferrer';
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
}
