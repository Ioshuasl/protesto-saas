"use client";

import { Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  PMOTIVOS_FILTER_ALL,
  type PMotivosFilterState,
} from "@/packages/administrativo/components/PMotivos/pmotivosFilterUtils";
import { useHydrated } from "@/shared/hooks/useHydrated";

const SITUACAO_LABELS: Record<string, string> = {
  [PMOTIVOS_FILTER_ALL]: "Todos",
  A: "Ativo",
  I: "Inativo",
};

interface PMotivosFilterProps {
  value: PMotivosFilterState;
  onChange: (value: PMotivosFilterState) => void;
}

export function PMotivosFilter({ value, onChange }: PMotivosFilterProps) {
  const hydrated = useHydrated();
  const update = (patch: Partial<PMotivosFilterState>) => onChange({ ...value, ...patch });

  return (
    <div className="flex w-full flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" strokeWidth={1.5} />
        <Input
          type="search"
          placeholder="Buscar por código ou descrição..."
          className="pl-8"
          value={value.search}
          onChange={(e) => update({ search: e.target.value })}
        />
      </div>

      {hydrated ? (
        <Select value={value.situacao} onValueChange={(situacao) => update({ situacao })}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Situação" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={PMOTIVOS_FILTER_ALL}>Todos</SelectItem>
            <SelectItem value="A">Ativo</SelectItem>
            <SelectItem value="I">Inativo</SelectItem>
          </SelectContent>
        </Select>
      ) : (
        <Button
          type="button"
          variant="outline"
          disabled
          className="w-full justify-between font-normal sm:w-[180px]"
        >
          {SITUACAO_LABELS[value.situacao] ?? "Situação"}
        </Button>
      )}
    </div>
  );
}
