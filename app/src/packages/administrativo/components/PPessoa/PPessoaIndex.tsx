"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PPessoaDialog } from "@/packages/administrativo/components/PPessoa/PPessoaDialog";
import { PPessoaFilter } from "@/packages/administrativo/components/PPessoa/PPessoaFilter";
import {
  buildPPessoaIndexQuery,
  defaultPPessoaFilterState,
  type PPessoaFilterState,
} from "@/packages/administrativo/components/PPessoa/ppessoaFilterUtils";
import type { PessoaFormValues } from "@/packages/administrativo/schemas/PPessoa/PPessoaFormSchema";
import { PPessoaTable } from "@/packages/administrativo/components/PPessoa/PPessoaTable";
import { usePPessoaDeleteHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaDeleteHook";
import { usePPessoaReadHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaReadHook";
import { usePPessoaSaveHook } from "@/packages/administrativo/hooks/PPessoa/usePPessoaSaveHook";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";

const PPESSOA_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

/** Tela de cadastro: listagem via API com formato3 e filtros nome/cpfcnpj/telefone. */
export default function PPessoaIndex() {
  const { pessoas, pagination, isLoading, fetchPessoas } = usePPessoaReadHook();
  const { savePessoa } = usePPessoaSaveHook();
  const { deletePessoa } = usePPessoaDeleteHook();

  const [buttonIsLoading, setButtonIsLoading] = useState(false);
  const [filters, setFilters] = useState<PPessoaFilterState>(defaultPPessoaFilterState);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedPessoa, setSelectedPessoa] = useState<PPessoaInterface | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState<number | null>(null);
  const [page, setPage] = useState(1);
  const [debouncedFilters, setDebouncedFilters] = useState<PPessoaFilterState>(filters);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedFilters(filters), 400);
    return () => window.clearTimeout(timer);
  }, [filters]);

  useEffect(() => {
    setPage(1);
  }, [debouncedFilters.search, debouncedFilters.tipo_pessoa]);

  const apiFilters = useMemo(
    () => buildPPessoaIndexQuery(debouncedFilters),
    [debouncedFilters],
  );

  const indexQuery = useMemo(
    () => ({
      ...apiFilters,
      page,
      per_page: PPESSOA_PER_PAGE,
    }),
    [apiFilters, page],
  );

  const handleFiltersChange = useCallback((next: PPessoaFilterState) => {
    setFilters(next);
  }, []);

  const handleOpenDialog = useCallback((pessoa?: PPessoaInterface) => {
    setSelectedPessoa(pessoa ?? null);
    setIsDialogOpen(true);
  }, []);

  const handleCloseDialog = useCallback(() => {
    setSelectedPessoa(null);
    setIsDialogOpen(false);
  }, []);

  const handleSave = useCallback(
    async (formData: PessoaFormValues) => {
      setButtonIsLoading(true);
      try {
        await savePessoa(formData, selectedPessoa);
        await fetchPessoas(indexQuery);
        handleCloseDialog();
      } catch (e) {
        console.error("Erro ao salvar pessoa:", e);
      } finally {
        setButtonIsLoading(false);
      }
    },
    [savePessoa, selectedPessoa, fetchPessoas, handleCloseDialog, indexQuery],
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
      await deletePessoa(id);
      await fetchPessoas(indexQuery);
    } catch (e) {
      console.error("Erro ao excluir pessoa:", e);
    }
  }, [pendingDeleteId, closeDeleteDialog, deletePessoa, fetchPessoas, indexQuery]);

  useEffect(() => {
    void fetchPessoas(indexQuery);
  }, [fetchPessoas, indexQuery]);

  return (
    <div className="flex w-full min-w-0 flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Pessoas</h1>
          <Button
            onClick={() => handleOpenDialog()}
            className="bg-[#FF6B00] hover:bg-[#E56000] text-white"
          >
            <Plus className="mr-2 h-4 w-4" />
            Nova Pessoa
          </Button>
        </div>
      </div>

      <div className="flex min-w-0 flex-col gap-4">
        <PPessoaFilter value={filters} onChange={handleFiltersChange} />

        <PPessoaTable
          data={pessoas}
          isLoading={isLoading}
          onEdit={handleOpenDialog}
          onDelete={openDeleteDialog}
        />

        <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
      </div>

      <PPessoaDialog
        open={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        pessoa={selectedPessoa}
        onSubmit={handleSave}
        isLoading={buttonIsLoading}
      />

      <ConfirmDialog
        isOpen={deleteDialogOpen}
        title="Pessoa"
        description="Confirmar exclusão"
        message="Tem certeza que deseja excluir esta pessoa?"
        confirmText="Excluir"
        onConfirm={() => void confirmDelete()}
        onCancel={closeDeleteDialog}
      />
    </div>
  );
}
