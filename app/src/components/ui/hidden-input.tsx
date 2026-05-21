'use client';

import { Eye, EyeOff } from 'lucide-react';
import * as React from 'react';

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from '@/components/ui/input-group';
import { cn } from '@/lib/utils';

export type HiddenInputProps = Omit<React.ComponentProps<'input'>, 'type'> & {
  /** Quando true, inicia com o texto visível. */
  defaultVisible?: boolean;
};

const HiddenInput = React.forwardRef<HTMLInputElement, HiddenInputProps>(
  ({ className, defaultVisible = false, disabled, ...props }, ref) => {
    const [visible, setVisible] = React.useState(defaultVisible);

    return (
      <InputGroup className={cn('h-9', className)}>
        <InputGroupInput
          ref={ref}
          type={visible ? 'text' : 'password'}
          disabled={disabled}
          className="h-full"
          {...props}
        />
        <InputGroupAddon align="inline-end">
          <InputGroupButton
            type="button"
            variant="ghost"
            size="icon-sm"
            disabled={disabled}
            className="cursor-pointer"
            aria-label={visible ? 'Ocultar senha' : 'Mostrar senha'}
            aria-pressed={visible}
            tabIndex={-1}
            onClick={() => setVisible((current) => !current)}
          >
            {visible ? <EyeOff className="size-4" /> : <Eye className="size-4" />}
          </InputGroupButton>
        </InputGroupAddon>
      </InputGroup>
    );
  },
);

HiddenInput.displayName = 'HiddenInput';

export { HiddenInput };
