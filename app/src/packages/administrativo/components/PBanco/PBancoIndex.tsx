"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PBancoDialog } from "@/packages/administrativo/components/PBanco/PBancoDialog";
import { PBancoFilter } from "@/packages/administrativo/components/PBanco/PBancoFilter";
import type { BancoFormValues } from "@/packages/administrativo/schemas/PBanco/PBancoFormSchema";
import { PBancoTable } from "@/packages/administrativo/components/PBanco/PBancoTable";
import { usePBancoDeleteHook } from "@/packages/administrativo/hooks/PBanco/usePBancoDeleteHook";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import { usePBancoSaveHook } from "@/packages/administrativo/hooks/PBanco/usePBancoSaveHook";
import type { PBancoInterface } from "@/packages/administrativo/interfaces/PBanco/PBancoInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

export default function PBancoIndex() {
  const { bancos, isLoading, fetchBancos } = usePBancoReadHook();
  const { saveBanco } = usePBancoSaveHook();
  const { deleteBanco } = usePBancoDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selected, setSelected] = useState<PBancoInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);

  const handleOpenDialog = useCallback((row?: PBancoInterface) => {
    setSelected(row ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelected(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: BancoFormValues) => {
      setButtonIsLoading(true);
      try {
        await saveBanco(formData, selected);
        await fetchBancos();
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar banco:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [saveBanco, selected, fetchBancos, handleCloseDialog],
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
      await deleteBanco(id);
      await fetchBancos();
    } catch (e) {
      console.error("Erro ao excluir banco:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deleteBanco, fetchBancos]);

  useEffect(() => {
    void fetchBancos();
  }, [fetchBancos]);

  const filtered = useMemo(() => {
    if (!searchQuery) return bancos;
    const q = searchQuery.toLowerCase();
    return bancos.filter(
      (b) => b.descricao?.toLowerCase().includes(q) || b.codigo_banco?.toLowerCase().includes(q),
    );
  }, [bancos, searchQuery]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Bancos</h1>
          <Button onClick={() => handleOpenDialog()} className="bg-[#FF6B00] hover:bg-[#E56000] text-white">
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Novo Banco
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PBancoFilter value={searchQuery} onChange={setSearchQuery} />
        <PBancoTable data={filtered} isLoading={isLoading} onEdit={handleOpenDialog} onDelete={openDeleteDialog} />
      </div>

      <PBancoDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        banco={selected}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Banco"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir este banco?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
