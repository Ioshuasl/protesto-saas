'use client';

import { Search } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  GFERIADO_FILTER_ALL,
  type GFeriadoFilterState,
} from '@/packages/administrativo/components/GFeriado/gFeriadoFilterUtils';
import { useHydrated } from '@/shared/hooks/useHydrated';

const TIPO_LABELS: Record<string, string> = {
  [GFERIADO_FILTER_ALL]: 'Todos os tipos',
  F: 'Fixo',
  V: 'Variável',
};

const SITUACAO_LABELS: Record<string, string> = {
  [GFERIADO_FILTER_ALL]: 'Todas as situações',
  A: 'Ativo',
  I: 'Inativo',
};

interface GFeriadoFilterProps {
  value: GFeriadoFilterState;
  onChange: (value: GFeriadoFilterState) => void;
}

export function GFeriadoFilter({ value, onChange }: GFeriadoFilterProps) {
  const hydrated = useHydrated();
  const update = (patch: Partial<GFeriadoFilterState>) => onChange({ ...value, ...patch });

  return (
    <div className="flex w-full flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input
          type="search"
          placeholder="Buscar por descrição ou ano..."
          className="pl-8"
          value={value.search}
          onChange={(e) => update({ search: e.target.value })}
        />
      </div>

      {hydrated ? (
        <Select value={value.tipo} onValueChange={(tipo) => update({ tipo })}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Tipo" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={GFERIADO_FILTER_ALL}>Todos os tipos</SelectItem>
            <SelectItem value="F">Fixo</SelectItem>
            <SelectItem value="V">Variável</SelectItem>
          </SelectContent>
        </Select>
      ) : (
        <Button
          type="button"
          variant="outline"
          disabled
          className="w-full justify-between font-normal sm:w-[180px]"
        >
          {TIPO_LABELS[value.tipo] ?? 'Tipo'}
        </Button>
      )}

      {hydrated ? (
        <Select value={value.situacao} onValueChange={(situacao) => update({ situacao })}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Situação" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={GFERIADO_FILTER_ALL}>Todas as situações</SelectItem>
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
          {SITUACAO_LABELS[value.situacao] ?? 'Situação'}
        </Button>
      )}
    </div>
  );
}
