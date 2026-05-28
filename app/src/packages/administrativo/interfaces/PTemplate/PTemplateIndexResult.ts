import type { PTemplateInterface } from '@/packages/administrativo/interfaces/PTemplate/PTemplateInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type PTemplateIndexResult = {
  rows: PTemplateInterface[];
  pagination: PaginationMeta;
};
