'use client';

import {
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  PaginationState,
  Row,
  RowSelectionState,
  SortingState,
  useReactTable,
  VisibilityState,
} from '@tanstack/react-table';
import { ChevronLeftIcon, ChevronRightIcon, EyeIcon } from 'lucide-react';
import React from 'react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

import LoadingButton from '../loadingButton/LoadingButton';
import DataTableInterface from './interfaces/DataTableInterface';

/**
 * DataTable genérico (sem suporte a subview).
 */
export function DataTable<TData>({
  data,
  columns,
  filterColumn,
  filterPlaceholder = 'Buscar...',
  onEdit,
  onDelete,
  onRowClick,
  loading = false,
  onLoadMore,
  isLoadingMore,
}: DataTableInterface<TData>) {
  const safeData = Array.isArray(data) ? data : [];

  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);
  const [columnVisibility, setColumnVisibility] = React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState<RowSelectionState>({});
  const [internalPagination, setInternalPagination] = React.useState<PaginationState>({
    pageIndex: 0,
    pageSize: 20,
  });

  const resolvedPagination: PaginationState = React.useMemo(
    () => ({
      pageIndex: internalPagination.pageIndex,
      pageSize: internalPagination.pageSize,
    }),
    [internalPagination],
  );

  const table = useReactTable({
    data: safeData,
    columns: [
      ...columns,
      ...(onEdit || onDelete
        ? [
          {
            id: 'actions',
            header: 'Ações',
            enableSorting: false,
            enableColumnFilter: false,
            enableHiding: false,
            cell: ({ row }: { row: Row<TData> }) => (
              <div className="flex gap-2 cursor-pointer">
                {onEdit && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onEdit(row.original)}
                  >
                    Editar
                  </Button>
                )}
                {onDelete && (
                  <Button
                    variant="destructive"
                    size="sm" onClick={() => onDelete(row.original)}
                  >
                    Excluir
                  </Button>
                )}
              </div>
            ),
          } as ColumnDef<TData, unknown>,
        ]
        : []),
    ],
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
      pagination: resolvedPagination,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    onPaginationChange: (updater) =>
      setInternalPagination((old) =>
        typeof updater === 'function'
          ? (updater as (old: PaginationState) => PaginationState)(old)
          : updater,
      ),
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    autoResetPageIndex: false,
  });

  const skeletonRows = Array.from({ length: 8 });

  return (
    <div className="flex h-full min-h-0 flex-col gap-4">
      {/* Filtros */}
      <div className="flex shrink-0 items-center gap-2">
        {filterColumn && (
          <Input
            placeholder={filterPlaceholder}
            value={(table.getColumn(filterColumn)?.getFilterValue() as string) ?? ''}
            onChange={(e) => table.getColumn(filterColumn)?.setFilterValue(e.target.value)}
            className="w-full"
          />
        )}

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto cursor-pointer">
              <EyeIcon className="mr-2 h-4 w-4" />
              Colunas visíveis
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((col) => col.getCanHide())
              .map((col) => (
                <DropdownMenuCheckboxItem
                  key={col.id}
                  checked={col.getIsVisible()}
                  onCheckedChange={(v) => col.toggleVisibility(!!v)}
                  className="cursor-pointer"
                >
                  {col.id}
                </DropdownMenuCheckboxItem>
              ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* Cabeçalho fixo */}
      <Table className="rounded-2xl border">
        <TableHeader className="bg-background sticky top-0 z-10">
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <TableHead
                  key={header.id}
                  className={(header.column.columnDef.meta as { headerClassName?: string })?.headerClassName}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>

        {/** Body da tabela */}
        <TableBody>
          {loading ? (
            skeletonRows.map((_, index) => (
              <TableRow key={index}>
                {table.getAllColumns().map((col) => (
                  <TableCell key={col.id}>
                    <Skeleton className="h-4 w-full" />
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                className={onRowClick ? 'hover:bg-muted/50 cursor-pointer' : ''}
                onClick={() => onRowClick?.(row.original)}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell
                    key={cell.id}
                    className={(cell.column.columnDef.meta as { cellClassName?: string })?.cellClassName}
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={table.getAllColumns().length} className="h-24 text-center">
                Não há registros disponíveis.
              </TableCell>
            </TableRow>
          )}
        </TableBody>


      </Table>

      {/* Paginação */}
      <div className="flex shrink-0 items-center justify-between gap-4">
        <span className="text-muted-foreground text-sm">
          Página {table.getState().pagination.pageIndex + 1} de {table.getPageCount()}
        </span>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.setPageIndex(0)}
            disabled={!table.getCanPreviousPage()}
            type="button"
          >
            Primeira
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            type="button"
          >
            <ChevronLeftIcon className="h-4 w-4" />
            Anterior
          </Button>
          {table.getCanNextPage() ? (
            <>
              <Button className='cursor-pointer' variant="outline" size="sm" onClick={() => table.nextPage()} type="button">
                Próxima
                <ChevronRightIcon className="h-4 w-4" />
              </Button>
              <Button
                className='cursor-pointer'
                variant="outline"
                size="sm"
                onClick={() => table.setPageIndex(table.getPageCount() - 1)}
                type="button"
              >
                Última
              </Button>
            </>
          ) : onLoadMore ? (
            <LoadingButton
              variant="outline"
              size="sm"
              type="button"
              text="Carregar mais"
              textLoading="Carregando..."
              loading={isLoadingMore}
              onClick={() => onLoadMore()}
            />
          ) : (
            <>
              <Button className='cursor-pointer' variant="outline" size="sm" disabled type="button">
                Próxima
                <ChevronRightIcon className="h-4 w-4" />
              </Button>
              <Button className='cursor-pointer' variant="outline" size="sm" disabled type="button">
                Última
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

