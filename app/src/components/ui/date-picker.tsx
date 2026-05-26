'use client';

import { format, type Locale as DateFnsLocale } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { CalendarIcon } from 'lucide-react';
import * as React from 'react';
import type { Locale } from 'react-day-picker';

import { Button } from '@/components/ui/button';
import { Calendar, type CalendarSize } from '@/components/ui/calendar';
import { DatePickerHybrid } from '@/components/ui/date-picker-hybrid';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { cn } from '@/lib/utils';

export type DatePickerVariant = 'popover' | 'inline' | 'hybrid';

export type DatePickerProps = {
  value?: Date;
  onChange?: (date: Date | undefined) => void;
  /**
   * - `popover`: botão que abre calendário
   * - `inline`: calendário fixo (dialogs)
   * - `hybrid`: input dd/mm/aaaa + ícone de calendário
   */
  variant?: DatePickerVariant;
  placeholder?: string;
  disabled?: boolean;
  calendarDisabled?: React.ComponentProps<typeof Calendar>['disabled'];
  calendarSize?: CalendarSize;
  showOutsideDays?: boolean;
  className?: string;
  /** Classes do input na variante `hybrid`. */
  inputClassName?: string;
  triggerClassName?: string;
  id?: string;
  name?: string;
  'aria-invalid'?: boolean;
  'aria-describedby'?: string;
  todayLabel?: string;
  showTodayButton?: boolean;
  align?: React.ComponentProps<typeof PopoverContent>['align'];
  side?: React.ComponentProps<typeof PopoverContent>['side'];
  sideOffset?: number;
  collisionPadding?: number;
  /** Evita conflito de foco com Dialog pai (padrão: true). */
  popoverModal?: boolean;
  locale?: Partial<Locale>;
  dateFormat?: string;
  /** Fecha o popover ao selecionar uma data (padrão: true). */
  closeOnSelect?: boolean;
};

export function DatePicker({
  value,
  onChange,
  variant = 'popover',
  placeholder = 'Selecione uma data',
  disabled,
  calendarDisabled,
  calendarSize = 'default',
  showOutsideDays = true,
  className,
  inputClassName,
  triggerClassName,
  id,
  name,
  'aria-invalid': ariaInvalid,
  'aria-describedby': ariaDescribedBy,
  todayLabel,
  showTodayButton,
  align = 'start',
  side = 'bottom',
  sideOffset = 8,
  collisionPadding = 16,
  popoverModal = true,
  locale = ptBR,
  dateFormat = 'PPP',
  closeOnSelect = true,
}: DatePickerProps) {
  const [open, setOpen] = React.useState(false);

  const handleSelect = (date: Date | undefined) => {
    onChange?.(date);
    if (closeOnSelect && date) {
      setOpen(false);
    }
  };

  const calendarProps = {
    mode: 'single' as const,
    selected: value,
    disabled: calendarDisabled,
    locale,
    todayLabel,
    showTodayButton: showTodayButton ?? false,
    size: calendarSize,
    showOutsideDays,
    hideWeekdays: true,
  };

  if (variant === 'hybrid') {
    return (
      <DatePickerHybrid
        value={value}
        onChange={onChange}
        placeholder={placeholder === 'Selecione uma data' ? 'dd/mm/aaaa' : placeholder}
        disabled={disabled}
        calendarDisabled={calendarDisabled}
        calendarSize={calendarSize}
        showOutsideDays={showOutsideDays}
        className={className}
        inputClassName={inputClassName}
        todayLabel={todayLabel}
        showTodayButton={showTodayButton ?? false}
        align={align}
        side={side}
        sideOffset={sideOffset}
        collisionPadding={collisionPadding}
        popoverModal={popoverModal}
        locale={locale}
        closeOnSelect={closeOnSelect}
        id={id}
        name={name}
        aria-invalid={ariaInvalid}
        aria-describedby={ariaDescribedBy}
      />
    );
  }

  if (variant === 'inline') {
    return (
      <div
        className={cn(
          'flex w-full justify-center rounded-xl bg-transparent',
          calendarSize === 'compact' ? 'p-0.5' : 'p-1',
          className,
        )}
      >
        <Calendar {...calendarProps} onSelect={onChange} />
      </div>
    );
  }

  return (
    <Popover open={open} onOpenChange={setOpen} modal={popoverModal}>
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
          {value ? format(value, dateFormat, { locale: locale as DateFnsLocale }) : <span>{placeholder}</span>}
          <CalendarIcon className="ml-auto h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="z-[100] w-auto border-0 bg-transparent p-0 shadow-none"
        align={align}
        side={side}
        sideOffset={sideOffset}
        collisionPadding={collisionPadding}
        sticky="partial"
        avoidCollisions
        updatePositionStrategy="always"
        onCloseAutoFocus={(event) => event.preventDefault()}
      >
        <Calendar {...calendarProps} onSelect={handleSelect} initialFocus />
      </PopoverContent>
    </Popover>
  );
}

export { DatePickerHybrid } from '@/components/ui/date-picker-hybrid';
export type { DatePickerHybridProps } from '@/components/ui/date-picker-hybrid';
export {
  formatDateToBrDisplay,
  isCompleteBrDateDisplay,
  maskBrDateInput,
  parseBrDisplayToDate,
} from '@/components/ui/date-picker-utils';
