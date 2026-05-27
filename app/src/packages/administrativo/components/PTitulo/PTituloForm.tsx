"use client";

import { formatBancoSelectLabel } from "@/packages/administrativo/components/PBanco/PBancoSelectObject";
import { formatEspecieSelectLabel } from "@/packages/administrativo/components/PEspecie/PEspecieSelectObject";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import { usePEspecieReadHook } from "@/packages/administrativo/hooks/PEspecie/usePEspecieReadHook";
import { usePMotivosReadHook } from "@/packages/administrativo/hooks/PMotivos/usePMotivosReadHook";
import { usePMotivosCancelamentoReadHook } from "@/packages/administrativo/hooks/PMotivosCancelamento/usePMotivosCancelamentoReadHook";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import { usePTituloShowHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloShowHook";
import type {
  PTituloDetailsFormValues,
  PTituloSelectOptionsByField,
} from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { ensureTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";
import {
  getWorkflowActionButtons,
  getPTituloCancelamentoOptions,
  getWorkflowProgress,
} from "@/packages/utils/PTitulo/ptituloWorkflowUtils";
import { ChevronLeft } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { PTituloDetailsForm } from "./PTituloDetailsForm";
import { PTituloWorkflowActions } from "./PTituloWorkflowActions";
import { PTituloWorkflowProgress } from "./PTituloWorkflowProgress";

export function PTituloForm({ id }: { id?: string }) {
  const router = useRouter();
  const isNew = id == null || id === "";
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { titulo, setTitulo, isLoading, fetchTituloById } = usePTituloShowHook();
  const fetchTituloByIdRef = useRef(fetchTituloById);
  const lastInitialFetchIdRef = useRef<number | null>(null);
  fetchTituloByIdRef.current = fetchTituloById;

  const { bancos, fetchBancos } = usePBancoReadHook();
  const { especies, fetchEspecies } = usePEspecieReadHook();
  const { ocorrencias, fetchOcorrencias } = usePOcorrenciasReadHook();
  const { motivos, fetchMotivos } = usePMotivosReadHook();
  const { motivosCancelamento, fetchMotivosCancelamento } = usePMotivosCancelamentoReadHook();

  useEffect(() => {
    void fetchBancos({ page: 1, per_page: 500, sort: "banco_id.desc" });
    void fetchEspecies({ page: 1, per_page: 500, sort: "especie_id.asc" });
    void fetchOcorrencias();
    void fetchMotivos();
    void fetchMotivosCancelamento();
  }, [fetchBancos, fetchEspecies, fetchMotivos, fetchMotivosCancelamento, fetchOcorrencias]);

  useEffect(() => {
    if (isNew) {
      lastInitialFetchIdRef.current = null;
      setTitulo(null);
      return;
    }

    const numericId = Number(id);
    if (Number.isNaN(numericId)) {
      lastInitialFetchIdRef.current = null;
      setTitulo(null);
      return;
    }

    if (lastInitialFetchIdRef.current === numericId) {
      return;
    }

    lastInitialFetchIdRef.current = numericId;
    void fetchTituloByIdRef.current(numericId).catch(() => {
      lastInitialFetchIdRef.current = null;
    });
  }, [id, isNew, setTitulo]);

  const selectOptionsByField = useMemo<PTituloSelectOptionsByField>(() => {
    const especieFromList = especies.map((especie) => ({
      value: String(especie.especie_id),
      label: formatEspecieSelectLabel(especie),
    }));
    const bancoFromList = bancos.map((banco) => ({
      value: String(banco.banco_id),
      label: formatBancoSelectLabel(banco),
    }));

    const especieId =
      titulo?.especie_id != null
        ? String(titulo.especie_id)
        : titulo?.especie?.especie_id != null
          ? String(titulo.especie.especie_id)
          : undefined;
    const bancoId =
      titulo?.banco_id != null
        ? String(titulo.banco_id)
        : titulo?.banco?.banco_id != null
          ? String(titulo.banco.banco_id)
          : undefined;

    const especieLabelFromTitulo = titulo?.especie
      ? formatEspecieSelectLabel(titulo.especie)
      : titulo?.especie_id != null
        ? formatEspecieSelectLabel({
            especie_id: titulo.especie_id,
            especie: titulo.especie_sigla,
          })
        : undefined;
    const bancoLabelFromTitulo = titulo?.banco
      ? formatBancoSelectLabel(titulo.banco)
      : titulo?.banco_id != null
        ? formatBancoSelectLabel({ banco_id: titulo.banco_id })
        : undefined;

    return {
      especie_id: ensureTituloSelectOption(especieFromList, especieId, especieLabelFromTitulo),
      banco_id: ensureTituloSelectOption(bancoFromList, bancoId, bancoLabelFromTitulo),
      ocorrencia_id: ocorrencias.map((ocorrencia) => ({
        value: String(ocorrencia.ocorrencias_id),
        label: ocorrencia.descricao || ocorrencia.tipo || ocorrencia.codigo || "-",
      })),
      motivo_apontamento_id: motivos.map((motivo) => ({
        value: String(motivo.motivos_id),
        label: motivo.descricao || motivo.codigo || "-",
      })),
      motivo_cancelamento: motivosCancelamento.map((motivoCancelamento) => ({
        value: String(motivoCancelamento.motivos_cancelamento_id),
        label: motivoCancelamento.descricao || motivoCancelamento.ord_jud_ou_rem_ind || "-",
      })),
    };
  }, [bancos, especies, motivos, motivosCancelamento, ocorrencias, titulo]);

  const workflowActionButtons = useMemo(() => {
    return getWorkflowActionButtons(titulo);
  }, [titulo]);
  const cancelamentoOptions = useMemo(() => {
    return getPTituloCancelamentoOptions(titulo);
  }, [titulo]);

  const numericTituloId = useMemo(() => {
    if (typeof titulo?.titulo_id === "number" && !Number.isNaN(titulo.titulo_id)) {
      return titulo.titulo_id;
    }
    if (id) {
      const parsed = Number(id);
      if (!Number.isNaN(parsed)) return parsed;
    }
    return null;
  }, [id, titulo?.titulo_id]);

  const handleActionSuccess = (nextTitulo: typeof titulo) => {
    setTitulo(nextTitulo);

    const nextId =
      typeof nextTitulo?.titulo_id === "number" && !Number.isNaN(nextTitulo.titulo_id)
        ? nextTitulo.titulo_id
        : numericTituloId;

    if (typeof nextId === "number" && nextId > 0) {
      void fetchTituloByIdRef.current(nextId);
    }
  };

  const workflowProgress = useMemo(() => {
    return getWorkflowProgress(titulo);
  }, [titulo]);

  const handleSubmit = async (data: PTituloDetailsFormValues) => {
    void data;
    setIsSubmitting(true);
    try {
      router.push("/titulos");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex w-full flex-col gap-4">
      <header className="rounded-xl border bg-card px-4 py-3 shadow-xs md:px-5 md:py-4">
        <div className="flex flex-col gap-2">
          <div className="flex flex-col gap-2 xl:flex-row xl:items-start xl:justify-between">
            <div className="flex min-w-0 items-start gap-2">
              <button
                type="button"
                onClick={() => router.back()}
                aria-label="Voltar para página anterior"
                className="text-muted-foreground hover:text-[#FF6B00] inline-flex h-8 w-8 items-center justify-center rounded-md transition-colors"
              >
                <ChevronLeft className="h-6 w-6" strokeWidth={1.5} />
              </button>

              <div className="min-w-0">
                <div className="flex min-w-0 flex-wrap items-center gap-2">
                  <h1 className="min-w-0 text-xl font-bold tracking-tight sm:text-2xl">
                    {isNew ? "Cadastrar Título" : "Detalhes do Título"}
                  </h1>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">
                  Gerencie os dados e o fluxo operacional do título nesta tela.
                </p>
              </div>
            </div>

            <div className="flex w-full flex-col gap-2 xl:w-auto xl:shrink-0 xl:items-end">
              <PTituloWorkflowActions
                actions={workflowActionButtons}
                cancelamentoOptions={cancelamentoOptions}
                numericTituloId={numericTituloId}
                titulo={titulo}
                onSuccess={handleActionSuccess}
              />
            </div>
          </div>

          <PTituloWorkflowProgress progress={workflowProgress} />
        </div>
      </header>

      {isLoading ? (
        <div className="text-muted-foreground w-full rounded-md border p-8 text-center">Carregando título...</div>
      ) : (
        <PTituloDetailsForm
          titulo={titulo}
          onSubmit={handleSubmit}
          isLoading={isSubmitting}
          selectOptionsByField={selectOptionsByField}
        />
      )}
    </div>
  );
}
