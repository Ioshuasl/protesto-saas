import type { POcorrenciaAndamentoInterface } from '@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoInterface';
import type { PaginationMeta } from '@/shared/components/pagination';

export type POcorrenciaAndamentoIndexResult = {
  rows: POcorrenciaAndamentoInterface[];
  pagination: PaginationMeta;
};
