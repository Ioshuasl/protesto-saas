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
import { TipoAquisicaoEnum } from '@/shared/enums/TipoAquisicaoEnum';

import TipoAquisicaoSelectInterface from './interface/TipoAquisicaoSelectInterface';

export default function TipoAquisicaoSelect({ field }: TipoAquisicaoSelectInterface) {
  const selectedLabel = field.value
    ? TipoAquisicaoEnum[field.value as keyof typeof TipoAquisicaoEnum]
    : 'Selecione';

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-full justify-between overflow-hidden cursor-pointer"
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
              {Object.entries(TipoAquisicaoEnum).map(([key, label]) => {
                const keyNumber = Number(key);

                return (
                  <CommandItem
                    key={key}
                    value={label}
                    onSelect={() => field.onChange(keyNumber)}
                    className="flex items-start gap-2 cursor-pointer"
                  >
                    <CheckIcon
                      className={cn(
                        'mt-0.5 h-4 w-4 shrink-0',
                        field.value === keyNumber ? 'opacity-100' : 'opacity-0',
                      )}
                    />

                    {/* POPOVER: quebra de linha liberada */}
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
