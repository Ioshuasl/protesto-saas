'use client';

import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { CalendarIcon } from 'lucide-react';
import * as React from 'react';
import type { Locale } from 'react-day-picker';

import { Button } from '@/components/ui/button';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';

export type DatePickerProps = {
  value?: Date;
  onChange?: (date: Date | undefined) => void;
  placeholder?: string;
  disabled?: boolean;
  calendarDisabled?: React.ComponentProps<typeof Calendar>['disabled'];
  className?: string;
  triggerClassName?: string;
  todayLabel?: string;
  showTodayButton?: boolean;
  align?: React.ComponentProps<typeof PopoverContent>['align'];
  locale?: Partial<Locale>;
  dateFormat?: string;
  /** Fecha o popover ao selecionar uma data (padrão: true). */
  closeOnSelect?: boolean;
};

export function DatePicker({
  value,
  onChange,
  placeholder = 'Selecione uma data',
  disabled,
  calendarDisabled,
  className,
  triggerClassName,
  todayLabel,
  showTodayButton,
  align = 'start',
  locale = ptBR,
  dateFormat = 'PPP',
  closeOnSelect = true,
}: DatePickerProps) {
  const [open, setOpen] = React.useState(false);

  const handleSelect: React.ComponentProps<typeof Calendar>['onSelect'] = (date) => {
    onChange?.(date);
    if (closeOnSelect && date) {
      setOpen(false);
    }
  };

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          type="button"
          variant="outline"
          disabled={disabled}
          className={cn(
            'w-full justify-start pl-3 text-left font-normal',
            !value && 'text-muted-foreground',
            triggerClassName,
            className,
          )}
        >
          {value ? format(value, dateFormat, { locale }) : <span>{placeholder}</span>}
          <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align={align}>
        <Calendar
          mode="single"
          selected={value}
          onSelect={handleSelect}
          disabled={calendarDisabled}
          locale={locale}
          todayLabel={todayLabel}
          showTodayButton={showTodayButton}
          initialFocus
        />
      </PopoverContent>
    </Popover>
  );
}
