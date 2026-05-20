'use client';

import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react';

import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { GrupoTipoEnum } from '@/shared/enums/GrupoTipoEnum';

import GrupoTipoSelectInterface from './interface/GrupoTipoSelectInterface';

export default function GrupoTipoSelect({ field }: GrupoTipoSelectInterface) {
  const selectedLabel = field.value
    ? GrupoTipoEnum[field.value as keyof typeof GrupoTipoEnum]
    : 'Selecione';
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-full justify-between overflow-hidden"
        >
          {/* TRIGGER: sempre truncado */}
          <span className="max-w-full truncate overflow-hidden text-ellipsis whitespace-nowrap">
            {selectedLabel}
          </span>
          <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Buscar tipo..." className="w-full" />
          <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>
          <CommandGroup>
            <CommandList>
              {Object.entries(GrupoTipoEnum).map(([key, label]) => {
                return (
                  <CommandItem
                    key={key}
                    value={key}
                    onSelect={() => field.onChange(key)}
                    className="flex items-start gap-2"
                  >
                    <CheckIcon
                      className={cn(
                        'mt-0.5 h-4 w-4 shrink-0',
                        field.value === key ? 'opacity-100' : 'opacity-0',
                      )}
                    />
                    <span className="leading-snug break-words whitespace-normal">{label}</span>
                  </CommandItem>
                );
              })}
            </CommandList>
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
