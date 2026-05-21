export type PaginationMeta = {
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
};

export const DEFAULT_PAGINATION_META: PaginationMeta = {
  page: 1,
  per_page: 20,
  total: 0,
  total_pages: 0,
};

export function normalizePaginationMeta(
  value: Partial<PaginationMeta> | null | undefined,
  fallbackPerPage = DEFAULT_PAGINATION_META.per_page,
): PaginationMeta {
  const page = Number(value?.page) > 0 ? Number(value?.page) : 1;
  const per_page = Number(value?.per_page) > 0 ? Number(value?.per_page) : fallbackPerPage;
  const total = Number(value?.total) >= 0 ? Number(value?.total) : 0;
  const total_pages =
    Number(value?.total_pages) >= 0
      ? Number(value?.total_pages)
      : per_page > 0
        ? Math.ceil(total / per_page)
        : 0;

  return { page, per_page, total, total_pages };
}
