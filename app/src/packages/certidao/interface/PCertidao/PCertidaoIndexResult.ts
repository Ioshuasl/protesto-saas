import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import type { PaginationMeta } from "@/shared/components/pagination";

export type PCertidaoIndexResult = {
  rows: PCertidaoInterface[];
  pagination: PaginationMeta;
};
