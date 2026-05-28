"use client";

import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";

interface PTemplateFilterProps {
  value: string;
  onChange: (value: string) => void;
}

export function PTemplateFilter({ value, onChange }: PTemplateFilterProps) {
  return (
    <div className="relative w-full max-w-md">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Buscar por descrição..."
        className="pl-8"
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </div>
  );
}
