'use client';

import { startOfDay } from 'date-fns';
import { ChevronDownIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
import * as React from 'react';
import {
  dateMatchModifiers,
  DayPicker,
  getDefaultClassNames,
  type DayButton,
  type DropdownOption,
  type Locale,
  type Matcher,
  type Modifiers,
  type OnSelectHandler,
} from 'react-day-picker';

import { Button, buttonVariants } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';

export type CalendarSize = 'default' | 'compact';

type DayPickerProps = React.ComponentProps<typeof DayPicker>;
type DayPickerOnSelect = DayPickerProps extends infer Props
  ? Props extends { onSelect?: infer Handler }
    ? Handler
    : never
  : never;

type CalendarProps = DayPickerProps & {
  buttonVariant?: React.ComponentProps<typeof Button>['variant'];
  /** Densidade visual: `compact` para dialogs e telas baixas. */
  size?: CalendarSize;
  /** Exibe botão para selecionar a data atual (apenas em `mode="single"`). Padrão: true. */
  showTodayButton?: boolean;
  todayLabel?: string;
};

function Calendar({
  className,
  classNames,
  showOutsideDays = true,
  captionLayout = 'dropdown',
  buttonVariant = 'ghost',
  size = 'default',
  locale,
  formatters,
  components,
  showTodayButton,
  todayLabel = 'Hoje',
  ...props
}: CalendarProps) {
  const defaultClassNames = getDefaultClassNames();
  const isCompact = size === 'compact';
  const { Footer: userFooter, ...restComponents } = components ?? {};
  const pickerProps = props as DayPickerProps & { onSelect?: DayPickerOnSelect };
  const singleOnSelect =
    pickerProps.mode === 'single' && typeof pickerProps.onSelect === 'function'
      ? (pickerProps.onSelect as OnSelectHandler<Date | undefined>)
      : undefined;
  const shouldShowTodayButton = showTodayButton !== false && Boolean(singleOnSelect);

  return (
    <DayPicker
      {...(props as DayPickerProps)}
      animate={props.animate ?? true}
      showOutsideDays={showOutsideDays}
      className={cn(
        'group/calendar w-fit rounded-xl border border-border bg-popover text-popover-foreground shadow-xl shadow-black/10 dark:border-white/10 dark:bg-[#171717] dark:text-[#f4f4f5] dark:shadow-black/25 [--calendar-accent:#2f9ce5] [--calendar-accent-foreground:#ffffff] [--calendar-accent-muted:rgba(47,156,229,0.18)] [--calendar-fg:var(--foreground)] [--calendar-hover:var(--accent)] [--calendar-muted:var(--muted-foreground)] [--calendar-weekday:var(--muted-foreground)] [--cell-radius:9999px] [--rdp-accent-color:var(--calendar-accent)] [--rdp-accent-background-color:var(--calendar-accent-muted)] [--rdp-animation_duration:650ms] [--rdp-animation_timing:cubic-bezier(0.22,1,0.36,1)] [--rdp-selected-border:0px_solid_transparent] [--rdp-today-color:var(--calendar-accent)] motion-reduce:[--rdp-animation_duration:0ms] dark:[--calendar-fg:#f4f4f5] dark:[--calendar-hover:rgba(255,255,255,0.1)] dark:[--calendar-muted:#71717a] dark:[--calendar-weekday:#d4d4d8]',
        isCompact
          ? 'p-1.5 [--cell-size:1.75rem]'
          : 'p-2 [--cell-size:2.125rem]',
        String.raw`rtl:**:[.rdp-button\_next>svg]:rotate-180`,
        String.raw`rtl:**:[.rdp-button\_previous>svg]:rotate-180`,
        className,
      )}
      captionLayout={captionLayout}
      locale={locale}
      formatters={{
        formatMonthDropdown: (date) => date.toLocaleString(locale?.code, { month: 'short' }),
        formatWeekdayName: (date) =>
          date
            .toLocaleDateString(locale?.code, { weekday: 'short' })
            .slice(0, 2)
            .toUpperCase(),
        ...formatters,
      }}
      classNames={{
        root: cn('w-fit', defaultClassNames.root),
        months: cn(
          'relative flex flex-col md:flex-row',
          isCompact ? 'gap-1.5' : 'gap-3',
          defaultClassNames.months,
        ),
        month: cn(
          'flex w-full flex-col overflow-hidden',
          isCompact ? 'gap-1.5' : 'gap-2',
          defaultClassNames.month,
        ),
        nav: cn(
          'pointer-events-none absolute inset-x-0 top-0 z-10 flex items-center justify-between gap-1',
          defaultClassNames.nav,
        ),
        button_previous: cn(
          buttonVariants({ variant: buttonVariant }),
          'pointer-events-auto rounded-md p-0 text-[var(--calendar-weekday)] select-none hover:bg-[var(--calendar-hover)] hover:text-[var(--calendar-fg)] aria-disabled:opacity-50',
          isCompact ? 'size-6' : 'size-7',
          defaultClassNames.button_previous,
        ),
        button_next: cn(
          buttonVariants({ variant: buttonVariant }),
          'pointer-events-auto rounded-md p-0 text-[var(--calendar-weekday)] select-none hover:bg-[var(--calendar-hover)] hover:text-[var(--calendar-fg)] aria-disabled:opacity-50',
          isCompact ? 'size-6' : 'size-7',
          defaultClassNames.button_next,
        ),
        month_caption: cn(
          'relative flex w-full items-center justify-center px-9',
          isCompact ? 'h-6' : 'h-7',
          defaultClassNames.month_caption,
        ),
        dropdowns: cn(
          'relative flex w-full items-center justify-center gap-1 font-semibold text-[var(--calendar-fg)]',
          isCompact ? 'h-6 text-xs' : 'h-7 text-sm',
          defaultClassNames.dropdowns,
        ),
        dropdown_root: cn(
          'relative rounded-md px-1 transition-colors hover:bg-[var(--calendar-hover)]',
          defaultClassNames.dropdown_root,
        ),
        dropdown: cn('absolute inset-0 cursor-pointer bg-transparent opacity-0', defaultClassNames.dropdown),
        caption_label: cn(
          'font-semibold text-[var(--calendar-fg)] select-none',
          captionLayout === 'label'
            ? isCompact
              ? 'text-sm'
              : 'text-base'
            : cn(
                'flex items-center gap-1 rounded-md py-1 [&>svg]:text-[var(--calendar-weekday)]',
                isCompact ? 'text-sm [&>svg]:size-3' : 'text-base [&>svg]:size-3.5',
              ),
          defaultClassNames.caption_label,
        ),
        table: 'w-full border-collapse',
        weekdays: cn('flex', defaultClassNames.weekdays),
        weekday: cn(
          'flex h-6 flex-1 items-center justify-center rounded-(--cell-radius) font-semibold tracking-wide text-[var(--calendar-weekday)] uppercase select-none',
          isCompact ? 'text-[0.58rem]' : 'text-[0.65rem]',
          defaultClassNames.weekday,
        ),
        week: cn('flex w-full', isCompact ? 'mt-0' : 'mt-0.5', defaultClassNames.week),
        week_number_header: cn(
          'w-(--cell-size) text-[var(--calendar-muted)] select-none',
          defaultClassNames.week_number_header,
        ),
        week_number: cn('text-[0.8rem] text-[var(--calendar-muted)] select-none', defaultClassNames.week_number),
        day: cn(
          'group/day relative flex aspect-square h-full w-full items-center justify-center rounded-(--cell-radius) p-0 text-center select-none [&:last-child[data-selected=true]_button]:rounded-r-(--cell-radius)',
          props.showWeekNumber
            ? '[&:nth-child(2)[data-selected=true]_button]:rounded-l-(--cell-radius)'
            : '[&:first-child[data-selected=true]_button]:rounded-l-(--cell-radius)',
          defaultClassNames.day,
        ),
        range_start: cn(
          'relative isolate z-0 rounded-l-(--cell-radius) bg-[var(--calendar-accent-muted)] after:absolute after:inset-y-0 after:right-0 after:w-1/2 after:bg-[var(--calendar-accent-muted)]',
          defaultClassNames.range_start,
        ),
        range_middle: cn(
          'rounded-none bg-[var(--calendar-accent-muted)]',
          defaultClassNames.range_middle,
        ),
        range_end: cn(
          'relative isolate z-0 rounded-r-(--cell-radius) bg-[var(--calendar-accent-muted)] after:absolute after:inset-y-0 after:left-0 after:w-1/2 after:bg-[var(--calendar-accent-muted)]',
          defaultClassNames.range_end,
        ),
        today: cn(
          'rounded-(--cell-radius) font-semibold text-[var(--calendar-accent)] data-[selected=true]:text-[var(--calendar-accent-foreground)]',
          defaultClassNames.today,
        ),
        selected: cn('border-transparent ring-0 outline-none', defaultClassNames.selected),
        outside: cn('text-[var(--calendar-muted)] aria-selected:text-[var(--calendar-muted)]', defaultClassNames.outside),
        disabled: cn('text-[var(--calendar-muted)] opacity-45', defaultClassNames.disabled),
        hidden: cn('invisible', defaultClassNames.hidden),
        ...classNames,
      }}
      components={{
        ...restComponents,
        Root: ({ className, rootRef, ...rootProps }) => {
          return <div data-slot="calendar" ref={rootRef} className={cn(className)} {...rootProps} />;
        },
        Chevron: ({ className, orientation, ...chevronProps }) => {
          const iconClassName = cn(
            isCompact ? 'size-3.5' : 'size-4',
            'fill-none stroke-current text-[var(--calendar-weekday)] [&_*]:fill-none',
            className,
          );
          if (orientation === 'left') {
            return <ChevronLeftIcon {...chevronProps} className={iconClassName} style={{ fill: 'none' }} />;
          }
          if (orientation === 'right') {
            return <ChevronRightIcon {...chevronProps} className={iconClassName} style={{ fill: 'none' }} />;
          }
          return <ChevronDownIcon {...chevronProps} className={iconClassName} style={{ fill: 'none' }} />;
        },
        DropdownNav: ({ className, children, ...dropdownNavProps }) => (
          <div
            className={cn(
              'relative flex w-full min-w-0 items-center justify-center',
              className,
            )}
            {...dropdownNavProps}
          >
            <div className="flex min-w-0 items-center justify-center gap-1.5">{children}</div>
          </div>
        ),
        Dropdown: (dropdownProps) => (
          <CalendarDropdown calendarSize={size} {...dropdownProps} />
        ),
        DayButton: ({ ...dayProps }) => (
          <CalendarDayButton locale={locale} size={size} {...dayProps} />
        ),
        WeekNumber: ({ children, ...weekProps }) => {
          return (
            <td {...weekProps}>
              <div className="flex size-(--cell-size) items-center justify-center text-center">{children}</div>
            </td>
          );
        },
        Footer: shouldShowTodayButton
          ? (footerProps) => (
              <div {...footerProps} className={cn('flex flex-col', footerProps.className)}>
                {typeof userFooter === 'function' ? userFooter(footerProps) : userFooter}
                <CalendarTodayButton
                  label={todayLabel}
                  disabled={props.disabled}
                  size={size}
                  onSelect={singleOnSelect!}
                />
              </div>
            )
          : userFooter,
      }}
    />
  );
}

function CalendarDropdown({
  options,
  value,
  disabled,
  'aria-label': ariaLabel,
  onChange,
  calendarSize = 'default',
}: {
  options?: DropdownOption[];
  value?: React.SelectHTMLAttributes<HTMLSelectElement>['value'];
  disabled?: boolean;
  'aria-label'?: string;
  onChange?: React.ChangeEventHandler<HTMLSelectElement>;
  calendarSize?: CalendarSize;
}) {
  const selectedValue = Array.isArray(value) ? value[0] : value == null ? undefined : String(value);
  const selectedOption = options?.find((option) => String(option.value) === selectedValue);

  return (
    <Select
      value={selectedValue}
      disabled={disabled}
      onValueChange={(nextValue) => {
        onChange?.({
          target: { value: nextValue },
          currentTarget: { value: nextValue },
        } as React.ChangeEvent<HTMLSelectElement>);
      }}
    >
      <SelectTrigger
        aria-label={ariaLabel}
        size="sm"
        className={cn(
          'h-auto w-auto min-w-fit gap-1 rounded-md border-0 bg-transparent px-1 py-1 font-semibold text-[var(--calendar-fg)] shadow-none hover:bg-[var(--calendar-hover)] focus:ring-0 focus-visible:ring-0 dark:bg-transparent dark:hover:bg-[var(--calendar-hover)] *:data-[slot=select-value]:overflow-visible *:data-[slot=select-value]:whitespace-nowrap [&>svg]:text-[var(--calendar-weekday)] [&>svg]:opacity-100',
          calendarSize === 'compact' ? 'text-xs' : 'text-sm',
        )}
      >
        <SelectValue placeholder={selectedOption?.label} />
      </SelectTrigger>
      <SelectContent
        align="start"
        className="z-[110] max-h-64 min-w-[6rem]"
      >
        {options?.map((option) => (
          <SelectItem
            key={option.value}
            value={String(option.value)}
            disabled={option.disabled}
          >
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

function isDateDisabledByMatcher(date: Date, disabled: Matcher | Matcher[] | boolean | undefined): boolean {
  if (!disabled) return false;
  if (typeof disabled === 'boolean') return disabled;
  return dateMatchModifiers(date, disabled);
}

function CalendarTodayButton({
  label,
  disabled,
  size = 'default',
  onSelect,
}: {
  label: string;
  disabled: CalendarProps['disabled'];
  size?: CalendarSize;
  onSelect: OnSelectHandler<Date | undefined>;
}) {
  const today = React.useMemo(() => startOfDay(new Date()), []);
  const isDisabled = isDateDisabledByMatcher(today, disabled);
  const isCompact = size === 'compact';

  return (
    <div className={cn('border-t border-border/60 dark:border-white/10', isCompact ? 'px-1 pt-1' : 'px-2 pt-2')}>
      <Button
        type="button"
        variant="outline"
        className={cn(
          'w-full dark:border-white/15 dark:bg-white/5 dark:text-[#f4f4f5] dark:hover:bg-white/10 dark:hover:text-white',
          isCompact && 'h-8 text-xs',
        )}
        disabled={isDisabled}
        onClick={(event) => {
          onSelect(today, today, {} as Modifiers, event);
        }}
      >
        {label}
      </Button>
    </div>
  );
}

function CalendarDayButton({
  className,
  day,
  modifiers,
  locale,
  size = 'default',
  ...props
}: React.ComponentProps<typeof DayButton> & { locale?: Partial<Locale>; size?: CalendarSize }) {
  const isCompact = size === 'compact';
  const defaultClassNames = getDefaultClassNames();

  const ref = React.useRef<HTMLButtonElement>(null);
  React.useEffect(() => {
    if (modifiers.focused) ref.current?.focus();
  }, [modifiers.focused]);

  return (
    <Button
      ref={ref}
      variant="ghost"
      size={isCompact ? 'icon-sm' : 'icon'}
      data-day={day.date.toLocaleDateString(locale?.code)}
      data-today={modifiers.today}
      data-outside={modifiers.outside}
      data-selected-single={
        modifiers.selected &&
        !modifiers.range_start &&
        !modifiers.range_end &&
        !modifiers.range_middle
      }
      data-range-start={modifiers.range_start}
      data-range-end={modifiers.range_end}
      data-range-middle={modifiers.range_middle}
      className={cn(
        'relative isolate z-10 flex size-(--cell-size) min-w-(--cell-size) flex-col items-center justify-center gap-1 rounded-(--cell-radius) border-0 bg-transparent p-0 text-sm leading-none font-medium text-[var(--calendar-fg)] transition-colors hover:bg-[var(--calendar-hover)] hover:text-[var(--calendar-fg)] focus-visible:ring-2 focus-visible:ring-[#2f9ce5]/40 focus-visible:ring-offset-0 focus-visible:outline-none aria-selected:border-transparent aria-selected:ring-0 aria-selected:outline-none data-[outside=true]:text-[var(--calendar-muted)] data-[outside=true]:hover:text-[var(--calendar-weekday)] data-[today=true]:text-[var(--calendar-accent)] data-[range-end=true]:rounded-(--cell-radius) data-[range-end=true]:rounded-r-(--cell-radius) data-[range-end=true]:bg-[var(--calendar-accent)] data-[range-end=true]:text-[var(--calendar-accent-foreground)] data-[range-middle=true]:rounded-none data-[range-middle=true]:bg-transparent data-[range-middle=true]:text-[var(--calendar-fg)] data-[range-start=true]:rounded-(--cell-radius) data-[range-start=true]:rounded-l-(--cell-radius) data-[range-start=true]:bg-[var(--calendar-accent)] data-[range-start=true]:text-[var(--calendar-accent-foreground)] data-[selected-single=true]:bg-[var(--calendar-accent)] data-[selected-single=true]:text-[var(--calendar-accent-foreground)] data-[today=true]:after:absolute data-[today=true]:after:-bottom-1 data-[today=true]:after:size-1.5 data-[today=true]:after:rounded-full data-[today=true]:after:bg-[var(--calendar-accent)] disabled:pointer-events-none disabled:opacity-40 [&>span]:text-xs [&>span]:opacity-70',
        defaultClassNames.day_button,
        className,
      )}
      {...props}
    />
  );
}

export { Calendar, CalendarDayButton };
