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
import { TipoCertidoesEnum } from '@/shared/enums/TipoCertidoesEnum';

import TiposCertidoesSelectInterface from './interfaces/TiposCertidoesSelectInterface';

export default function TiposCertidoesSelect({ field }: TiposCertidoesSelectInterface) {
  const [open, setOpen] = React.useState(false);

  const options = Object.entries(TipoCertidoesEnum).map(([key, label]) => ({
    value: Number(key),
    label,
  }));

  // Label exibida atualmente
  const selectedLabel =
    field.value !== undefined && field.value !== null
      ? options.find((item) => item.value === Number(field.value))?.label
      : 'Selecione...';

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <FormControl className="w-full">
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="justify-between"
          >
            {selectedLabel}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>
      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Buscar tipo de parte..." />
          <CommandList>
            <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>
            <CommandGroup>
              {options.map((item) => (
                <CommandItem
                  key={item.value}
                  value={item.label.toLowerCase()}
                  onSelect={() => {
                    field.onChange(item.value); // envia número
                    setOpen(false);
                  }}
                >
                  <CheckIcon
                    className={cn(
                      'mr-2 h-4 w-4',
                      Number(field.value) === item.value ? 'opacity-100' : 'opacity-0',
                    )}
                  />
                  {item.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
