"use client";

import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import type { PEspecieFilterState } from "@/packages/administrativo/components/PEspecie/pEspecieFilterUtils";

interface PEspecieFilterProps {
  value: PEspecieFilterState;
  onChange: (value: PEspecieFilterState) => void;
}

export function PEspecieFilter({ value, onChange }: PEspecieFilterProps) {
  return (
    <div className="relative w-full max-w-md">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Buscar por sigla ou descrição..."
        className="pl-8"
        value={value.search}
        onChange={(e) => onChange({ search: e.target.value })}
      />
    </div>
  );
}
