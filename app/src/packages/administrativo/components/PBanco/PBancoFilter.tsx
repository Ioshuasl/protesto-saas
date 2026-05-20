"use client";

import { Input } from "@/components/ui/input";
import { Search } from "lucide-react";

interface PBancoFilterProps {
  value: string;
  onChange: (value: string) => void;
}

export function PBancoFilter({ value, onChange }: PBancoFilterProps) {
  return (
    <div className="relative w-full max-w-sm">
      <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
      <Input
        type="search"
        placeholder="Buscar por código ou descrição..."
        className="pl-8"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
