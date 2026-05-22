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
import GUsuarioInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import GetCapitalize from '@/shared/actions/text/GetCapitalize';
import { SortableHeader } from '@/shared/components/dataTable/SortableHeader';
import { formatEmptyField } from '@/shared/utils/emptyField';

export default function GUsuarioColumns(
  onEdit: (item: GUsuarioInterface, isEditingFormStatus: boolean) => void,
  onDelete: (item: GUsuarioInterface, isEditingFormStatus: boolean) => void,
): ColumnDef<GUsuarioInterface>[] {
  return [
    // ID
    {
      accessorKey: 'usuario_id',
      header: ({ column }) => SortableHeader('ID', column),
      cell: ({ row }) => Number(row.getValue('usuario_id')),
      enableSorting: true,
      meta: { 
          headerClassName: 'w-[100px] text-center bg-muted', // Estilo só do Header
          cellClassName: 'w-[100px] text-center'    // Estilo só do Body
        }  
    },

    {
      accessorKey: 'cpf',
      header: ({ column }) => SortableHeader('CPF', column),
      cell: ({ row }) => GetCapitalize(formatEmptyField(row.getValue('cpf') as string | null | undefined)),
      meta: { 
          headerClassName: 'w-[100px]text-center bg-muted', // Estilo só do Header
          cellClassName: 'w-[100px] text-center'    // Estilo só do Body
        } 
    },      

    // Nome completo
    {
      accessorKey: 'nome_completo',
      header: ({ column }) => SortableHeader('Nome', column),
      cell: ({ row }) => GetCapitalize(formatEmptyField(row.getValue('nome_completo') as string | null | undefined)),
      filterFn: 'includesString',
      meta: { 
          headerClassName: 'text-center bg-muted', // Estilo só do Header
          cellClassName: 'text-left'    // Estilo só do Body
        } 
    },    

    {
      accessorKey: 'email',
      header: ({ column }) => SortableHeader('E-mail', column),
      cell: ({ row }) => GetCapitalize(formatEmptyField(row.getValue('email') as string | null | undefined)),
      meta: { 
          headerClassName: 'text-center bg-muted', // Estilo só do Header
          cellClassName: 'text-left'    // Estilo só do Body
        } 
    }, 
    
    {
      accessorKey: 'funcao',
      header: ({ column }) => SortableHeader('Função', column),
      cell: ({ row }) => GetCapitalize(formatEmptyField(row.getValue('funcao') as string | null | undefined)),
      meta: { 
          headerClassName: 'text-center bg-muted', // Estilo só do Header
          cellClassName: 'text-left'    // Estilo só do Body
        } 
    },      

    // Ações
    {
      id: 'actions',
      header: 'Ações',
      meta: { headerClassName: 'w-[100px] bg-muted' } ,
      cell: ({ row }) => {
        const natureza = row.original;

        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                className='cursor-pointer' 
                variant="ghost" 
                size="icon"
              >
                <EllipsisIcon />
              </Button>
            </DropdownMenuTrigger>

            <DropdownMenuContent side="left" align="start" className='cursor-pointer'>
              <DropdownMenuGroup>
                <DropdownMenuItem onSelect={() => onEdit(natureza, true)}>
                  <PencilIcon className="mr-2 h-4 w-4 cursor-pointer" />
                  Editar
                </DropdownMenuItem>

                <DropdownMenuSeparator />

                <DropdownMenuItem
                  className="text-red-600 cursor-pointer"
                  onSelect={() => onDelete(natureza, true)}
                >
                  <Trash2Icon className="mr-2 h-4 w-4" />
                  Remover
                </DropdownMenuItem>
              </DropdownMenuGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
      enableSorting: false,
      enableHiding: false,
    },
  ];
}
