import type { PaginationMeta } from "@/shared/components/pagination";
import type { PArquivoTituloInterface } from "./PArquivoTituloInterface";

export type PArquivoTituloIndexQuery = {
  page?: number;
  per_page?: number;
  sort?: string;
  include?: string;
  portador_codigo?: string;
  data_inicio?: string;
  data_fim?: string;
};

export type PArquivoTituloIndexResult = {
  rows: PArquivoTituloInterface[];
  pagination: PaginationMeta;
};
