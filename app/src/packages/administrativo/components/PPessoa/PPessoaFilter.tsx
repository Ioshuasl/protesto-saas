"use client";

import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

interface PPessoaFilterProps {
  value: string;
  onChange: (value: string) => void;
}

export function PPessoaFilter({ value, onChange }: PPessoaFilterProps) {
  return (
    <div className="relative w-full max-w-sm">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Buscar por Nome, CPF ou CNPJ..."
        className="pl-8"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
