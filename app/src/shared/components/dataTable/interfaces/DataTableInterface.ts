import { ColumnDef } from '@tanstack/react-table';

// Tipagem genérica
export default interface DataTableInterface<TData> {
  data?: TData[] | null;
  columns: ColumnDef<TData, any>[];
  filterColumn?: string;
  filterPlaceholder?: string;
  loading?: boolean;
  onEdit?: (item: TData) => void;
  onDelete?: (item: TData) => void;
  onRowClick?: (item: TData) => void;
  onLoadMore?: () => void;
  isLoadingMore?: boolean;
}
