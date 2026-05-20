"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PLivroAndamentoDialog } from "@/packages/administrativo/components/PLivroAndamento/PLivroAndamentoDialog";
import { PLivroAndamentoFilter } from "@/packages/administrativo/components/PLivroAndamento/PLivroAndamentoFilter";
import type { LivroAndamentoFormValues } from "@/packages/administrativo/schemas/PLivroAndamento/PLivroAndamentoFormSchema";
import { PLivroAndamentoTable } from "@/packages/administrativo/components/PLivroAndamento/PLivroAndamentoTable";
import { usePLivroAndamentoDeleteHook } from "@/packages/administrativo/hooks/PLivroAndamento/usePLivroAndamentoDeleteHook";
import { usePLivroAndamentoReadHook } from "@/packages/administrativo/hooks/PLivroAndamento/usePLivroAndamentoReadHook";
import { usePLivroAndamentoSaveHook } from "@/packages/administrativo/hooks/PLivroAndamento/usePLivroAndamentoSaveHook";
import { usePLivroNaturezaReadHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaReadHook";
import type { PLivroAndamentoInterface } from "@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function PLivroAndamentoIndex() {
  const { livrosAndamento, isLoading: isLoadingLivros, fetchLivrosAndamento } = usePLivroAndamentoReadHook();
  const { naturezas, isLoading: isLoadingNaturezas, fetchNaturezas } = usePLivroNaturezaReadHook();
  const { saveLivroAndamento } = usePLivroAndamentoSaveHook();
  const { deleteLivroAndamento } = usePLivroAndamentoDeleteHook();

  const isLoading = isLoadingLivros || isLoadingNaturezas;

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PLivroAndamentoInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const fetchData = useCallback(async () => {
    await Promise.all([fetchLivrosAndamento(), fetchNaturezas()]);
  }, [fetchLivrosAndamento, fetchNaturezas]);

  useEffect(() => {
    void fetchData();
  }, [fetchData]);

  const filtered = useMemo(() => {
    if (!searchQuery) return livrosAndamento;
    const q = searchQuery.toLowerCase();
    return livrosAndamento.filter(
      (l) => l.numero_livro?.toString().includes(q) || l.sigla?.toLowerCase().includes(q),
    );
  }, [livrosAndamento, searchQuery]);

  const handleOpenDialog = useCallback((row?: PLivroAndamentoInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: LivroAndamentoFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveLivroAndamento(formData, selected);
        await fetchData();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar livro em andamento:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveLivroAndamento, selected, fetchData, handleCloseDialog],
  );

  const openDeleteDialog = useCallback((id: number) => {
    setPendingDeleteId(id);
    setDeleteDialogOpen(true);
  }, []);

  const closeDeleteDialog = useCallback(() => {
    setDeleteDialogOpen(false);
    setPendingDeleteId(null);
  }, []);

  const confirmDelete = useCallback(async () => {
    const id = pendingDeleteId;
    if (id == null) return;
    closeDeleteDialog();
    try {
      await deleteLivroAndamento(id);
      await fetchData();
    } catch (e) {
      console.error("Erro ao excluir:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteLivroAndamento, fetchData]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Livro Andamento</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" />
            Novo Livro Andamento
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PLivroAndamentoFilter value={searchQuery} onChange={setSearchQuery} />
        <PLivroAndamentoTable
          data={filtered}
          naturezas={naturezas}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />
      </div>

      <PLivroAndamentoDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        livroAndamento={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Livro em andamento"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir este livro em andamento?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
