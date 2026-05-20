'use client';

import clsx from 'clsx';
import { Loader } from 'lucide-react';
import { forwardRef } from 'react';

import { Button } from '@/components/ui/button';

import type LoadingButtonProps from './LoadingButtonInterface';

const LoadingButton = forwardRef<HTMLButtonElement, LoadingButtonProps>(
  (
    { text, textLoading, loading = false, className, disabled, type = 'button', onClick, ...props },
    ref,
  ) => {
    const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
      if (loading) {
        e.preventDefault();
        return;
      }
      if (onClick) onClick(e);
    };

    return (
      <Button
        ref={ref}
        type={type}
        disabled={loading || disabled}
        aria-busy={loading}
        aria-live="polite"
        onClick={handleClick}
        className={clsx('cursor-pointer', className)}
        {...props}
      >
        {loading && <Loader className="h-4 w-4 animate-spin" aria-hidden="true" />}
        <span>{loading ? textLoading : text}</span>
      </Button>
    );
  },
);

LoadingButton.displayName = 'LoadingButton';

export default LoadingButton;
