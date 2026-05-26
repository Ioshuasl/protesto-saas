'use client';

import { CalendarIcon } from 'lucide-react';
import * as React from 'react';
import type { Locale } from 'react-day-picker';

import { Button } from '@/components/ui/button';
import { Calendar, type CalendarSize } from '@/components/ui/calendar';
import {
  formatDateToBrDisplay,
  isCompleteBrDateDisplay,
  maskBrDateInput,
  parseBrDisplayToDate,
} from '@/components/ui/date-picker-utils';
import { Input } from '@/components/ui/input';
import { Popover, PopoverAnchor, PopoverContent } from '@/components/ui/popover';
import { cn } from '@/lib/utils';

export type DatePickerHybridProps = {
  value?: Date;
  onChange?: (date: Date | undefined) => void;
  placeholder?: string;
  disabled?: boolean;
  calendarDisabled?: React.ComponentProps<typeof Calendar>['disabled'];
  calendarSize?: CalendarSize;
  showOutsideDays?: boolean;
  className?: string;
  inputClassName?: string;
  todayLabel?: string;
  showTodayButton?: boolean;
  align?: React.ComponentProps<typeof PopoverContent>['align'];
  side?: React.ComponentProps<typeof PopoverContent>['side'];
  sideOffset?: number;
  collisionPadding?: number;
  popoverModal?: boolean;
  locale?: Partial<Locale>;
  closeOnSelect?: boolean;
  id?: string;
  name?: string;
  'aria-invalid'?: boolean;
  'aria-describedby'?: string;
};

export function DatePickerHybrid({
  value,
  onChange,
  placeholder = 'dd/mm/aaaa',
  disabled,
  calendarDisabled,
  calendarSize = 'default',
  showOutsideDays = true,
  className,
  inputClassName,
  todayLabel,
  showTodayButton,
  align = 'start',
  side = 'bottom',
  sideOffset = 8,
  collisionPadding = 16,
  popoverModal = true,
  locale,
  closeOnSelect = true,
  id,
  name,
  'aria-invalid': ariaInvalid,
  'aria-describedby': ariaDescribedBy,
}: DatePickerHybridProps) {
  const [open, setOpen] = React.useState(false);
  const [inputText, setInputText] = React.useState(() => formatDateToBrDisplay(value));
  const [inputInvalid, setInputInvalid] = React.useState(false);

  React.useEffect(() => {
    setInputText(formatDateToBrDisplay(value));
    setInputInvalid(false);
  }, [value]);

  const commitDate = React.useCallback(
    (date: Date | undefined) => {
      onChange?.(date);
      setInputText(formatDateToBrDisplay(date));
      setInputInvalid(false);
    },
    [onChange],
  );

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const masked = maskBrDateInput(event.target.value);
    setInputText(masked);
    setInputInvalid(false);

    if (!masked) {
      onChange?.(undefined);
      return;
    }

    if (!isCompleteBrDateDisplay(masked)) return;

    const parsed = parseBrDisplayToDate(masked);
    if (parsed) {
      onChange?.(parsed);
      return;
    }

    setInputInvalid(true);
  };

  const handleInputBlur = () => {
    if (!inputText) {
      commitDate(undefined);
      return;
    }

    if (!isCompleteBrDateDisplay(inputText)) {
      setInputText(formatDateToBrDisplay(value));
      setInputInvalid(false);
      return;
    }

    const parsed = parseBrDisplayToDate(inputText);
    if (!parsed) {
      setInputInvalid(true);
      setInputText(formatDateToBrDisplay(value));
      return;
    }

    commitDate(parsed);
  };

  const handleCalendarSelect = (date: Date | undefined) => {
    commitDate(date);
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

  return (
    <Popover open={open} onOpenChange={setOpen} modal={popoverModal}>
      <PopoverAnchor asChild>
        <div className={cn('relative w-full', className)}>
          <Input
            id={id}
            name={name}
            type="text"
            inputMode="numeric"
            autoComplete="off"
            placeholder={placeholder}
            disabled={disabled}
            value={inputText}
            maxLength={10}
            aria-invalid={ariaInvalid ?? inputInvalid}
            aria-describedby={ariaDescribedBy}
            onChange={handleInputChange}
            onBlur={handleInputBlur}
            className={cn('pr-9', inputClassName)}
          />
          <Button
            type="button"
            variant="ghost"
            size="icon-sm"
            disabled={disabled}
            className="absolute top-1/2 right-1 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            aria-label="Abrir calendário"
            aria-expanded={open}
            onClick={(event) => {
              event.preventDefault();
              event.stopPropagation();
              setOpen((prev) => !prev);
            }}
          >
            <CalendarIcon className="size-4 opacity-70" />
          </Button>
        </div>
      </PopoverAnchor>
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
        <Calendar {...calendarProps} onSelect={handleCalendarSelect} initialFocus />
      </PopoverContent>
    </Popover>
  );
}
