'use client';

import React from 'react';
import { Control, FieldValues, Path } from 'react-hook-form';

import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form';
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select';

interface PessoaTipoSelectProps<T extends FieldValues> {
  control: Control<T>;
  name: Path<T>;
  label?: string;
  disabled?: boolean;
  placeholder?: string;
}

export function TipoPessoaSelect<T extends FieldValues>({
  control,
  name,
  label = 'Pessoa',
  disabled = false,
  placeholder = 'Selecione uma opção',
}: PessoaTipoSelectProps<T>) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className="w-full">
          {label && <FormLabel>{label}</FormLabel>}
          <Select value={field.value} onValueChange={field.onChange} disabled={disabled}>
            <FormControl className="w-full">
              <SelectTrigger className="w-full cursor-pointer">
                <SelectValue placeholder={placeholder} />
              </SelectTrigger>
            </FormControl>
            <SelectContent>
              <SelectItem value="F" className="cursor-pointer">
                Física
              </SelectItem>
              <SelectItem value="J" className="cursor-pointer">
                Jurídica
              </SelectItem>
            </SelectContent>
          </Select>
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
