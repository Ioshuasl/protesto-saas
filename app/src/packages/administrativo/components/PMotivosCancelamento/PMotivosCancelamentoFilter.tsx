"use client";

import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

interface PMotivosCancelamentoFilterProps {
  value: string;
  onChange: (value: string) => void;
}

export function PMotivosCancelamentoFilter({ value, onChange }: PMotivosCancelamentoFilterProps) {
  return (
    <div className="relative w-full max-w-sm">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
      <Input
        type="search"
        placeholder="Buscar por descrição..."
        className="pl-8"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
