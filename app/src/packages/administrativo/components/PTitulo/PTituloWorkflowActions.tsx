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
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import type { WorkflowActionButton } from "@/packages/utils/PTitulo/ptituloWorkflowUtils";

interface PTituloWorkflowActionsProps {
  actions: WorkflowActionButton[];
  cancelamentoOptions: WorkflowActionButton[];
  numericTituloId: number | null;
  titulo: TituloListItem | null;
  onSuccess: (titulo: TituloListItem) => void;
}

export function PTituloWorkflowActions({
  actions,
  cancelamentoOptions,
  numericTituloId,
  titulo,
  onSuccess,
}: PTituloWorkflowActionsProps) {
  if (actions.length === 0 || numericTituloId == null) {
    return null;
  }

  return (
    <div className="rounded-lg bg-muted/30 p-2 xl:max-w-[52rem]">
      <div className="flex flex-wrap items-center gap-1.5 xl:justify-end">
        {actions.map((action) => (
          <div key={action.key}>{renderWorkflowAction(action, numericTituloId, titulo, cancelamentoOptions, onSuccess)}</div>
        ))}
      </div>
    </div>
  );
}

function renderWorkflowAction(
  action: WorkflowActionButton,
  numericTituloId: number,
  titulo: TituloListItem | null,
  cancelamentoOptions: WorkflowActionButton[],
  onSuccess: (titulo: TituloListItem) => void,
) {
  switch (action.key) {
    case "voltarProtesto":
      return <PTituloVoltarProtestoButton id={numericTituloId} onSuccess={onSuccess} />;
    case "apontarTitulo":
      return (
        <PTituloApontarButton
          id={numericTituloId}
          numeroApontamento={titulo?.numero_apontamento ?? null}
          onSuccess={onSuccess}
        />
      );
    case "voltarIntimacao":
      return <PTituloVoltarIntimacaoButton id={numericTituloId} onSuccess={onSuccess} />;
    case "cancelarTitulo":
      return cancelamentoOptions.length > 0 ? (
        <PTituloCancelamentoOptionsDIalog
          id={numericTituloId}
          titulo={titulo}
          options={cancelamentoOptions}
          onSuccess={onSuccess}
        />
      ) : (
        <PTituloCancelamentoButton id={numericTituloId} onSuccess={onSuccess} />
      );
    case "voltarApontamento":
      return <PTituloVoltarApontamentoButton id={numericTituloId} onSuccess={onSuccess} />;
    case "aceiteEdital":
      return <PTituloAceiteEditalButton id={numericTituloId} onSuccess={onSuccess} />;
    case "desistirTitulo":
      return <PTituloDesistenciaButton id={numericTituloId} onSuccess={onSuccess} />;
    case "liquidarTitulo":
      return <PTituloLiquidacaoButton id={numericTituloId} onSuccess={onSuccess} />;
    case "protestarTitulo":
      return <PTituloProtestoButton id={numericTituloId} onSuccess={onSuccess} />;
    case "intimarTitulo":
      return <PTituloIntimacaoButton id={numericTituloId} onSuccess={onSuccess} />;
    case "retiradaTitulo":
    case "sustarTitulo":
      return null;
  }
}
