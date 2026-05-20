import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";

export type WorkflowActionKey =
  | "apontarTitulo"
  | "voltarProtesto"
  | "voltarIntimacao"
  | "cancelarTitulo"
  | "voltarApontamento"
  | "aceiteEdital"
  | "sustarTitulo"
  | "retiradaTitulo"
  | "desistirTitulo"
  | "liquidarTitulo"
  | "protestarTitulo"
  | "intimarTitulo";

export interface WorkflowActionButton {
  key: WorkflowActionKey;
  label: string;
}

export function getPTituloCancelamentoOptions(titulo: TituloListItem | null): WorkflowActionButton[] {
  const hasApontamentoBase = hasValue(titulo?.numero_apontamento) && hasValue(titulo?.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo?.data_intimacao);
  const hasProtestoCompleto = hasProtestoCompletoFields(titulo);

  if (hasProtestoCompleto) {
    return [
      { key: "cancelarTitulo", label: "Cancelar Título" },
      { key: "sustarTitulo", label: "Sustar Título" },
      { key: "retiradaTitulo", label: "Retirada do Título" },
    ];
  }

  if (hasIntimacao) {
    return [
      { key: "sustarTitulo", label: "Sustar Título" },
      { key: "retiradaTitulo", label: "Retirada do Título" },
      { key: "desistirTitulo", label: "Desistir Título" },
      { key: "liquidarTitulo", label: "Liquidar Título" },
    ];
  }

  return [];
}

export interface WorkflowProgressStep {
  label: string;
  completed: boolean;
}

export interface WorkflowProgressResult {
  hasApontado: boolean;
  hasIntimado: boolean;
  hasDesistenciaOuLiquidacao: boolean;
  hasProtestado: boolean;
  hasCancelado: boolean;
  stage: number;
  percent: number;
  stageLabel: string;
  steps: WorkflowProgressStep[];
}

function hasValue(value: unknown) {
  return value !== null && value !== undefined && value !== "";
}

/** Apontamento + intimação + data_protesto + livro + folha (registro completo de protesto). */
function hasProtestoCompletoFields(titulo: TituloListItem | null): boolean {
  const hasApontamentoBase = hasValue(titulo?.numero_apontamento) && hasValue(titulo?.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo?.data_intimacao);
  return (
    hasIntimacao &&
    hasValue(titulo?.data_protesto) &&
    hasValue(titulo?.livro_id_protesto) &&
    hasValue(titulo?.folha_protesto)
  );
}

/** Quando há data e motivo de cancelamento, o fluxo edital exige protesto registrado (cancelamento de protesto). */
function hasCancelamentoEstruturado(titulo: TituloListItem | null): boolean {
  return hasValue(titulo?.data_cancelamento) && hasValue(titulo?.motivo_cancelamento);
}

/**
 * Cancelamento explícito no cadastro: se vier data+motivo, só tratamos como cancelado no fluxo
 * se existir protesto completo; caso contrário mantemos outras regras (status ou só data).
 */
function hasCanceladoNoFluxo(titulo: TituloListItem | null, normalizedStatus: string): boolean {
  if (hasCancelamentoEstruturado(titulo)) {
    return hasProtestoCompletoFields(titulo) && hasValue(titulo?.data_cancelamento);
  }
  return hasValue(titulo?.data_cancelamento) || normalizedStatus.includes("cancel");
}

/**
 * Cancelamento “completo”: apontamento + intimação + protesto registrado + data e motivo de cancelamento
 * (cancelamento após protesto). Neste caso a única ação prevista é voltar ao estado de protesto.
 */
export function hasCancelamentoCompleto(titulo: TituloListItem | null): boolean {
  const hasApontamentoBase = hasValue(titulo?.numero_apontamento) && hasValue(titulo?.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo?.data_intimacao);
  return (
    hasApontamentoBase &&
    hasIntimacao &&
    hasProtestoCompletoFields(titulo) &&
    hasCancelamentoEstruturado(titulo)
  );
}

export function getWorkflowActionButtons(titulo: TituloListItem | null): WorkflowActionButton[] {
  const normalizedStatus = String(titulo?.situacao_aceite ?? "").toLowerCase();
  const hasApontamentoBase = hasValue(titulo?.numero_apontamento) && hasValue(titulo?.data_apontamento);
  const hasIntimacao = hasApontamentoBase && hasValue(titulo?.data_intimacao);
  const hasProtestado = hasProtestoCompletoFields(titulo) || normalizedStatus.includes("protest");
  const hasCancelado = hasCanceladoNoFluxo(titulo, normalizedStatus);
  const hasSemAndamento =
    !hasApontamentoBase &&
    !hasIntimacao &&
    !hasProtestado &&
    !hasCancelado;
  const hasDesistenciaLiquidacao =
    hasApontamentoBase &&
    hasIntimacao &&
    (hasValue(titulo?.data_desistencia) || hasValue(titulo?.data_sustado));
  const hasProtestoCompleto = hasProtestoCompletoFields(titulo);

  if (hasSemAndamento) {
    return [{ key: "apontarTitulo", label: "Apontar Título" }];
  }

  if (hasCancelamentoCompleto(titulo)) {
    return [{ key: "voltarProtesto", label: "Voltar para Protesto" }];
  }

  if (hasDesistenciaLiquidacao) {
    return [{ key: "voltarIntimacao", label: "Voltar para Intimação" }];
  }

  if (hasProtestoCompleto) {
    return [
      { key: "voltarIntimacao", label: "Voltar para Intimação" },
      { key: "cancelarTitulo", label: "Cancelar Título" },
    ];
  }

  if (hasIntimacao) {
    return [
      { key: "voltarApontamento", label: "Voltar para Apontamento" },
      { key: "aceiteEdital", label: "Aceite/Edital" },
      { key: "cancelarTitulo", label: "Cancelar Título" },
      { key: "protestarTitulo", label: "Protestar Título" },
    ];
  }

  if (hasApontamentoBase) {
    return [{ key: "intimarTitulo", label: "Intimar Título" }];
  }

  return [];
}

