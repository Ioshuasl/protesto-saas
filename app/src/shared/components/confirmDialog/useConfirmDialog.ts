// Importa os hooks useCallback e useState do React
import { useCallback, useState } from 'react';

// Define a interface para opções do hook
// Permite que o usuário passe callbacks opcionais para confirmação e cancelamento
interface UseConfirmDialogOptions {
  onConfirm?: () => void; // Função chamada quando o usuário confirma a ação
  onCancel?: () => void; // Função chamada quando o usuário cancela a ação
}

// Declara o hook customizado useConfirmDialog
// Recebe um objeto de opções que contém os callbacks onConfirm e onCancel
export function useConfirmDialog({ onConfirm, onCancel }: UseConfirmDialogOptions = {}) {
  // Estado interno que controla se o diálogo de confirmação está aberto
  const [isOpen, setIsOpen] = useState(false);

  // Função para abrir o diálogo
  // useCallback memoriza a função para que não seja recriada em cada renderização
  const openDialog = useCallback(() => setIsOpen(true), []);

  // Função para fechar o diálogo
  const closeDialog = useCallback(() => setIsOpen(false), []);

  // Função chamada quando o usuário confirma a ação
  // Executa o callback onConfirm, se fornecido, e fecha o diálogo
  const handleConfirm = useCallback(() => {
    onConfirm?.(); // Chama onConfirm somente se ele existir
    closeDialog(); // Fecha o diálogo após a confirmação
  }, [onConfirm, closeDialog]);

  // Função chamada quando o usuário cancela a ação
  // Executa o callback onCancel, se fornecido, e fecha o diálogo
  const handleCancel = useCallback(() => {
    onCancel?.(); // Chama onCancel somente se ele existir
    closeDialog(); // Fecha o diálogo após o cancelamento
  }, [onCancel, closeDialog]);

  // Retorna os valores e funções que serão usados pelo componente
  // isOpen -> estado do modal
  // openDialog -> função para abrir o modal
  // closeDialog -> função para fechar o modal
  // handleConfirm -> função para confirmar a ação
  // handleCancel -> função para cancelar a ação
  return {
    isOpen,
    openDialog,
    closeDialog,
    handleConfirm,
    handleCancel,
  };
}
