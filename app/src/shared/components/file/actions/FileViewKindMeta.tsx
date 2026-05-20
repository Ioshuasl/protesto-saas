import {
  FileArchive,
  FileImage,
  FileSpreadsheet,
  FileText,
} from 'lucide-react';
import { type ElementType } from 'react';

const META: Record<string, { label: string; icon: ElementType }> = {
  image: { label: 'Imagem', icon: FileImage },
  pdf: { label: 'PDF', icon: FileText },
  sheet: { label: 'Planilha', icon: FileSpreadsheet },
  slides: { label: 'Apresentação', icon: FileText },
  archive: { label: 'Arquivo', icon: FileArchive },
  other: { label: 'Arquivo', icon: FileText },
};

/**
 * Metadados de tipo de arquivo para o viewer (label + ícone).
 */
export class FileViewKindMeta {
  static getMeta(kind: string): { label: string; icon: ElementType } {
    return META[kind] ?? META.other;
  }
}
