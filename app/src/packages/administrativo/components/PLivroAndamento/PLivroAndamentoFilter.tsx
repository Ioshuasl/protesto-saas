"use client";

import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import type { PLivroAndamentoFilterState } from "@/packages/administrativo/components/PLivroAndamento/pLivroAndamentoFilterUtils";

interface PLivroAndamentoFilterProps {
  value: PLivroAndamentoFilterState;
  onChange: (value: PLivroAndamentoFilterState) => void;
}

export function PLivroAndamentoFilter({ value, onChange }: PLivroAndamentoFilterProps) {
  return (
    <div className="relative w-full max-w-md">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Buscar por número do livro ou sigla..."
        className="pl-8"
        value={value.search}
        onChange={(e) => onChange({ search: e.target.value })}
      />
    </div>
  );
}
