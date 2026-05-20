"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { usePLivroNaturezaReadHook } from "@/packages/administrativo/hooks/PLivroNatureza/usePLivroNaturezaReadHook";
import { cn } from "@/lib/utils";

export interface PLivroNaturezaSelectObjectProps {
  value?: string;
  onValueChange?: (livroNaturezaId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

function naturezaLabel(n: { livro_natureza_id: number; descricao?: string }) {
  return n.descricao?.trim() || `Natureza ${n.livro_natureza_id}`;
}

export function PLivroNaturezaSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione a natureza",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhuma natureza disponível",
}: PLivroNaturezaSelectObjectProps) {
  const { naturezas, isLoading, fetchNaturezas } = usePLivroNaturezaReadHook();

  useEffect(() => {
    void fetchNaturezas();
  }, [fetchNaturezas]);

  const options = useMemo(
    () =>
      naturezas.map((n) => ({
        value: String(n.livro_natureza_id),
        label: naturezaLabel(n),
      })),
    [naturezas],
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
          <SelectItem value="__plivro_natureza_loading" disabled>
            Carregando naturezas...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__plivro_natureza_empty" disabled>
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
