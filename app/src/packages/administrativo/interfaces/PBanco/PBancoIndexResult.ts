import type { PBancoInterface } from '@/packages/administrativo/interfaces/PBanco/PBancoInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PBancoIndexResult = {
  rows: PBancoInterface[];
  pagination: PaginationMeta;
};
