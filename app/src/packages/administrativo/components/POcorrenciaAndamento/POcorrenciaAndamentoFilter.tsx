"use client";

import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";
import type { POcorrenciaAndamentoFilterState } from "@/packages/administrativo/components/POcorrenciaAndamento/pocorrenciaAndamentoFilterUtils";

interface POcorrenciaAndamentoFilterProps {
  value: POcorrenciaAndamentoFilterState;
  onChange: (value: POcorrenciaAndamentoFilterState) => void;
}

export function POcorrenciaAndamentoFilter({ value, onChange }: POcorrenciaAndamentoFilterProps) {
  return (
    <div className="relative w-full max-w-md">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
      <Input
        type="search"
        placeholder="Buscar por descrição..."
        className="pl-8"
        value={value.search}
        onChange={(e) => onChange({ search: e.target.value })}
      />
    </div>
  );
}
