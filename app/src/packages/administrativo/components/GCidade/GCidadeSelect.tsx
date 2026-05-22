'use client';

import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react';
import { useEffect, useMemo, useRef, useState } from 'react';

import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import { FormControl } from '@/components/ui/form';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { useGCidadeReadHook } from '@/packages/administrativo/hooks/GCidade/useGCidadeReadHook';
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import GCidadeSelectInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeSelectInterface';

export default function GCidadeSelect({ field, uf, disable = false }: GCidadeSelectInterface) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const lastUfRef = useRef<string | null>(null);

  const { gCidade, fetchGCidade } = useGCidadeReadHook();

  const selected = useMemo(() => {
    if (!gCidade || !field?.value) return null;
    return gCidade.find((item) => item.cidade_nome == field.value);
  }, [gCidade, field?.value]);

  function handleSelect(cidade_nome: string) {
    if (disable) return;
    field?.onChange?.(cidade_nome);
    setOpen(false);
  }

  useEffect(() => {
    const normalizedUf = String(uf ?? '')
      .trim()
      .toUpperCase();

    if (!normalizedUf || lastUfRef.current === normalizedUf) {
      return;
    }

    lastUfRef.current = normalizedUf;
    const data: GCidadeInterface = { uf: normalizedUf };
    setIsLoading(true);
    fetchGCidade(data).finally(() => {
      setIsLoading(false);
    });
  }, [uf, fetchGCidade]);

  return (
    <Popover
      open={disable ? false : open}
      onOpenChange={(nextOpen) => {
        if (disable) return;
        setOpen(nextOpen);
      }}
    >
      <PopoverTrigger asChild>
        <FormControl className="w-full">
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            disabled={isLoading || disable}
            className={cn('w-full justify-between', !disable && 'cursor-pointer')}
          >
            {isLoading
              ? 'Carregando...'
              : selected
                ? selected.cidade_nome?.toUpperCase()
                : 'Selecione...'}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>
      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Busca..." disabled={isLoading || disable} />
          <CommandList>
            <CommandEmpty>
              {isLoading ? 'Carregando...' : 'Nenhum resultado encontrado.'}
            </CommandEmpty>
            <CommandGroup>
              {gCidade?.map((item) => (
                <CommandItem
                  className={cn(!disable && 'cursor-pointer')}
                  disabled={disable}
                  key={item.cidade_id}
                  value={String(item.cidade_nome)}
                  onSelect={() => handleSelect(String(item.cidade_nome))}
                >
                  <CheckIcon
                    className={cn(
                      'mr-2 h-4 w-4',
                      item.cidade_nome === field?.value ? 'opacity-100' : 'opacity-0',
                    )}
                  />
                  {item.cidade_nome?.toUpperCase() ?? ''}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
