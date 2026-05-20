"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import { usePRetornoCraReadHook } from "@/packages/cra/hooks/PRetornoCra/usePRetornoCraReadHook";
import { DateRangePicker } from "@/shared/components/dateRangePicker/DateRangePicker";
import { FileUp, Search } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type { DateRange } from "react-day-picker";
import { toast } from "sonner";
import { PRetornoCraTable } from "./PRetornoCraTable";

function getTodayRange(): DateRange {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  return { from: yesterday, to: today };
}

export default function PRetornoCraIndex() {
  const { titulosRetorno, isLoading, fetchTitulosRetorno } = usePRetornoCraReadHook();
  const { bancos, isLoading: isLoadingBancos, fetchBancos } = usePBancoReadHook();
  const { ocorrencias, isLoading: isLoadingOcorrencias, fetchOcorrencias } = usePOcorrenciasReadHook();
  const [numeroApontamentoDe, setNumeroApontamentoDe] = useState("");
  const [numeroApontamentoAte, setNumeroApontamentoAte] = useState("");
  const [statusImportacao, setStatusImportacao] = useState("");
  const [dateRange, setDateRange] = useState<DateRange | undefined>(getTodayRange);

  useEffect(() => {
    void fetchTitulosRetorno();
    void fetchBancos();
    void fetchOcorrencias();
  }, [fetchTitulosRetorno, fetchBancos, fetchOcorrencias]);

  const data = useMemo(() => titulosRetorno as PTituloInterface[], [titulosRetorno]);
  const resumo = useMemo(() => {
    const total = data.length;
    const exportados = data.filter((titulo) => titulo.status_importacao === "E").length;
    const aguardando = data.filter((titulo) => titulo.status_importacao === "D").length;

    return { total, exportados, aguardando };
  }, [data]);
  const bancoLabelById = useMemo(
    () =>
      new Map(
        bancos.map((banco) => [
          banco.banco_id,
          banco.descricao || (banco.codigo_banco ? `Banco ${banco.codigo_banco}` : `Banco ${banco.banco_id}`),
        ]),
      ),
    [bancos],
  );
  const ocorrenciaLabelById = useMemo(
    () =>
      new Map(
        ocorrencias.map((ocorrencia) => [
          ocorrencia.ocorrencias_id,
          ocorrencia.descricao || ocorrencia.tipo || ocorrencia.codigo || `Ocorrência ${ocorrencia.ocorrencias_id}`,
        ]),
      ),
    [ocorrencias],
  );

  const handleVisualSearch = () => {
    toast.info("Filtro visual aplicado", {
      description: "A consulta por intervalo será processada pelo backend na próxima etapa.",
    });
  };

  const handleGerarArquivoRetorno = () => {
    toast.info("Geração em construção", {
      description: "A geração do arquivo de retorno CRA será integrada em uma próxima etapa.",
    });
  };

  const handleClearVisualFilter = () => {
    setNumeroApontamentoDe("");
    setNumeroApontamentoAte("");
    setStatusImportacao("");
    setDateRange(getTodayRange());
  };

  return (
    <div className="flex w-full flex-col gap-5">
      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight">CRA - Retorno</h1>
            <p className="text-sm text-muted-foreground">
              Acompanhe os títulos no processo de retorno e os principais dados operacionais.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <div className="rounded-md border bg-muted/30 px-3 py-1.5 text-sm">
              Total: <span className="font-semibold">{resumo.total}</span>
            </div>
            <div className="rounded-md border bg-muted/30 px-3 py-1.5 text-sm">
              Exportados: <span className="font-semibold text-emerald-600">{resumo.exportados}</span>
            </div>
            <div className="rounded-md border bg-muted/30 px-3 py-1.5 text-sm">
              Aguardando: <span className="font-semibold">{resumo.aguardando}</span>
            </div>
          </div>
        </div>
      </section>

      <section className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="grid gap-4 xl:grid-cols-[1fr_auto]">
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Número apontamento (de)
              </label>
              <Input
                type="number"
                placeholder="Ex.: 5000"
                value={numeroApontamentoDe}
                onChange={(event) => setNumeroApontamentoDe(event.target.value)}
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Número apontamento (até)
              </label>
              <Input
                type="number"
                placeholder="Ex.: 5999"
                value={numeroApontamentoAte}
                onChange={(event) => setNumeroApontamentoAte(event.target.value)}
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Status de importação
              </label>
              <Select
                value={statusImportacao || "all"}
                onValueChange={(value) => setStatusImportacao(value === "all" ? "" : value)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Status de importação" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos os status</SelectItem>
                  <SelectItem value="D">Aguardando</SelectItem>
                  <SelectItem value="E">Exportação</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Intervalo de data
              </label>
              <DateRangePicker value={dateRange} onChange={setDateRange} placeholder="Selecione o intervalo" />
            </div>
          </div>

          <div className="flex items-end gap-2 xl:justify-end">
            <Button
              type="button"
              className="bg-[#FF6B00] text-white transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-[#E56000]"
              onClick={handleVisualSearch}
            >
              <Search className="mr-1 h-4 w-4" />
              Pesquisar
            </Button>
            <Button type="button" variant="outline" onClick={handleClearVisualFilter}>
              Limpar
            </Button>
          </div>
        </div>
      </section>

      <section className="space-y-3">
        <PRetornoCraTable
          data={data}
          isLoading={isLoading || isLoadingBancos || isLoadingOcorrencias}
          bancoLabelById={bancoLabelById}
          ocorrenciaLabelById={ocorrenciaLabelById}
        />

        <div className="flex justify-end">
          <Button
            type="button"
            className="bg-[#FF6B00] text-white transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-[#E56000]"
            onClick={handleGerarArquivoRetorno}
          >
            <FileUp className="mr-1 h-4 w-4" />
            Gerar arquivo de retorno CRA
          </Button>
        </div>
      </section>
    </div>
  );
}
