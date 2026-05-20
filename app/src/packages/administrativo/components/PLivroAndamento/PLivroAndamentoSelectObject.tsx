"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePLivroAndamentoReadHook } from "@/packages/administrativo/hooks/PLivroAndamento/usePLivroAndamentoReadHook";
import { cn } from "@/lib/utils";

export interface PLivroAndamentoSelectObjectProps {
  value?: string;
  onValueChange?: (livroAndamentoId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

function livroLabel(m: {
  livro_andamento_id: number;
  numero_livro?: number;
  sigla?: string;
}) {
  const num = m.numero_livro != null ? String(m.numero_livro) : "-";
  const extra = m.sigla?.trim() ? ` — ${m.sigla}` : "";
  return `Livro ${num}${extra}`;
}

export function PLivroAndamentoSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o livro",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum livro em andamento disponível",
}: PLivroAndamentoSelectObjectProps) {
  const { livrosAndamento, isLoading, fetchLivrosAndamento } = usePLivroAndamentoReadHook();

  useEffect(() => {
    void fetchLivrosAndamento();
  }, [fetchLivrosAndamento]);

  const options = useMemo(
    () =>
      livrosAndamento.map((m) => ({
        value: String(m.livro_andamento_id),
        label: livroLabel(m),
      })),
    [livrosAndamento],
  );

  const selectedLabel = useMemo(
    () => options.find((o) => o.value === (value ?? ""))?.label,
    [options, value],
  );

  return (
    <Select
      value={value && value.length > 0 ? value : undefined}
      onValueChange={onValueChange}
      disabled={disabled || isLoading}
    >
      <SelectTrigger className={cn("w-full", triggerClassName, className)}>
        <SelectValue placeholder={isLoading && options.length === 0 ? "Carregando..." : placeholder}>
          {selectedLabel}
        </SelectValue>
      </SelectTrigger>
      <SelectContent>
        {isLoading && options.length === 0 ? (
          <SelectItem value="__plivro_loading" disabled>
            Carregando livros...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__plivro_empty" disabled>
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
