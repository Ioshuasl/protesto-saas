import type { PEspecieInterface } from '@/packages/administrativo/interfaces/PEspecie/PEspecieInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PEspecieIndexResult = {
  rows: PEspecieInterface[];
  pagination: PaginationMeta;
};
