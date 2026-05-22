import type { TituloListItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloListItem';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PTituloIndexResult = {
  rows: TituloListItem[];
  pagination: PaginationMeta;
};
