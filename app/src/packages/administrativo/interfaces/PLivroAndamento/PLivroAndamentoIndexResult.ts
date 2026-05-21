import type { PLivroAndamentoInterface } from '@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PLivroAndamentoIndexResult = {
  rows: PLivroAndamentoInterface[];
  pagination: PaginationMeta;
};
