/**
 * Ações estáticas para extração de extensão e nome a partir de path/URL.
 */
export class FilePathActions {
  static pathToExtension(path: string): string {
    const withoutQuery = path.split('?')[0] ?? '';
    const segments = withoutQuery.split(/[/\\]/);
    const last = segments[segments.length - 1] ?? '';
    const dot = last.lastIndexOf('.');
    if (dot === -1) return '';
    return last.slice(dot + 1).toLowerCase();
  }

  static pathToFileName(path: string): string {
    const withoutQuery = path.split('?')[0] ?? '';
    const segments = withoutQuery.split(/[/\\]/);
    return segments[segments.length - 1] ?? 'Arquivo';
  }

  static extensionToKind(ext: string): string {
    if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'].includes(ext)) return 'image';
    if (ext === 'pdf') return 'pdf';
    if (['xls', 'xlsx', 'ods', 'csv'].includes(ext)) return 'sheet';
    if (['ppt', 'pptx', 'odp'].includes(ext)) return 'slides';
    if (['zip', 'rar', '7z'].includes(ext)) return 'archive';
    return 'other';
  }
}
