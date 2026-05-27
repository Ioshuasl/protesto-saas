import type { GSistemaInterface } from '@/packages/administrativo/interfaces/GSistema/GSistemaInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type GSistemaIndexResult = {
  rows: GSistemaInterface[];
  pagination: PaginationMeta;
};
