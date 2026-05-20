"use client";

import { PTituloAceiteEditalButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloAceiteEditalButton";
import { PTituloApontarButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloApontarButton";
import { PTituloCancelamentoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloCancelamentoButton";
import { PTituloDesistenciaButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloDesistenciaButton";
import { PTituloIntimacaoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloIntimacaoButton";
import { PTituloLiquidacaoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloLiquidacaoButton";
import { PTituloProtestoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloProtestoButton";
import { PTituloVoltarApontamentoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloVoltarApontamentoButton";
import { PTituloVoltarIntimacaoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloVoltarIntimacaoButton";
import { PTituloVoltarProtestoButton } from "@/packages/administrativo/components/PTitulo/actions/PTituloVoltarProtestoButton";
import { PTituloCancelamentoOptionsDIalog } from "@/packages/administrativo/components/PTitulo/PTituloCancelamentoOptionsDIalog";
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
import {
  getWorkflowActionButtons,
  getPTituloCancelamentoOptions,
  getWorkflowProgress,
} from "@/packages/utils/PTitulo/ptituloWorkflowUtils";
import { CheckCircle2, ChevronLeft } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { PTituloDetailsForm } from "./PTituloDetailsForm";

export function PTituloForm({ id }: { id?: string }) {
  const router = useRouter();
  const isNew = id == null || id === "";
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { titulo, setTitulo, isLoading, fetchTituloById } = usePTituloShowHook();
  const fetchTituloByIdRef = useRef(fetchTituloById);
  fetchTituloByIdRef.current = fetchTituloById;

  const { bancos, fetchBancos } = usePBancoReadHook();
  const { especies, fetchEspecies } = usePEspecieReadHook();
  const { ocorrencias, fetchOcorrencias } = usePOcorrenciasReadHook();
  const { motivos, fetchMotivos } = usePMotivosReadHook();
  const { motivosCancelamento, fetchMotivosCancelamento } = usePMotivosCancelamentoReadHook();

  useEffect(() => {
    void fetchBancos();
    void fetchEspecies();
    void fetchOcorrencias();
    void fetchMotivos();
    void fetchMotivosCancelamento();
  }, [fetchBancos, fetchEspecies, fetchMotivos, fetchMotivosCancelamento, fetchOcorrencias]);

  useEffect(() => {
    if (isNew) {
      setTitulo(null);
      return;
    }

    const numericId = Number(id);
    if (Number.isNaN(numericId)) {
      setTitulo(null);
      return;
    }

    void fetchTituloByIdRef.current(numericId);
  }, [id, isNew, setTitulo]);

  const selectOptionsByField = useMemo<PTituloSelectOptionsByField>(
    () => ({
      especie_id: especies.map((especie) => ({
        value: String(especie.especie_id),
        label: especie.descricao || especie.especie || "-",
      })),
      banco_id: bancos.map((banco) => ({
        value: String(banco.banco_id),
        label: banco.descricao || banco.codigo_banco || "-",
      })),
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
    }),
    [bancos, especies, motivos, motivosCancelamento, ocorrencias],
  );

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
    <div className="flex w-full flex-col gap-6">
      <header className="rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
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
                  <h1 className="min-w-0 text-xl font-bold tracking-tight sm:text-2xl xl:text-3xl">
                    {isNew ? "Cadastrar Título" : "Detalhes do Título"}
                  </h1>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">
                  Gerencie os dados e o fluxo operacional do título nesta tela.
                </p>
              </div>
            </div>

            <div className="flex w-full flex-col gap-2 xl:w-auto xl:shrink-0 xl:items-end">
              {workflowActionButtons.length > 0 ? (
                <div className="rounded-lg bg-muted/30 p-2 xl:max-w-[52rem]">
                  <div className="flex flex-wrap items-center gap-1.5 xl:justify-end [&>div>button]:h-8 [&>div>button]:px-2.5 [&>div>button]:text-xs xl:[&>div>button]:h-9 xl:[&>div>button]:px-3 xl:[&>div>button]:text-sm">
                    {workflowActionButtons.map((buttonConfig) => (
                      <div key={buttonConfig.key}>
                        {numericTituloId == null ? null : buttonConfig.key === "voltarProtesto" ? (
                          <PTituloVoltarProtestoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "apontarTitulo" ? (
                          <PTituloApontarButton
                            id={numericTituloId}
                            numeroApontamento={titulo?.numero_apontamento ?? null}
                            onSuccess={handleActionSuccess}
                          />
                        ) : buttonConfig.key === "voltarIntimacao" ? (
                          <PTituloVoltarIntimacaoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "cancelarTitulo" ? (
                          cancelamentoOptions.length > 0 ? (
                            <PTituloCancelamentoOptionsDIalog
                              id={numericTituloId}
                              titulo={titulo}
                              options={cancelamentoOptions}
                              onSuccess={handleActionSuccess}
                            />
                          ) : (
                            <PTituloCancelamentoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                          )
                        ) : buttonConfig.key === "voltarApontamento" ? (
                          <PTituloVoltarApontamentoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "aceiteEdital" ? (
                          <PTituloAceiteEditalButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "desistirTitulo" ? (
                          <PTituloDesistenciaButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "liquidarTitulo" ? (
                          <PTituloLiquidacaoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "protestarTitulo" ? (
                          <PTituloProtestoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : buttonConfig.key === "intimarTitulo" ? (
                          <PTituloIntimacaoButton id={numericTituloId} onSuccess={handleActionSuccess} />
                        ) : null}
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </div>

          <div className="rounded-lg bg-muted/20 p-3">
            <div className="h-2 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-[#FF6B00] transition-all duration-700 ease-out hover:brightness-110"
                style={{ width: `${workflowProgress.percent}%` }}
              />
            </div>
            <div
              className="mt-2 grid gap-2"
              style={{ gridTemplateColumns: `repeat(${Math.max(workflowProgress.steps.length, 1)}, minmax(0, 1fr))` }}
            >
              {workflowProgress.steps.map((step) => (
                <div
                  key={step.label}
                  className={`flex items-center gap-1 text-[11px] ${step.completed ? "text-emerald-600" : "text-muted-foreground"}`}
                >
                  {step.completed ? <CheckCircle2 className="h-3.5 w-3.5" /> : <span className="h-2 w-2 rounded-full bg-muted-foreground/40" />}
                  <span>{step.label}</span>
                </div>
              ))}
            </div>
          </div>
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
