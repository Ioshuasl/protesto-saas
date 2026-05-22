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
import { GCidadeSelectObject } from "@/packages/administrativo/components/GCidade/GCidadeSelectObject";
import { GUFSelectObject } from "@/packages/administrativo/components/GUF/GUFSelectObject";
import {
  PPESSOA_FILTER_ALL,
  type PPessoaFilterState,
  type PPessoaTipoPessoaFilter,
} from "@/packages/administrativo/components/PPessoa/ppessoaFilterUtils";
import { useHydrated } from "@/shared/hooks/useHydrated";

const TIPO_PESSOA_LABELS: Record<PPessoaTipoPessoaFilter, string> = {
  [PPESSOA_FILTER_ALL]: "Todos os tipos",
  F: "Pessoa física (CPF)",
  J: "Pessoa jurídica (CNPJ)",
};

const SEARCH_PLACEHOLDER: Record<PPessoaTipoPessoaFilter, string> = {
  [PPESSOA_FILTER_ALL]: "Buscar por nome, CPF, CNPJ ou telefone...",
  F: "Buscar por nome, CPF ou telefone...",
  J: "Buscar por nome, CNPJ ou telefone...",
};

interface PPessoaFilterProps {
  value: PPessoaFilterState;
  onChange: (value: PPessoaFilterState) => void;
}

export function PPessoaFilter({ value, onChange }: PPessoaFilterProps) {
  const hydrated = useHydrated();
  const update = (patch: Partial<PPessoaFilterState>) => onChange({ ...value, ...patch });

  return (
    <div className="flex w-full flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
      <div className="relative w-full max-w-sm">
        <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
        <Input
          type="search"
          placeholder={SEARCH_PLACEHOLDER[value.tipo_pessoa]}
          className="pl-8"
          value={value.search}
          onChange={(e) => update({ search: e.target.value })}
        />
      </div>

      {hydrated ? (
        <Select
          value={value.tipo_pessoa}
          onValueChange={(tipo_pessoa) =>
            update({ tipo_pessoa: tipo_pessoa as PPessoaTipoPessoaFilter })
          }
        >
          <SelectTrigger className="w-full sm:w-[220px]">
            <SelectValue placeholder="Tipo de pessoa" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={PPESSOA_FILTER_ALL}>
              {TIPO_PESSOA_LABELS[PPESSOA_FILTER_ALL]}
            </SelectItem>
            <SelectItem value="F">{TIPO_PESSOA_LABELS.F}</SelectItem>
            <SelectItem value="J">{TIPO_PESSOA_LABELS.J}</SelectItem>
          </SelectContent>
        </Select>
      ) : (
        <Button
          type="button"
          variant="outline"
          disabled
          className="w-full justify-between font-normal sm:w-[220px]"
        >
          {TIPO_PESSOA_LABELS[value.tipo_pessoa]}
        </Button>
      )}

      {hydrated ? (
        <GUFSelectObject
          className="w-full sm:w-[200px]"
          value={value.uf ?? ""}
          onValueChange={(ufNova) => {
            const uf = ufNova.trim().toUpperCase() || undefined;
            const ufAnterior = value.uf?.trim().toUpperCase();
            update({
              uf,
              ...(ufAnterior && ufAnterior !== uf ? { cidade: undefined } : {}),
            });
          }}
          placeholder="UF"
        />
      ) : (
        <Button
          type="button"
          variant="outline"
          disabled
          className="w-full justify-between font-normal sm:w-[200px]"
        >
          {value.uf ?? "UF"}
        </Button>
      )}

      {hydrated ? (
        <GCidadeSelectObject
          className="w-full sm:w-[240px]"
          value={value.cidade ?? ""}
          onValueChange={(cidade) =>
            update({ cidade: cidade.trim() || undefined })
          }
          uf={value.uf}
          placeholder="Cidade"
        />
      ) : (
        <Button
          type="button"
          variant="outline"
          disabled
          className="w-full justify-between font-normal sm:w-[240px]"
        >
          {value.cidade ?? "Cidade"}
        </Button>
      )}
    </div>
  );
}
