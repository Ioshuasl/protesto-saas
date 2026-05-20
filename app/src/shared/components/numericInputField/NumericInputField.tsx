'use client';

import React from 'react';
import { Control, FieldValues, Path } from 'react-hook-form';

import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';

interface NumericInputFieldProps<T extends FieldValues> {
  control: Control<T>;
  name: Path<T>;
  label?: string;
  placeholder?: string;
  disabled?: boolean;
  min?: number;
  max?: number;
}

export function NumericInputField<T extends FieldValues>({
  control,
  name,
  label = 'Número',
  placeholder = 'Digite um número',
  disabled = false,
  min,
  max,
}: NumericInputFieldProps<T>) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className="w-full">
          {label && <FormLabel>{label}</FormLabel>}

          <FormControl>
            <Input
              {...field}
              type="text"
              disabled={disabled}
              value={field.value ?? ''}
              placeholder={placeholder}
              inputMode="numeric"
              pattern="[0-9]*"
              onChange={(e) => {
                // Mantém apenas números
                let value = e.target.value.replace(/[^0-9]/g, '');

                // Limita faixa, se definido
                if (min !== undefined && Number(value) < min) value = String(min);
                if (max !== undefined && Number(value) > max) value = String(max);

                field.onChange(value);
              }}
            />
          </FormControl>

          <FormMessage />
        </FormItem>
      )}
    />
  );
}
