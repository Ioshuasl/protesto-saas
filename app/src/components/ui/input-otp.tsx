'use client';

import { OTPInput, OTPInputContext } from 'input-otp';
import { MinusIcon } from 'lucide-react';
import * as React from 'react';

import { cn } from '@/lib/utils';

function InputOTP({
  className,
  containerClassName,
  ...props
}: React.ComponentProps<typeof OTPInput> & {
  containerClassName?: string;
}) {
  return (
    <OTPInput
      data-slot="input-otp"
      containerClassName={cn('flex items-center gap-2 has-disabled:opacity-50', containerClassName)}
      className={cn('disabled:cursor-not-allowed', className)}
      {...props}
    />
  );
}

function InputOTPGroup({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div data-slot="input-otp-group" className={cn('flex items-center', className)} {...props} />
  );
}

function InputOTPSlot({
  index,
  className,
  split = false,
  ...props
}: React.ComponentProps<'div'> & {
  index: number;
  /** Caixas independentes (espaçamento, borda completa, estados filled/active) */
  split?: boolean;
}) {
  const inputOTPContext = React.useContext(OTPInputContext);
  const { char, hasFakeCaret, isActive } = inputOTPContext?.slots[index] ?? {};
  const filled = Boolean(char);

  return (
    <div
      data-slot="input-otp-slot"
      data-active={isActive}
      data-filled={filled}
      className={cn(
        'relative flex items-center justify-center font-medium tabular-nums outline-none transition-[transform,box-shadow,border-color,background-color] duration-200 ease-out',
        split
          ? cn(
              'size-11 rounded-xl border border-input bg-muted/30 text-base shadow-none sm:size-[3.25rem] sm:text-lg',
              'data-[filled=true]:border-foreground/40 data-[filled=true]:bg-background data-[filled=true]:text-foreground',
              'data-[active=true]:z-10 data-[active=true]:-translate-y-0.5 data-[active=true]:scale-[1.04] data-[active=true]:border-ring data-[active=true]:bg-background data-[active=true]:shadow-md',
              'data-[active=true]:ring-2 data-[active=true]:ring-ring/35',
              'aria-invalid:border-destructive data-[active=true]:aria-invalid:ring-destructive/30',
            )
          : cn(
              'dark:bg-input/30 border-input h-9 w-9 border-y border-r text-sm shadow-xs first:rounded-l-md first:border-l last:rounded-r-md',
              'data-[active=true]:border-ring data-[active=true]:ring-ring/50 data-[active=true]:aria-invalid:ring-destructive/20 dark:data-[active=true]:aria-invalid:ring-destructive/40 aria-invalid:border-destructive data-[active=true]:aria-invalid:border-destructive data-[active=true]:z-10 data-[active=true]:ring-[3px]',
            ),
        className,
      )}
      {...props}
    >
      {char}
      {hasFakeCaret && (
        <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
          <div className="animate-caret-blink bg-foreground h-4 w-px duration-1000" />
        </div>
      )}
    </div>
  );
}

function InputOTPSeparator({ ...props }: React.ComponentProps<'div'>) {
  return (
    <div data-slot="input-otp-separator" role="separator" {...props}>
      <MinusIcon />
    </div>
  );
}

export { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator };
