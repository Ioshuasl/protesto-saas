'use client';

import { PlusIcon } from 'lucide-react';
import Link from 'next/link';

import { Button } from '@/components/ui/button';

interface HeaderProps {
  title: string;
  description: string;
  buttonText: string;
  href?: `/${string}`;
  buttonAction?: () => void;
  className?: string;
}

export default function Header({
  title,
  description,
  buttonText,
  href,
  buttonAction,
  className,
}: HeaderProps) {
  return (
    <div className={className}>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="mb-1 text-4xl font-semibold">{title}</h1>
          <p className="text-muted-foreground text-base">{description}</p>
        </div>

        {href ? (
          <Button asChild className="cursor-pointer">
            <Link href={href} prefetch>
              <PlusIcon className="mr-2 h-4 w-4" />
              {buttonText}
            </Link>
          </Button>
        ) : (
          <Button onClick={() => buttonAction?.()} className="cursor-pointer">
            <PlusIcon className="mr-2 h-4 w-4" />
            {buttonText}
          </Button>
        )}
      </div>
    </div>
  );
}
