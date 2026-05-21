"use client";

import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";
import type { PBancoFilterState } from "@/packages/administrativo/components/PBanco/pBancoFilterUtils";

interface PBancoFilterProps {
  value: PBancoFilterState;
  onChange: (value: PBancoFilterState) => void;
}

export function PBancoFilter({ value, onChange }: PBancoFilterProps) {
  return (
    <div className="relative w-full max-w-md">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Buscar por código ou descrição..."
        className="pl-8"
        value={value.search}
        onChange={(e) => onChange({ search: e.target.value })}
      />
    </div>
  );
}
