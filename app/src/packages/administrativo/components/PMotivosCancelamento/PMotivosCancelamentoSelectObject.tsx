"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePMotivosCancelamentoReadHook } from "@/packages/administrativo/hooks/PMotivosCancelamento/usePMotivosCancelamentoReadHook";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import { cn } from "@/lib/utils";

export interface PMotivosCancelamentoSelectObjectProps {
  value?: string;
  onValueChange?: (motivosCancelamentoId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
  optionsOverride?: PTituloSelectOption[];
}

function motivoCancelamentoLabel(m: {
  descricao?: string;
  ord_jud_ou_rem_ind?: string;
  motivos_cancelamento_id: number;
}) {
  return m.descricao?.trim() || m.ord_jud_ou_rem_ind?.trim() || `Motivo ${m.motivos_cancelamento_id}`;
}

export function PMotivosCancelamentoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o motivo de cancelamento",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum motivo de cancelamento disponível",
  optionsOverride,
}: PMotivosCancelamentoSelectObjectProps) {
  const { motivosCancelamento, isLoading, fetchMotivosCancelamento } = usePMotivosCancelamentoReadHook();

  useEffect(() => {
    void fetchMotivosCancelamento();
  }, [fetchMotivosCancelamento]);

  const options = useMemo(() => {
    if (optionsOverride && optionsOverride.length > 0) {
      return optionsOverride;
    }
    return motivosCancelamento.map((m) => ({
      value: String(m.motivos_cancelamento_id),
      label: motivoCancelamentoLabel(m),
    }));
  }, [optionsOverride, motivosCancelamento]);

  const selectedLabel = useMemo(
    () => options.find((o) => o.value === (value ?? ""))?.label,
    [options, value],
  );

  return (
    <Select
      value={value && value.length > 0 ? value : undefined}
      onValueChange={onValueChange}
      disabled={disabled || (isLoading && !(optionsOverride && optionsOverride.length > 0))}
    >
      <SelectTrigger className={cn("w-full", triggerClassName, className)}>
        <SelectValue placeholder={isLoading && options.length === 0 ? "Carregando..." : placeholder}>
          {selectedLabel}
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {isLoading && options.length === 0 ? (
          <SelectItem value="__pmotivos_cancel_loading" disabled>
            Carregando motivos...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__pmotivos_cancel_empty" disabled>
            {emptyMessage}
          </SelectItem>
        ) : null}
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
