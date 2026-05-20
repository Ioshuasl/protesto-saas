"use client";

import { useEffect, useMemo } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";
import { cn } from "@/lib/utils";

export interface GUsuarioSelectObjectProps {
  value?: string;
  onValueChange?: (usuarioId: string) => void;
  placeholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

function usuarioLabel(u: { usuario_id: number; nome_completo?: string; login?: string }) {
  return u.nome_completo?.trim() || u.login?.trim() || `Usuário ${u.usuario_id}`;
}

export function GUsuarioSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o usuário",
  disabled,
  className,
  triggerClassName,
  emptyMessage = "Nenhum usuário disponível",
}: GUsuarioSelectObjectProps) {
  const { usuarios, isLoading, fetchUsuarios } = useGUsuarioReadHook();

  useEffect(() => {
    void fetchUsuarios();
  }, [fetchUsuarios]);

  const options = useMemo(
    () =>
      usuarios.map((u) => ({
        value: String(u.usuario_id),
        label: usuarioLabel(u),
      })),
    [usuarios],
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
          <SelectItem value="__gusuario_loading" disabled>
            Carregando usuários...
          </SelectItem>
        ) : null}
        {!isLoading && options.length === 0 ? (
          <SelectItem value="__gusuario_empty" disabled>
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
