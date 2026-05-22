"use client";

import { CheckIcon, ChevronsUpDownIcon } from "lucide-react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { FormControl } from "@/components/ui/form";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { POCORRENCIA_ANDAMENTO_LIST_QUERY } from "@/packages/administrativo/data/POcorrenciaAndamento/pocorrenciaAndamentoDataConfig";
import {
  ocorrenciaAndamentoLabel,
  ocorrenciaAndamentoSearchValue,
} from "@/packages/administrativo/components/POcorrenciaAndamento/pocorrenciaAndamentoLabelUtils";
import { usePOcorrenciaAndamentoReadHook } from "@/packages/administrativo/hooks/POcorrenciaAndamento/usePOcorrenciaAndamentoReadHook";
import POcorrenciaAndamentoSelectInterface from "@/packages/administrativo/interfaces/POcorrenciaAndamento/POcorrenciaAndamentoSelectInterface";
import { comboboxSearchFilter } from "@/shared/actions/text/comboboxSearchFilter";
import { cn } from "@/lib/utils";

export default function POcorrenciaAndamentoSelect({
  field,
  disabled = false,
  placeholder = "Selecione a ocorrência de andamento",
}: POcorrenciaAndamentoSelectInterface) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const didLoadRef = useRef(false);

  const { ocorrenciasAndamento, fetchOcorrenciasAndamento } = usePOcorrenciaAndamentoReadHook();

  const loadData = useCallback(async () => {
    if (didLoadRef.current) return;
    didLoadRef.current = true;
    try {
      setIsLoading(true);
      await fetchOcorrenciasAndamento(POCORRENCIA_ANDAMENTO_LIST_QUERY);
    } finally {
      setIsLoading(false);
    }
  }, [fetchOcorrenciasAndamento]);

  useEffect(() => {
    if (!ocorrenciasAndamento.length) {
      void loadData();
    }
  }, [ocorrenciasAndamento.length, loadData]);

  const selected = useMemo(() => {
    if (!field?.value) return null;
    const id = String(field.value);
    return ocorrenciasAndamento.find((item) => String(item.ocorrencia_andamento_id) === id) ?? null;
  }, [ocorrenciasAndamento, field?.value]);

  function handleSelect(ocorrenciaAndamentoId: string) {
    if (disabled) return;
    field?.onChange?.(ocorrenciaAndamentoId);
    setOpen(false);
  }

  return (
    <Popover
      open={disabled ? false : open}
      onOpenChange={(nextOpen) => {
        if (disabled) return;
        setOpen(nextOpen);
      }}
    >
      <PopoverTrigger asChild>
        <FormControl className="w-full">
          <Button
            type="button"
            variant="outline"
            role="combobox"
            aria-expanded={open}
            disabled={isLoading || disabled}
            className={cn("w-full justify-between font-normal", !disabled && "cursor-pointer")}
          >
            {isLoading
              ? "Carregando..."
              : selected
                ? ocorrenciaAndamentoLabel(selected)
                : placeholder}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>
      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command filter={comboboxSearchFilter}>
          <CommandInput placeholder="Buscar por código ou descrição..." disabled={isLoading || disabled} />
          <CommandList>
            <CommandEmpty>
              {isLoading ? "Carregando..." : "Nenhum resultado encontrado."}
            </CommandEmpty>
            <CommandGroup>
              {ocorrenciasAndamento.map((item) => (
                <CommandItem
                  key={item.ocorrencia_andamento_id}
                  value={ocorrenciaAndamentoSearchValue(item)}
                  className={cn(!disabled && "cursor-pointer")}
                  disabled={disabled}
                  onSelect={() => handleSelect(String(item.ocorrencia_andamento_id))}
                >
                  <CheckIcon
                    className={cn(
                      "mr-2 h-4 w-4",
                      String(item.ocorrencia_andamento_id) === String(field?.value ?? "")
                        ? "opacity-100"
                        : "opacity-0",
                    )}
                  />
                  {ocorrenciaAndamentoLabel(item)}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