export function getWorkflowProgress(titulo: TituloListItem | null): WorkflowProgressResult {
  const normalizedStatus = String(titulo?.situacao_aceite ?? "").toLowerCase();

  const hasApontado = hasValue(titulo?.numero_apontamento) && hasValue(titulo?.data_apontamento);
  const hasIntimado = hasApontado && hasValue(titulo?.data_intimacao);
  const hasDesistenciaOuLiquidacao =
    hasIntimado &&
    (hasValue(titulo?.data_desistencia) ||
      hasValue(titulo?.data_pago) ||
      normalizedStatus.includes("desist") ||
      normalizedStatus.includes("liquid") ||
      normalizedStatus.includes("pago"));
  const hasProtestoCompleto = hasProtestoCompletoFields(titulo);
  const hasProtestado = hasProtestoCompleto || normalizedStatus.includes("protest");
  const hasCancelado = hasCanceladoNoFluxo(titulo, normalizedStatus);

  const stage = hasDesistenciaOuLiquidacao
    ? 3
    : hasCancelado
      ? 5
      : hasProtestado
        ? 4
        : hasIntimado
          ? 2
          : hasApontado
            ? 1
            : 0;

  const stageLabel =
    stage === 5
      ? "Cancelado"
      : stage === 4
        ? "Protestado"
        : stage === 3
          ? "Desistido/Liquidado"
          : stage === 2
            ? "Intimado"
            : stage === 1
              ? "Apontado"
              : "Sem andamento";

  const stepsBase: WorkflowProgressStep[] = [
    { label: "Apontamento", completed: stage >= 1 },
    { label: "Intimação", completed: stage >= 2 },
    { label: "Desistido/Liquidado", completed: stage >= 3 && stage !== 4 && stage !== 5 ? true : hasDesistenciaOuLiquidacao },
    { label: "Protesto", completed: stage >= 4 && !hasCancelado ? true : hasProtestado },
    { label: "Cancelado", completed: stage >= 5 ? true : hasCancelado },
  ];

  const steps = hasDesistenciaOuLiquidacao
    ? stepsBase.filter((step) => step.label !== "Protesto" && step.label !== "Cancelado")
    : hasProtestado || hasCancelado
      ? stepsBase.filter((step) => step.label !== "Desistido/Liquidado")
      : stepsBase;
  const currentStepLabel = hasDesistenciaOuLiquidacao
    ? "Desistido/Liquidado"
    : hasCancelado
      ? "Cancelado"
      : hasProtestado
        ? "Protesto"
        : hasIntimado
          ? "Intimação"
          : hasApontado
            ? "Apontamento"
            : "";
  const currentStepIndex = steps.findIndex((step) => step.label === currentStepLabel);
  const percent = currentStepIndex < 0 || steps.length === 0 ? 0 : ((currentStepIndex + 1) / steps.length) * 100;

  return {
    hasApontado,
    hasIntimado,
    hasDesistenciaOuLiquidacao,
    hasProtestado,
    hasCancelado,
    stage,
    percent,
    stageLabel,
    steps,
  };
}

export function getPTituloConfirmDialogMessage(label: string): string {
  const normalized = label.trim();
  if (normalized === "Apontar Título") {
    return "Deseja realmente apontar este título para iniciar o fluxo?";
  }
  if (normalized === "Voltar para Protesto") {
    return "Deseja realmente voltar este título para a etapa de protesto? O cancelamento será desfeito conforme a regra do sistema.";
  }
  if (normalized === "Voltar para Intimação") {
    return "Deseja realmente voltar este título para a etapa de intimação?";
  }
  if (normalized === "Cancelar Título") {
    return "Deseja realmente cancelar este título? Esta ação altera o andamento atual.";
  }
  if (normalized === "Voltar para Apontamento") {
    return "Deseja realmente retornar este título para a etapa de apontamento?";
  }
  if (normalized === "Aceite/Edital") {
    return "Deseja realmente registrar a ação de aceite/edital para este título?";
  }
  if (normalized === "Sustar Título") {
    return "Deseja realmente sustar este título?";
  }
  if (normalized === "Retirada do Título") {
    return "Deseja realmente registrar a retirada deste título?";
  }
  if (normalized === "Desistir Título") {
    return "Deseja realmente registrar a desistência deste título?";
  }
  if (normalized === "Liquidar Título") {
    return "Deseja realmente liquidar este título?";
  }
  if (normalized === "Protestar Título") {
    return "Deseja realmente protestar este título?";
  }
  if (normalized === "Intimar Título") {
    return "Deseja realmente intimar este título?";
  }
  return "Confirme para executar esta ação no título.";
}
