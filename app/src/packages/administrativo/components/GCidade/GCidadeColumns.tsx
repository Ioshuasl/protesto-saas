'use client';

import { ColumnDef } from '@tanstack/react-table';
import { EllipsisIcon, PencilIcon, Trash2Icon } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import { SortableHeader } from '@/shared/components/dataTable/SortableHeader';
import { formatEmptyField } from '@/shared/utils/emptyField';

export default function GCidadeColumns(
  onEdit: (item: GCidadeInterface, isEditingFormStatus: boolean) => void,
  onDelete: (item: GCidadeInterface, isEditingFormStatus: boolean) => void,
): ColumnDef<GCidadeInterface>[] {
  return [
    {
      accessorKey: 'cidade_id',
      header: ({ column }) => SortableHeader('#', column),
      cell: ({ row }) => Number(row.getValue('cidade_id')),
      enableSorting: true,
      meta: {
        headerClassName: 'w-[60px] text-center bg-muted',
        cellClassName: 'w-[60px] text-center',
      },
    },
    {
      accessorKey: 'codigo_ibge',
      header: ({ column }) => SortableHeader('IBGE', column),
      cell: ({ row }) => formatEmptyField(row.getValue('codigo_ibge') as string | number | null | undefined),
      meta: {
        headerClassName: 'w-[100px] text-center bg-muted',
        cellClassName: 'w-[100px] text-center',
      },
    },
    {
      accessorKey: 'uf',
      header: ({ column }) => SortableHeader('UF', column),
      cell: ({ row }) => formatEmptyField(row.getValue('uf') as string | null | undefined),
      meta: {
        headerClassName: 'w-[70px] text-center bg-muted',
        cellClassName: 'w-[70px] text-center',
      },
    },
    {
      accessorKey: 'cidade_nome',
      header: ({ column }) => SortableHeader('Descrição', column),
      cell: ({ row }) => (
        <div className="font-semibold">{formatEmptyField(row.getValue('cidade_nome') as string | null | undefined)}</div>
      ),
      meta: {
        headerClassName: 'text-center bg-muted',
        cellClassName: '',
      },
    },
    {
      id: 'actions',
      header: () => <div className="flex w-full items-center justify-center">Ações</div>,
      cell: ({ row }) => {
        const item = row.original;
        return (
          <div className="flex w-full items-center justify-center">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="cursor-pointer shrink-0">
                  <EllipsisIcon />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent side="left" align="start">
                <DropdownMenuGroup>
                  <DropdownMenuItem className="cursor-pointer" onSelect={() => onEdit(item, true)}>
                    <PencilIcon className="mr-2 h-4 w-4" />
                    Editar
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="cursor-pointer" onSelect={() => onDelete(item, true)}>
                    <Trash2Icon className="mr-2 h-4 w-4" />
                    Remover
                  </DropdownMenuItem>
                </DropdownMenuGroup>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        );
      },
      enableSorting: false,
      enableHiding: false,
      meta: {
        headerClassName: 'w-[90px] text-center bg-muted',
        cellClassName: 'w-[90px] text-center',
      },
    },
  ];
}
