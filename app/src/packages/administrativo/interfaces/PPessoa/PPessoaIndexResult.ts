import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PPessoaIndexResult = {
  rows: PPessoaInterface[];
  pagination: PaginationMeta;
};
