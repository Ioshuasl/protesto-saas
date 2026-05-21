'use client';

import { useEffect, useState } from 'react';

/** Indica que o React já hidratou no cliente (evita mismatch em Radix, tema, etc.). */
export function useHydrated(): boolean {
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setHydrated(true);
  }, []);

  return hydrated;
}
