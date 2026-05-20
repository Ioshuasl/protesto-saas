"use client";

import { useEffect, useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { usePTituloReadHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloReadHook";
import { usePTituloSaveHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloSaveHook";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import { PTituloFilter } from "./PTituloFilter";
import { toInputDate } from "./titulo-list-utils";
import { PTituloTable } from "./PTituloTable";

export interface PTituloWorkflowState {
  hasApontamentoBase: boolean;
  hasIntimacao: boolean;
  hasProtestoCompleto: boolean;
}

function getPTituloWorkflowState(titulo: TituloListItem): PTituloWorkflowState {
  const hasValue = (value: unknown) => value !== null && value !== undefined && value !== "";
  const hasApontamentoBase = hasValue(titulo.numero_apontamento) && hasValue(titulo.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo.data_intimacao);
  const hasProtestoCompleto =
    hasIntimacao &&
    hasValue(titulo.data_protesto) &&
    hasValue(titulo.livro_id_protesto) &&
    hasValue(titulo.folha_protesto);

  return { hasApontamentoBase, hasIntimacao, hasProtestoCompleto };
}

export default function PTituloIndex() {
  const router = useRouter();
  const { titulos, isLoading, fetchTitulos } = usePTituloReadHook();
  const { saveTituloStatus } = usePTituloSaveHook();

  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    void fetchTitulos();
  }, [fetchTitulos]);

  const filteredTitulos = useMemo(() => {
    return titulos.filter((titulo) => {
      const query = searchQuery.trim().toLowerCase();
      const status = titulo.status_descricao ?? titulo.situacao_aceite ?? "";
      const apontamento = toInputDate(titulo.data_apontamento as unknown as string);

      const matchesSearch =
        !query ||
        titulo.devedor_nome?.toLowerCase().includes(query) ||
        titulo.devedor_cpfcnpj?.toLowerCase().includes(query) ||
        titulo.apresentante_nome?.toLowerCase().includes(query) ||
        titulo.credor_nome?.toLowerCase().includes(query) ||
        titulo.cedente_nome?.toLowerCase().includes(query) ||
        titulo.partes_label?.toLowerCase().includes(query) ||
        titulo.partes_documentos?.toLowerCase().includes(query);

      const matchesStatus = statusFilter === "all" || status.toLowerCase() === statusFilter.toLowerCase();
      const matchesStartDate = !startDate || (apontamento && apontamento >= startDate);
      const matchesEndDate = !endDate || (apontamento && apontamento <= endDate);

      return Boolean(matchesSearch && matchesStatus && matchesStartDate && matchesEndDate);
    });
  }, [titulos, searchQuery, statusFilter, startDate, endDate]);

  const tableData = useMemo(
    () => filteredTitulos.map((titulo) => ({ ...titulo, ...getPTituloWorkflowState(titulo) })),
    [filteredTitulos],
  );

  const handleViewDetails = (titulo: TituloListItem) => {
    router.push(`/titulos/${titulo.titulo_id}`);
  };

  const handleUpdateStatus = async (tituloId: number, status: "Em Tríduo" | "Pago" | "Protestado") => {
    try {
      await saveTituloStatus(tituloId, status);
      await fetchTitulos();
    } catch (error) {
      console.error("Erro ao atualizar status do título:", error);
    }
  };

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight">Gestão de Títulos</h1>
          <Button className="bg-[#FF6B00] hover:bg-[#E56000] text-white" onClick={() => router.push("/titulo/new")}>
            <Plus className="mr-2 h-4 w-4" strokeWidth={1.5} />
            Novo Título
          </Button>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <PTituloFilter
          searchQuery={searchQuery}
          status={statusFilter}
          startDate={startDate}
          endDate={endDate}
          onSearchChange={setSearchQuery}
          onStatusChange={setStatusFilter}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
        />

        <PTituloTable
          data={tableData}
          isLoading={isLoading}
          onViewDetails={handleViewDetails}
          onUpdateStatus={handleUpdateStatus}
        />
      </div>
    </div>
  );
}
