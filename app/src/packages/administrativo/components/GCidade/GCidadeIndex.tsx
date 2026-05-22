'use client';

import { useCallback, useEffect, useState } from 'react';

import { Card, CardContent } from '@/components/ui/card';
import GCidadeForm from '@/packages/administrativo/components/GCidade/GCidadeForm';
import GCidadeTable from '@/packages/administrativo/components/GCidade/GCidadeTable';
import { useGCidadeReadHook } from '@/packages/administrativo/hooks/GCidade/useGCidadeReadHook';
import { useGCidadeRemoveHook } from '@/packages/administrativo/hooks/GCidade/useGCidadeRemoveHook';
import { useGCidadeSaveHook } from '@/packages/administrativo/hooks/GCidade/useGCidadeSaveHook';
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import ConfirmDialog from '@/shared/components/confirmDialog/ConfirmDialog';
import { useConfirmDialog } from '@/shared/components/confirmDialog/useConfirmDialog';
import Header from '@/shared/components/structure/Header';

export default function GCidadeIndex() {
  // Hooks para leitura e salvamento
  const { gCidade, fetchGCidade } = useGCidadeReadHook();
  const { saveGCidade } = useGCidadeSaveHook();
  const { removeGCidade } = useGCidadeRemoveHook();

  // Estados
  const [selectedCidade, setSelectedCidade] = useState<GCidadeInterface>();
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isActiveIndexCidadeSkeleton, setIsActiveIndexCidadeSkeleton] = useState(false);

  // Estado para saber qual item será deletado
  const [itemToDelete, setItemToDelete] = useState<GCidadeInterface>();

  /**
   * Hook do modal de confirmação
   */
  const {
    isOpen: isConfirmOpen,
    openDialog: openConfirmDialog,
    handleConfirm,
    handleCancel,
  } = useConfirmDialog();

  /**
   * Abre o formulário no modo de edição ou criação
   */
  const handleOpenForm = useCallback((data: GCidadeInterface) => {
    setSelectedCidade(data);
    setIsFormOpen(true);
  }, []);

  /**
   * Fecha o formulário e limpa o andamento selecionado
   */
  const handleCloseForm = useCallback(() => {
    setSelectedCidade({});
    setIsFormOpen(false);
  }, []);

  /**
   * Salva os dados do formulário
   */
  const handleSave = useCallback(
    async (formData: GCidadeInterface) => {
      // Aguarda salvar o registro
      await saveGCidade(formData);

      // Atualiza a lista de dados
      fetchGCidade({ uf: 'GO' });
    },
    [saveGCidade, fetchGCidade],
  );

  /**
   * Quando o usuário clica em "remover" na tabela
   */
  const handleConfirmDelete = useCallback(
    (item: GCidadeInterface) => {
      // Define o item atual para remoção
      setItemToDelete(item);

      // Abre o modal de confirmação
      openConfirmDialog();
    },
    [openConfirmDialog],
  );

  /**
   * Executa a exclusão de fato quando o usuário confirma
   */
  const handleDelete = useCallback(async () => {
    // Protege contra null
    if (!itemToDelete) return;

    // Executa o Hook de remoção
    await removeGCidade(itemToDelete);

    // Atualiza a lista
    await fetchGCidade({ uf: 'GO' });

    // Limpa o item selecionado
    setItemToDelete({});

    // Fecha o modal
    handleCancel();
  }, [itemToDelete, fetchGCidade, handleCancel]);

  const executeIndexGCidade = async () => {
    setIsActiveIndexCidadeSkeleton(true);
    await fetchGCidade({ uf: 'GO' });
    setIsActiveIndexCidadeSkeleton(false);
  };

  useEffect(() => {
    executeIndexGCidade();
  }, []);

  return (
    <div>
      {/* Cabeçalho */}
      <Header
        title={'Cidades'}
        description={'Gerenciamento de Cidades'}
        buttonText={'Nova Cidade'}
        buttonAction={() => {
          handleOpenForm({});
        }}
      />

      {/* Tabela de andamentos */}
      <Card>
        <CardContent>
          <GCidadeTable
            data={gCidade ?? []}
            isLoading={isActiveIndexCidadeSkeleton || !gCidade}
            onEdit={handleOpenForm}
            onDelete={handleConfirmDelete}
          />
        </CardContent>
      </Card>

      {/* Modal de confirmação */}
      <ConfirmDialog
        isOpen={isConfirmOpen}
        title="Confirmar exclusão"
        description="Atenção"
        message={`Deseja realmente excluir a cidade "${itemToDelete?.cidade_nome}"?`}
        confirmText="Sim, excluir"
        cancelText="Cancelar"
        onConfirm={handleDelete}
        onCancel={handleCancel}
      />

      {/* Formulário de criação/edição */}
      <GCidadeForm
        isOpen={isFormOpen}
        data={selectedCidade}
        onClose={handleCloseForm}
        onSave={handleSave}
      />
    </div>
  );
}
