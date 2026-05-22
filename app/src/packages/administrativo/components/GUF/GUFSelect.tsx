'use client';

import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

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
import { useGUfReadHook } from '@/packages/administrativo/hooks/GUF/useGUfReadHook';
import GUFSelectInterface from '@/packages/administrativo/interfaces/GUF/GUFSelectInterface';

export default function GUFSelect({ field, disable = false }: GUFSelectInterface) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { gUf, fetchGUf } = useGUfReadHook();
  const didLoadRef = useRef(false);

  const loadData = useCallback(async () => {
    if (didLoadRef.current) return;
    didLoadRef.current = true;

    try {
      setIsLoading(true);
      await fetchGUf();
    } finally {
      setIsLoading(false);
    }
  }, [fetchGUf]);

  useEffect(() => {
    if (gUf?.length) {
      didLoadRef.current = true;
      return;
    }
    void loadData();
  }, [gUf?.length, loadData]);

  const selected = useMemo(() => {
    if (!gUf || !field?.value) return null;

    return gUf.find((item) => item.sigla?.toUpperCase() === String(field.value).toUpperCase());
  }, [gUf, field?.value]);

  function handleSelect(sigla: string) {
    if (disable) return;
    field?.onChange?.(sigla);
    setOpen(false);
  }

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
            {isLoading ? 'Carregando...' : selected ? selected.sigla.toUpperCase() : 'Selecione...'}
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
              {gUf?.map((item) => (
                <CommandItem
                  className={cn(!disable && 'cursor-pointer')}
                  disabled={disable}
                  key={item.g_uf_id}
                  value={item.sigla?.toLowerCase() ?? ''}
                  onSelect={() => handleSelect(item.sigla)}
                >
                  <CheckIcon
                    className={cn(
                      'mr-2 h-4 w-4',
                      item.sigla?.toUpperCase() === String(field?.value ?? '').toUpperCase()
                        ? 'opacity-100'
                        : 'opacity-0',
                    )}
                  />
                  {item.sigla?.toUpperCase() ?? ''}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
