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
import { Sexo } from '@/shared/enums/SexoEnum';

type SexoSelectProps = {
  field: {
    value?: string | null;
    onChange: (value: string) => void;
  };
};

export default function SexoSelect({ field }: SexoSelectProps) {
  const [open, setOpen] = React.useState(false);

  // Cria as opções a partir do enum
  const options = Object.entries(Sexo).map(([key, label]) => ({
    value: key, // 'M' | 'F'
    label, // 'Masculino' | 'Feminino'
  }));

  // Label exibida atualmente
  const selectedLabel =
    field.value !== undefined && field.value !== null && field.value !== ''
      ? options.find((item) => item.value === String(field.value))?.label
      : 'Selecione...';

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <FormControl className="w-full">
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between cursor-pointer"
          >
            {selectedLabel}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>
      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Buscar sexo..." />
          <CommandList>
            <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>
            <CommandGroup>
              {options.map((item) => (
                <CommandItem
                  className='cursor-pointer'
                  key={item.value}
                  value={item.label.toLowerCase()}
                  onSelect={() => {
                    field.onChange(item.value); // envia 'M' | 'F'
                    setOpen(false);
                  }}
                >
                  <CheckIcon
                    className={cn(
                      'mr-2 h-4 w-4',
                      String(field.value) === item.value ? 'opacity-100' : 'opacity-0',
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
