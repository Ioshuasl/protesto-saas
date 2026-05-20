'use client';

import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react';
import React from 'react';

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
import { TipoQualificaoImovelEnum } from '@/shared/enums/TipoQualificaoImovel';

import TipoQualificacaoImovelSelectInterface from './interface/TipoQualificacaoImovelSelectInterface';

export default function TipoQualificacaoImovelSelect({
  field,
}: TipoQualificacaoImovelSelectInterface) {
  const [open, setOpen] = React.useState(false);

  const options = Object.entries(TipoQualificaoImovelEnum).map(([key, label]) => ({
    value: Number(key),
    label,
  }));

  const selected = options.find((item) => item.value === field.value);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <FormControl className="w-full">
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between overflow-hidden cursor-pointer"
          >
            {/* TRIGGER: truncado, sem quebra */}
            <span className="max-w-full truncate overflow-hidden text-ellipsis whitespace-nowrap">
              {selected ? selected.label : 'Selecione...'}
            </span>

            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>

      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Buscar tipo de qualificação..." className="w-full" />

          <CommandList>
            <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>

            <CommandGroup>
              {options.map((item) => {
                const isSelected = field.value === item.value;

                return (
                  <CommandItem
                    key={item.value}
                    value={item.label.toLowerCase()}
                    onSelect={() => {
                      field.onChange(item.value);
                      setOpen(false);
                    }}
                    className="flex items-start gap-2 cursor-pointer"
                  >
                    <CheckIcon
                      className={cn(
                        'mt-0.5 h-4 w-4 shrink-0',
                        isSelected ? 'opacity-100' : 'opacity-0',
                      )}
                    />

                    {/* POPOVER: quebra de linha liberada */}
                    <span className="leading-snug break-words whitespace-normal">{item.label}</span>
                  </CommandItem>
                );
              })}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
