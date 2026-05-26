"use client";

import { Button } from "@/components/ui/button";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";
import { PCertidaoFilter } from "@/packages/certidao/components/PCertidao/PCertidaoFilter";
import {
  buildPCertidaoIndexQuery,
  defaultPCertidaoFilterState,
  type PCertidaoFilterState,
} from "@/packages/certidao/components/PCertidao/pCertidaoFilterUtils";
import { usePCertidaoCancelarHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoCancelarHook";
import { usePCertidaoReadHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoReadHook";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { isPCertidaoSaveResult } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { Plus } from "lucide-react";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";
import { PCertidaoForm } from "./PCertidaoForm";
import { PCertidaoTable } from "./PCertidaoTable";

const PCERTIDAO_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

function getTipoCertidaoConfirmLabel(tipo?: PCertidaoInterface["tipo_certidao"] | string): string {
  const normalized = (tipo ?? "").trim().toUpperCase();
  if (normalized === "P") return "positiva";
  if (normalized === "N") return "negativa";
  if (normalized === "R") return "Serasa";
  return "selecionada";
}

function buildCancelamentoMessage(certidao: PCertidaoInterface): string {
  const tipo = getTipoCertidaoConfirmLabel(certidao.tipo_certidao);
  const nome = certidao.nome?.trim() || certidao.apresentante?.trim() || "Não informado";
  const cpfcnpj = certidao.cpfcnpj?.trim() || "Não informado";

  return `Você tem certeza que deseja cancelar a certidão ${tipo} de ${nome} - ${cpfcnpj}? Lembrando que esta ação é irreversível e o selo é cancelado automaticamente.`;
}

export default function PCertidaoIndex() {
  const router = useRouter();
  const { certidoes, pagination, isLoading, fetchCertidoes } = usePCertidaoReadHook();
  const { usuarios, isLoading: isLoadingUsuarios, fetchUsuarios } = useGUsuarioReadHook();
  const { isCanceling, cancelarCertidao } = usePCertidaoCancelarHook();
  const [filters, setFilters] = useState<PCertidaoFilterState>(defaultPCertidaoFilterState);
  const [page, setPage] = useState(1);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingCertidao, setEditingCertidao] = useState<PCertidaoInterface | null>(null);
  const [cancelingCertidao, setCancelingCertidao] = useState<PCertidaoInterface | null>(null);

  const apiFilters = useMemo(() => buildPCertidaoIndexQuery(filters), [filters]);
  const indexQuery = useMemo(
    () => ({
      ...(apiFilters ?? {}),
      page,
      per_page: PCERTIDAO_PER_PAGE,
    }),
    [apiFilters, page],
  );

  useEffect(() => {
    void fetchUsuarios();
  }, [fetchUsuarios]);

  useEffect(() => {
    void fetchCertidoes(indexQuery);
  }, [fetchCertidoes, indexQuery]);

  const usuarioLabelById = new Map<number, string>(
    usuarios.map((usuario) => [usuario.usuario_id, usuario.nome_completo || usuario.login || String(usuario.usuario_id)]),
  );

  const isPageLoading = isLoading || isLoadingUsuarios || isCanceling;

  const handleFiltersChange = useCallback((next: PCertidaoFilterState) => {
    setFilters(next);
    setPage(1);
  }, []);

  const handleEditarCertidao = (certidao: PCertidaoInterface) => {
    setEditingCertidao(certidao);
    setEditDialogOpen(true);
  };

  const handleCancelarCertidao = (certidao: PCertidaoInterface) => {
    setCancelingCertidao(certidao);
  };

  const closeCancelDialog = () => {
    if (isCanceling) return;
    setCancelingCertidao(null);
  };

  const handleConfirmCancelamento = async () => {
    if (!cancelingCertidao || isCanceling) return;

    const response = await cancelarCertidao(cancelingCertidao.certidao_id);
    if (isPCertidaoSaveResult(response)) {
      setCancelingCertidao(null);
      await fetchCertidoes(indexQuery);
    }
  };

  const handleOpenEmissaoPage = () => {
    router.push("/certidao/new");
  };

  const handleEditSaved = async () => {
    setEditDialogOpen(false);
    setEditingCertidao(null);
    await fetchCertidoes(indexQuery);
  };

  return (
    <div className="flex w-full min-w-0 flex-col gap-4">
      <section className="rounded-xl border bg-card p-4 shadow-xs">
        <div className="flex min-w-0 flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
          <div className="min-w-0 space-y-1">
            <h1 className="text-2xl font-bold tracking-tight md:text-3xl">Certidão</h1>
            <p className="max-w-3xl text-sm text-muted-foreground">
              Consulte as certidões e acompanhe o status (A: ativa/emitida, C: cancelada), apresentante e horário.
            </p>
          </div>
          <div className="flex shrink-0 flex-wrap items-center gap-2 xl:justify-end">
            <div className="rounded-md border bg-muted/30 px-2.5 py-1.5 text-xs md:text-sm">
              Registros: <span className="font-semibold">{pagination.total}</span>
            </div>
            <Button
              type="button"
              size="sm"
              className="whitespace-nowrap bg-[#FF6B00] text-white transition-transform duration-200 hover:-translate-y-0.5 hover:bg-[#E56000] md:h-9"
              onClick={handleOpenEmissaoPage}
            >
              <Plus className="mr-1 h-4 w-4" />
              Emitir nova certidão
            </Button>
          </div>
        </div>
      </section>

      <PCertidaoFilter
        value={filters}
        onChange={handleFiltersChange}
        onSearch={() => void fetchCertidoes(indexQuery)}
        disabled={isPageLoading}
      />

      <PCertidaoTable
        data={certidoes}
        isLoading={isPageLoading}
        onEditarCertidao={handleEditarCertidao}
        onCancelarCertidao={handleCancelarCertidao}
        usuarioLabelById={usuarioLabelById}
      />

      <Pagination pagination={pagination} onPageChange={setPage} disabled={isPageLoading} />

      {editingCertidao ? (
        <PCertidaoForm
          key={editingCertidao.certidao_id}
          open={editDialogOpen}
          onOpenChange={(open) => {
            setEditDialogOpen(open);
            if (!open) setEditingCertidao(null);
          }}
          certidao={editingCertidao}
          onSaved={() => {
            void handleEditSaved();
          }}
        />
      ) : null}

      <ConfirmDialog
        isOpen={Boolean(cancelingCertidao)}
        title="Certidão"
        description="Confirmar cancelamento"
        message={cancelingCertidao ? buildCancelamentoMessage(cancelingCertidao) : ""}
        confirmText={isCanceling ? "Cancelando..." : "Cancelar certidão"}
        cancelText="Voltar"
        onConfirm={() => {
          void handleConfirmCancelamento();
        }}
        onCancel={closeCancelDialog}
      />
    </div>
  );
}
