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
import { TipoDeAssinaturaEnum, TipoDeAssinaturaKey } from '@/shared/enums/TipoDeAssinaturaEnum';

import TipoDeAssinaturaSelectInterface from './interface/TipoDeAssinaturaSelectInterface';

export default function TipoDeAssinaturaSelect({ field }: TipoDeAssinaturaSelectInterface) {
  const [open, setOpen] = React.useState(false);

  const options = Object.entries(TipoDeAssinaturaEnum).map(([key, label]) => ({
    value: key as TipoDeAssinaturaKey, // ✅ string "1" | "2" | ...
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
            className="justify-between cursor-pointer"
          >
            {selected ? selected.label : 'Selecione...'}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>

      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Buscar tipo de assinatura..." />
          <CommandList>
            <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>

            <CommandGroup>
              {options.map((item) => {
                const isSelected = field.value === item.value;

                return (
                  <CommandItem
                    className='cursor-pointer'
                    key={item.value}
                    value={item.label.toLowerCase()}
                    onSelect={() => {
                      field.onChange(item.value);
                      setOpen(false);
                    }}
                  >
                    <CheckIcon
                      className={cn('mr-2 h-4 w-4', isSelected ? 'opacity-100' : 'opacity-0')}
                    />
                    {item.label}
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
