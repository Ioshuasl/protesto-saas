import type { PAndamentoInterface } from '@/packages/administrativo/interfaces/PAndamento/PAndamentoInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PAndamentoIndexResult = {
  rows: PAndamentoInterface[];
  pagination: PaginationMeta;
};
