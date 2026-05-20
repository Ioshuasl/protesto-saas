import { Command } from 'cmdk';
import { CheckIcon, ChevronsUpDownIcon } from 'lucide-react';
import React from 'react';

import { Button } from '@/components/ui/button';
import {
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import { FormControl } from '@/components/ui/form';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';
import { TipoNaturezaEnum } from '@/shared/enums/TipoNaturezaEnum';

export default function TipoNaturezaSelect({ field }: any) {
  const [open, setOpen] = React.useState(false);

  // Gera opções a partir do Enum
  const options = Object.entries(TipoNaturezaEnum).map(([id, label]) => ({
    value: Number(id),
    label,
  }));

  // 🔹 Converte valor recebido (string tipo ";0,1,2,3") para array de números
  const parseToArray = (value: any): number[] => {
    if (!value) return [];
    if (Array.isArray(value)) return value.map(Number);
    if (typeof value === 'string') {
      return value
        .replace(/^;/, '') // remove o primeiro ";"
        .split(',')
        .filter(Boolean)
        .map((v) => Number(v.trim()));
    }
    return [];
  };

  // Array de valores selecionados
  const selectedValues: number[] = parseToArray(field.value);

  // Atualiza valor selecionado (e reenvia como string ";0,1,2,3")
  const toggleSelect = (value: number) => {
    let newValues;
    if (selectedValues.includes(value)) {
      newValues = selectedValues.filter((v) => v !== value);
    } else {
      newValues = [...selectedValues, value];
    }
    // Converte para formato ";0,1,2,3"
    const formatted = ';' + newValues.join(',');
    field.onChange(formatted);
  };

  // Label do botão (nomes selecionados)
  const selectedLabels = options
    .filter((opt) => selectedValues.includes(opt.value))
    .map((opt) => opt.label)
    .join(', ');

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
            {selectedLabels || 'Selecione...'}
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </FormControl>
      </PopoverTrigger>

      <PopoverContent className="w-[var(--radix-popover-trigger-width)] p-0">
        <Command>
          <CommandInput placeholder="Buscar tipo natureza..." />
          <CommandList>
            <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>
            <CommandGroup>
              {options.map((item) => (
                <CommandItem
                  key={item.value}
                  value={item.label.toLowerCase()}
                  onSelect={() => toggleSelect(item.value)}
                >
                  <CheckIcon
                    className={cn(
                      'mr-2 h-4 w-4',
                      selectedValues.includes(item.value) ? 'opacity-100' : 'opacity-0',
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
