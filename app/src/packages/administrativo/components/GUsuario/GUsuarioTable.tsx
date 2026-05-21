'use client';

import GUsuarioTableInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioTableInterface';
import { DataTable } from '@/shared/components/dataTable/DataTable';

import GUsuarioColumns from './GUsuarioColumns';

/**
 * Componente principal da tabela de Naturezas
 */
export default function GUsuarioTable({
  data,
  onEdit,
  onDelete,
  openModalOnRowClick = true,
}: GUsuarioTableInterface) {
  const columns = GUsuarioColumns(onEdit, onDelete);
  return (
    <div>
      <DataTable
        data={data ?? []}
        columns={columns}
        loading={!data}
        filterColumn="nome_completo"
        filterPlaceholder="Busca por nome de usuário..."
        openModalOnRowClick={openModalOnRowClick}
        onEdit={(item) => onEdit(item, true)}
      />
    </div>
  );
}
