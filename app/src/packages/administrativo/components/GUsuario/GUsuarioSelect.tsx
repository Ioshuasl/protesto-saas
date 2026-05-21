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
import { useGUsuarioIndexHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioIndexHook';
import GUsuarioIndexInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioIndexInterface';
import GUsuarioSelectInterface from '@/packages/administrativo/interfaces/GUsuario/GUsuarioSelectInterface';
import GetCapitalize from '@/shared/actions/text/GetCapitalize';

export default function GUsuarioSelect({ field }: GUsuarioSelectInterface) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { GUsuario, indexGUsuario } = useGUsuarioIndexHook();

  // evita múltiplas execuções em StrictMode / re-render
  const didLoadRef = useRef(false);

  const loadData = useCallback(async () => {
    if (didLoadRef.current) return;

    didLoadRef.current = true;

    const urlParams = { assina: 'S', situacao: 'A' };
    const GUsuarioIndex: GUsuarioIndexInterface = { urlParams };

    try {
      setIsLoading(true);
      await indexGUsuario(GUsuarioIndex);
    } finally {
      setIsLoading(false);
    }
  }, [indexGUsuario]);

  useEffect(() => {
    if (!GUsuario || GUsuario.length === 0) {
      loadData();
    }
  }, [GUsuario?.length, loadData]);

  const selected = useMemo(() => {
    if (!GUsuario || !field?.value) return null;
    return GUsuario.find((b) => String(b.usuario_id) === String(field.value));
  }, [GUsuario, field?.value]);

  const handleSelect = useCallback(
    (usuarioId: string | number) => {
      if (!field?.onChange) return;
      field.onChange(usuarioId);
      setOpen(false);
    },
    [field?.onChange],
  );

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <FormControl className="w-full">
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            disabled={isLoading}
            className="w-full justify-between cursor-pointer"
          >
            {isLoading
              ? 'Carregando...'
              : selected
                ? GetCapitalize(selected.nome_completo)
                : 'Selecione...'}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>

      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command className="w-full">
          <CommandInput placeholder="Busca..." disabled={isLoading} className="w-full" />
          <CommandList className="w-full">
            <CommandEmpty>
              {isLoading ? 'Carregando...' : 'Nenhum resultado encontrado.'}
            </CommandEmpty>

            <CommandGroup className="w-full">
              {GUsuario?.map((item) => (
                <CommandItem
                  key={item.usuario_id}
                  value={item?.nome_completo?.toLowerCase() ?? ''}
                  onSelect={() => handleSelect(item.usuario_id)}
                  className="w-full cursor-pointer"
                >
                  <CheckIcon
                    className={cn(
                      'mr-2 h-4 w-4',
                      String(field?.value ?? '') === String(item.usuario_id)
                        ? 'opacity-100'
                        : 'opacity-0',
                    )}
                  />
                  {GetCapitalize(item.nome_completo ?? '')}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
