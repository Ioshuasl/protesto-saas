'use client';

import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import { DataTable } from '@/shared/components/dataTable/DataTable';

import GCidadeColumns from './GCidadeColumns';

interface GCidadeTableProps {
  data: GCidadeInterface[];
  isLoading?: boolean;
  onEdit: (item: GCidadeInterface, isEditingFormStatus: boolean) => void;
  onDelete: (item: GCidadeInterface, isEditingFormStatus: boolean) => void;
  openModalOnRowClick?: boolean;
}

export default function GCidadeTable({
  data,
  isLoading = false,
  onEdit,
  onDelete,
  openModalOnRowClick = true,
}: GCidadeTableProps) {
  const columns = GCidadeColumns(onEdit, onDelete);

  return (
    <DataTable
      data={data}
      columns={columns}
      loading={isLoading}
      filterColumn="cidade_nome"
      filterPlaceholder="Buscar por cidade..."
      openModalOnRowClick={openModalOnRowClick}
      onEdit={(item) => onEdit(item, true)}
    />
  );
}
