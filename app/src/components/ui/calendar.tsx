'use client';

import { startOfDay } from 'date-fns';
import { ChevronDownIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
import * as React from 'react';
import {
  dateMatchModifiers,
  DayPicker,
  getDefaultClassNames,
  type DayButton,
  type Locale,
  type Matcher,
  type Modifiers,
  type OnSelectHandler,
} from 'react-day-picker';

import { Button, buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export type CalendarSize = 'default' | 'compact';

type CalendarProps = React.ComponentProps<typeof DayPicker> & {
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
  captionLayout = 'label',
  buttonVariant = 'ghost',
  size = 'default',
  locale,
  formatters,
  components,
  showTodayButton,
  todayLabel = 'Hoje',
  mode,
  onSelect,
  disabled,
  ...props
}: CalendarProps) {
  const defaultClassNames = getDefaultClassNames();
  const isCompact = size === 'compact';
  const { Footer: userFooter, ...restComponents } = components ?? {};
  const shouldShowTodayButton =
    showTodayButton !== false && mode === 'single' && typeof onSelect === 'function';

  return (
    <DayPicker
      mode={mode}
      onSelect={onSelect}
      disabled={disabled}
      showOutsideDays={showOutsideDays}
      className={cn(
        'group/calendar bg-background [--cell-radius:var(--radius-md)] [--rdp-selected-border:0px_solid_transparent] in-data-[slot=card-content]:bg-transparent in-data-[slot=popover-content]:bg-transparent',
        isCompact
          ? 'p-1 [--cell-size:1.75rem]'
          : 'p-2 [--cell-size:--spacing(7)]',
        String.raw`rtl:**:[.rdp-button\_next>svg]:rotate-180`,
        String.raw`rtl:**:[.rdp-button\_previous>svg]:rotate-180`,
        className,
      )}
      captionLayout={captionLayout}
      locale={locale}
      formatters={{
        formatMonthDropdown: (date) => date.toLocaleString(locale?.code, { month: 'short' }),
        ...formatters,
      }}
      classNames={{
        root: cn('w-fit', defaultClassNames.root),
        months: cn(
          'relative flex flex-col md:flex-row',
          isCompact ? 'gap-2' : 'gap-4',
          defaultClassNames.months,
        ),
        month: cn(
          'flex w-full flex-col',
          isCompact ? 'gap-2' : 'gap-4',
          defaultClassNames.month,
        ),
        nav: cn(
          'absolute inset-x-0 top-0 flex w-full items-center justify-between gap-1',
          defaultClassNames.nav,
        ),
        button_previous: cn(
          buttonVariants({ variant: buttonVariant }),
          'size-(--cell-size) p-0 select-none aria-disabled:opacity-50',
          defaultClassNames.button_previous,
        ),
        button_next: cn(
          buttonVariants({ variant: buttonVariant }),
          'size-(--cell-size) p-0 select-none aria-disabled:opacity-50',
          defaultClassNames.button_next,
        ),
        month_caption: cn(
          'flex h-(--cell-size) w-full items-center justify-center px-(--cell-size)',
          defaultClassNames.month_caption,
        ),
        dropdowns: cn(
          'flex h-(--cell-size) w-full items-center justify-center gap-1.5 text-sm font-medium',
          defaultClassNames.dropdowns,
        ),
        dropdown_root: cn('relative rounded-(--cell-radius)', defaultClassNames.dropdown_root),
        dropdown: cn('absolute inset-0 bg-popover opacity-0', defaultClassNames.dropdown),
        caption_label: cn(
          'font-medium select-none',
          captionLayout === 'label'
            ? isCompact
              ? 'text-xs'
              : 'text-sm'
            : cn(
                'flex items-center gap-1 rounded-(--cell-radius) [&>svg]:text-muted-foreground',
                isCompact ? 'text-xs [&>svg]:size-3' : 'text-sm [&>svg]:size-3.5',
              ),
          defaultClassNames.caption_label,
        ),
        table: 'w-full border-collapse',
        weekdays: cn('flex', defaultClassNames.weekdays),
        weekday: cn(
          'flex-1 rounded-(--cell-radius) font-normal text-muted-foreground select-none',
          isCompact ? 'text-[0.65rem]' : 'text-[0.8rem]',
          defaultClassNames.weekday,
        ),
        week: cn('flex w-full', isCompact ? 'mt-0.5' : 'mt-2', defaultClassNames.week),
        week_number_header: cn('w-(--cell-size) select-none', defaultClassNames.week_number_header),
        week_number: cn('text-[0.8rem] text-muted-foreground select-none', defaultClassNames.week_number),
        day: cn(
          'group/day relative aspect-square h-full w-full rounded-(--cell-radius) p-0 text-center select-none [&:last-child[data-selected=true]_button]:rounded-r-(--cell-radius)',
          props.showWeekNumber
            ? '[&:nth-child(2)[data-selected=true]_button]:rounded-l-(--cell-radius)'
            : '[&:first-child[data-selected=true]_button]:rounded-l-(--cell-radius)',
          defaultClassNames.day,
        ),
        range_start: cn(
          'relative isolate z-0 rounded-l-(--cell-radius) bg-muted after:absolute after:inset-y-0 after:right-0 after:w-4 after:bg-muted',
          defaultClassNames.range_start,
        ),
        range_middle: cn('rounded-none', defaultClassNames.range_middle),
        range_end: cn(
          'relative isolate z-0 rounded-r-(--cell-radius) bg-muted after:absolute after:inset-y-0 after:left-0 after:w-4 after:bg-muted',
          defaultClassNames.range_end,
        ),
        today: cn(
          /* Let --rdp-today-color / --primary show through (avoid text-foreground overriding library today color). */
          'rounded-(--cell-radius) bg-muted font-medium data-[selected=true]:rounded-none',
          defaultClassNames.today,
        ),
        selected: cn('border-transparent ring-0 outline-none', defaultClassNames.selected),
        outside: cn('text-muted-foreground aria-selected:text-muted-foreground', defaultClassNames.outside),
        disabled: cn('text-muted-foreground opacity-50', defaultClassNames.disabled),
        hidden: cn('invisible', defaultClassNames.hidden),
        ...classNames,
      }}
      components={{
        ...restComponents,
        Root: ({ className, rootRef, ...rootProps }) => {
          return <div data-slot="calendar" ref={rootRef} className={cn(className)} {...rootProps} />;
        },
        Chevron: ({ className, orientation, ...chevronProps }) => {
          const iconSize = isCompact ? 'size-3.5' : 'size-4';
          if (orientation === 'left') {
            return <ChevronLeftIcon className={cn(iconSize, className)} {...chevronProps} />;
          }
          if (orientation === 'right') {
            return <ChevronRightIcon className={cn(iconSize, className)} {...chevronProps} />;
          }
          return <ChevronDownIcon className={cn(iconSize, className)} {...chevronProps} />;
        },
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
                  disabled={disabled}
                  size={size}
                  onSelect={onSelect as OnSelectHandler<Date | undefined>}
                />
              </div>
            )
          : userFooter,
      }}
      {...props}
    />
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
    <div className={cn('border-t', isCompact ? 'px-1 pt-1' : 'px-2 pt-2')}>
      <Button
        type="button"
        variant="outline"
        className={cn('w-full', isCompact && 'h-8 text-xs')}
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
        'relative isolate z-10 flex aspect-square size-auto w-full min-w-(--cell-size) flex-col gap-1 border-0 leading-none font-normal focus-visible:ring-0 focus-visible:ring-offset-0 focus-visible:outline-none aria-selected:border-transparent aria-selected:ring-0 aria-selected:outline-none data-[range-end=true]:rounded-(--cell-radius) data-[range-end=true]:rounded-r-(--cell-radius) data-[range-end=true]:bg-primary data-[range-end=true]:text-primary-foreground data-[range-middle=true]:rounded-none data-[range-middle=true]:bg-muted data-[range-middle=true]:text-foreground data-[range-start=true]:rounded-(--cell-radius) data-[range-start=true]:rounded-l-(--cell-radius) data-[range-start=true]:bg-primary data-[range-start=true]:text-primary-foreground data-[selected-single=true]:bg-primary data-[selected-single=true]:text-primary-foreground dark:hover:text-foreground [&>span]:text-xs [&>span]:opacity-70',
        defaultClassNames.day,
        className,
      )}
      {...props}
    />
  );
}

export { Calendar, CalendarDayButton };
