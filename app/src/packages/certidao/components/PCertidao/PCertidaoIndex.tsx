"use client";

import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";
import { usePCertidaoReadHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoReadHook";
import { usePCertidaoSaveHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoSaveHook";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { isPCertidaoSaveResult } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import { Loader2, Plus, Search } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import type { DateRange } from "react-day-picker";
import { toast } from "sonner";
import { PCertidaoEmissaoDialogTitleRow, PCertidaoEmissaoForm } from "./PCertidaoEmissaoForm";
import { PCERTIDAO_TIPO_INFO_MARKDOWN, PCertidaoForm } from "./PCertidaoForm";
import type { PCertidaoFormValues } from "./PCertidaoFormValues";
import { PCertidaoTable } from "./PCertidaoTable";

function getStatusLabel(status?: PCertidaoInterface["status"] | string): string {
  const normalized = (status ?? "").trim().toUpperCase();
  if (normalized === "A" || normalized === "ATIVA" || normalized === "ATIVO" || normalized === "EMITIDA") {
    return "Ativa/Emitida";
  }
  if (normalized === "C" || normalized === "CANCELADA" || normalized === "INATIVA") {
    return "Cancelada";
  }
  return "-";
}

function normalizeCode(value?: string): string {
  return (value ?? "").trim().toUpperCase();
}

function getDateOnly(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

export default function PCertidaoIndex() {
  const { certidoes, isLoading, fetchCertidoes } = usePCertidaoReadHook();
  const { usuarios, isLoading: isLoadingUsuarios, fetchUsuarios } = useGUsuarioReadHook();
  const { isSaving: isSavingEmissao, saveCertidao: saveCertidaoEmissao } = usePCertidaoSaveHook();
  const initialFetchDoneRef = useRef(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<"" | "A" | "C">("");
  const [dateRange, setDateRange] = useState<DateRange | undefined>(undefined);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [emissaoDialogOpen, setEmissaoDialogOpen] = useState(false);
  const [editingCertidao, setEditingCertidao] = useState<PCertidaoInterface | null>(null);
  const [emissaoInfoOpen, setEmissaoInfoOpen] = useState(false);

  useEffect(() => {
    if (initialFetchDoneRef.current) return;
    initialFetchDoneRef.current = true;
    void Promise.all([fetchCertidoes(), fetchUsuarios()]);
  }, [fetchCertidoes, fetchUsuarios]);

  const usuarioLabelById = new Map<number, string>(
    usuarios.map((usuario) => [usuario.usuario_id, usuario.nome_completo || usuario.login || String(usuario.usuario_id)]),
  );

  const isPageLoading = isLoading || isLoadingUsuarios;
  const filteredCertidoes = useMemo(() => {
    const normalizedQuery = searchQuery.trim().toLowerCase();
    const from = dateRange?.from ? getDateOnly(dateRange.from) : undefined;
    const to = dateRange?.to ? getDateOnly(dateRange.to) : undefined;

    return certidoes.filter((certidao) => {
      if (normalizedQuery) {
        const apresentante = (certidao.apresentante ?? "").toLowerCase();
        const cpfcnpj = (certidao.cpfcnpj ?? "").toLowerCase();
        if (!apresentante.includes(normalizedQuery) && !cpfcnpj.includes(normalizedQuery)) {
          return false;
        }
      }

      if (statusFilter) {
        const normalizedStatus = normalizeCode(certidao.status);
        if (normalizedStatus !== statusFilter) return false;
      }

      if (from || to) {
        if (!certidao.data_certidao) return false;
        const current = getDateOnly(new Date(certidao.data_certidao));
        if (from && current < from) return false;
        if (to && current > to) return false;
      }

      return true;
    });
  }, [certidoes, dateRange?.from, dateRange?.to, searchQuery, statusFilter]);

  const handleEditarCertidao = (certidao: PCertidaoInterface) => {
    setEditingCertidao(certidao);
    setEditDialogOpen(true);
  };

  const handleCancelarCertidao = (certidao: PCertidaoInterface) => {
    toast.info("Funcionalidade em construção", {
      description: `Cancelamento da certidão #${certidao.certidao_id} (${getStatusLabel(certidao.status)}) ainda não implementado.`,
    });
  };

  const handleClearFilters = () => {
    setSearchQuery("");
    setStatusFilter("");
    setDateRange(undefined);
  };

  const handleOpenEmissaoDialog = () => {
    setEmissaoDialogOpen(true);
  };

  const handleEditSaved = async (_saved: PCertidaoInterface) => {
    setEditDialogOpen(false);
    setEditingCertidao(null);
    await fetchCertidoes();
  };

  const handleEmitNovaCertidao = async (payload: PCertidaoFormValues) => {
    const response = await saveCertidaoEmissao(payload);
    if (isPCertidaoSaveResult(response)) {
      setEmissaoDialogOpen(false);
      await fetchCertidoes();
    }
  };

  return (
    <div className="flex w-full flex-col gap-5">
      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight">Certidão</h1>
            <p className="text-sm text-muted-foreground">
              Consulte as certidões e acompanhe o status (A: ativa/emitida, C: cancelada), apresentante e horário.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className="rounded-md border bg-muted/30 px-3 py-1.5 text-sm">
              Registros: <span className="font-semibold">{filteredCertidoes.length}</span>
            </div>
            <Button
              type="button"
              className="bg-[#FF6B00] text-white transition-transform duration-200 hover:-translate-y-0.5 hover:bg-[#E56000]"
              onClick={handleOpenEmissaoDialog}
            >
              <Plus className="mr-1 h-4 w-4" />
              Emitir nova certidão
            </Button>
          </div>
        </div>
      </section>

      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="grid gap-4 xl:grid-cols-[1fr_auto]">
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Busca por apresentante / CPF-CNPJ
              </label>
              <Input
                placeholder="Ex.: João da Silva ou 111.111.111-11"
                value={searchQuery}
                onChange={(event) => setSearchQuery(event.target.value)}
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Status</label>
              <Select
                value={statusFilter || "all"}
                onValueChange={(value) => setStatusFilter(value === "A" || value === "C" ? value : "")}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Todos os status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os status</SelectItem>
                  <SelectItem value="A">Ativa/Emitida</SelectItem>
                  <SelectItem value="C">Cancelada</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Intervalo de data</label>
              <DateRangePicker value={dateRange} onChange={setDateRange} placeholder="Selecione o intervalo" />
            </div>
          </div>

          <div className="flex items-end gap-2 xl:justify-end">
            <Button type="button" className="bg-[#FF6B00] text-white hover:bg-[#E56000]">
              <Search className="mr-1 h-4 w-4" />
              Pesquisar
            </Button>
            <Button type="button" variant="outline" onClick={handleClearFilters}>
              Limpar
            </Button>
          </div>
        </div>
      </section>

      <PCertidaoTable
        data={filteredCertidoes}
        isLoading={isPageLoading}
        onEditarCertidao={handleEditarCertidao}
        onCancelarCertidao={handleCancelarCertidao}
        usuarioLabelById={usuarioLabelById}
      />

      <Dialog open={emissaoDialogOpen} onOpenChange={setEmissaoDialogOpen}>
        <DialogContent className="max-h-[88vh] gap-3 overflow-y-auto p-5 sm:max-w-3xl sm:p-6">
          <DialogHeader>
            <PCertidaoEmissaoDialogTitleRow onOpenTipoInfo={() => setEmissaoInfoOpen(true)} />
          </DialogHeader>

          {isLoadingUsuarios && emissaoDialogOpen ? (
            <div className="flex min-h-[200px] flex-col items-center justify-center gap-3 text-muted-foreground">
              <Loader2 className="h-5 w-5 animate-spin" />
              <p className="text-sm">Carregando…</p>
            </div>
          ) : (
            <PCertidaoEmissaoForm
              open={emissaoDialogOpen}
              usuarios={usuarios}
              isLoadingUsuarios={isLoadingUsuarios}
              onEmit={handleEmitNovaCertidao}
              onCancel={() => setEmissaoDialogOpen(false)}
              isSaving={isSavingEmissao}
            />
          )}
        </DialogContent>
      </Dialog>

      {editingCertidao ? (
        <PCertidaoForm
          key={editingCertidao.certidao_id}
          open={editDialogOpen}
          onOpenChange={(open) => {
            setEditDialogOpen(open);
            if (!open) setEditingCertidao(null);
          }}
          certidao={editingCertidao}
          onSaved={(saved) => {
            void handleEditSaved(saved);
          }}
        />
      ) : null}

      <InfoDialog
        isOpen={emissaoInfoOpen}
        onOpenChange={setEmissaoInfoOpen}
        title="Tipos de certidão"
        description="Diferença entre certidão negativa e positiva"
        content={PCERTIDAO_TIPO_INFO_MARKDOWN}
      />
    </div>
  );
}
