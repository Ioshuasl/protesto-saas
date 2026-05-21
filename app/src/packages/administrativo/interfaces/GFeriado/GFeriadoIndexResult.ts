import type { GFeriadoInterface } from '@/packages/administrativo/interfaces/GFeriado/GFeriadoInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type GFeriadoIndexResult = {
  rows: GFeriadoInterface[];
  pagination: PaginationMeta;
};
