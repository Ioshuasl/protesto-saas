"use client";

import { useEffect, useMemo } from "react";
import {
  SearchComboboxSelect,
} from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import { buildSearchComboboxOptions } from "@/packages/administrativo/components/shared/buildSearchComboboxOptions";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";

export interface GUsuarioSelectObjectProps {
  value?: string;
  onValueChange?: (usuarioId: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  emptyMessage?: string;
}

export function usuarioLabel(u: {
  usuario_id: number;
  nome_completo?: string;
  login?: string;
}) {
  return u.nome_completo?.trim() || u.login?.trim() || `Usuário ${u.usuario_id}`;
}

function usuarioSearchValue(u: {
  usuario_id: number;
  nome_completo?: string;
  login?: string;
}) {
  const label = usuarioLabel(u);
  const parts = [u.nome_completo, u.login, label, String(u.usuario_id)];
  return parts
    .map((part) => String(part ?? "").trim())
    .filter(Boolean)
    .join(" ");
}

export function GUsuarioSelectObject({
  value,
  onValueChange,
  placeholder = "Selecione o usuário",
  searchPlaceholder = "Buscar usuário (nome ou login)...",
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
      buildSearchComboboxOptions({
        fromFetch: usuarios.map((u) => ({
          value: String(u.usuario_id),
          label: usuarioLabel(u),
          searchValue: usuarioSearchValue(u),
        })),
        value,
      }),
    [usuarios, value],
  );

  return (
    <SearchComboboxSelect
      value={value}
      onValueChange={onValueChange}
      options={options}
      isLoading={isLoading}
      placeholder={placeholder}
      searchPlaceholder={searchPlaceholder}
      disabled={disabled}
      className={className}
      triggerClassName={triggerClassName}
      emptyMessage={emptyMessage}
      loadingMessage="Carregando usuários..."
      clearAriaLabel="Limpar usuário"
    />
  );
}
