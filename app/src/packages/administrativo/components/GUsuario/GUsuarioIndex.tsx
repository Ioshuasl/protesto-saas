'use client';

import { useCallback, useEffect, useState } from 'react';

import { useGUsuarioDeleteHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioDeleteHook';
import { useGUsuarioIndexHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioIndexHook';
import { useGUsuarioSaveHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioSaveHook';
import GUsuarioInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioInterface';
import ConfirmDialog from '@/shared/components/confirmDialog/ConfirmDialog';
import { useConfirmDialog } from '@/shared/components/confirmDialog/useConfirmDialog';
import Loading from '@/shared/components/loading/loading';
import Header from '@/shared/components/structure/Header';

import GUsuarioForm from './GUsuarioForm';
import GUsuarioTable from './GUsuarioTable';
import { nullable } from 'zod';

export default function GUsuarioIndex() {
  // Controle de estado do botão
  const [buttonIsLoading, setButtonIsLoading] = useState(false);

  // Hooks para leitura e salvamento
  const { GUsuario, indexGUsuario } = useGUsuarioIndexHook();
  const { saveGUsuario } = useGUsuarioSaveHook();
  const { deleteGUsuario } = useGUsuarioDeleteHook();

  // Estados
  const [selectedData, setSelectedData] = useState<GUsuarioInterface | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);

  // Estado para saber qual item será deletado
  const [itemToDelete, setItemToDelete] = useState<GUsuarioInterface | null>(null);

  /**
   * Hook do modal de confirmação
   */
  const { isOpen: isConfirmOpen, openDialog: openConfirmDialog, handleCancel } = useConfirmDialog();

  /**
   * Abre o formulário no modo de edição ou criação
   */
  const handleOpenForm = useCallback((data: GUsuarioInterface | null) => {
    setSelectedData(data);
    setIsFormOpen(true);
  }, []);

  /**
   * Fecha o formulário e limpa o andamento selecionado
   */
  const handleCloseForm = useCallback(() => {
    setSelectedData(null);
    setIsFormOpen(false);
  }, []);

  /**
   * Salva os dados do formulário
   */
  const handleSave = useCallback(
    async (formData: GUsuarioInterface) => {
      // Coloca o botão em estado de loading
      setButtonIsLoading(true);

      // Aguarda salvar o registro
      await saveGUsuario(formData);

      // Remove o botão em estado de loading
      setButtonIsLoading(false);

      // Atualiza a lista apenas quando for NOVO registro
      if (!formData.usuario_id) {
        indexGUsuario({});
      }
    },
    [saveGUsuario, indexGUsuario, handleCloseForm],
  );

  /**
   * Quando o usuário clica em "remover" na tabela
   */
  const handleConfirmDelete = useCallback(
    (item: GUsuarioInterface) => {
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
    await deleteGUsuario(itemToDelete);

    // Atualiza a lista
    await indexGUsuario({});

    // Limpa o item selecionado
    setItemToDelete(null);

    // Fecha o modal
    handleCancel();
  }, [itemToDelete, indexGUsuario, handleCancel]);

  /**
   * Busca inicial dos dados
   */
  useEffect(() => {
    indexGUsuario({});
  }, []);

  /**
   * Tela de loading enquanto carrega os dados
   */
  if (GUsuario?.length == 0) {
    return <Loading type={2} />;
  }

    return (
    <div>
      {/* Cabeçalho */}
      <Header
        title={'Usuários'}
        description={'Gerenciamento de Usuários'}
        buttonText={'Novo usuário'}
        buttonAction={() => {
          handleOpenForm(null);
        }}
      />

      {/* Tabela de andamentos */}
      <GUsuarioTable 
        data={GUsuario || undefined} 
        onEdit={handleOpenForm} 
        onDelete={handleConfirmDelete} 
      />


      {/* Modal de confirmação */}
      {isConfirmOpen && (
        <ConfirmDialog
          isOpen={isConfirmOpen}
          title="Confirmar exclusão"
          description="Atenção"
          message={`Deseja realmente excluir o valor "${itemToDelete?.nome_completo}"?`}
          confirmText="Sim, excluir"
          cancelText="Cancelar"
          onConfirm={handleDelete}
          onCancel={handleCancel}
        />
      )}
      {/* Formulário de criação/edição */}
      {isFormOpen && (
        <GUsuarioForm
          isOpen={isFormOpen}
          data={selectedData}
          onClose={handleCloseForm}
          onSave={handleSave}
          buttonIsLoading={buttonIsLoading}
        />
      )}
    </div>
  );
}
