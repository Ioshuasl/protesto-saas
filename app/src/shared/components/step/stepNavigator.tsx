'use client';

import * as React from 'react';

import { cn } from '@/lib/utils'; // ajuste o caminho conforme seu projeto

/** =========================
 * Constantes (com defaults)
 * ========================= */
const DEFAULT_SCROLL_OFFSET = 16;
const DEFAULT_SPY_LOCK_MS = 600;

/** ===========
 * Tipos
 * =========== */
export type StepKey = string;

export type StepSection = {
  /** chave lógica do step (ex.: 'pedido') */
  key: StepKey;
  /** id do elemento alvo no DOM (ex.: 'selectPedido') */
  id: string;
  /** ícone (lucide ou outro) */
  icon: React.ReactNode;
  /** título do step */
  title: string;
  /** descrição curta do step */
  description?: string;
};

export type StepNavigatorProps = {
  /** Lista de seções em ordem */
  sections: StepSection[];
  /** Ativo controlado externamente */
  active?: StepKey;
  /** Ativo padrão (modo não-controlado) */
  defaultActive?: StepKey;
  /** Callback ao mudar de seção (por scroll ou clique) */
  onChange?: (key: StepKey) => void;

  /** Offset do topo ao calcular posicionamento (ex.: header fixo) */
  scrollOffset?: number;
  /** Tempo de bloqueio do spy após scroll programático */
  spyLockMs?: number;

  /** Classe extra no container */
  className?: string;
  /** Se `false`, desabilita o scroll-spy */
  enableScrollSpy?: boolean;
};

/** =================
 * Hook: useScrollSpy
 * ================= */
function useScrollSpy(opts: {
  sections: StepSection[];
  active: StepKey | undefined;
  setActive: (key: StepKey) => void;
  scrollOffset: number;
  enable: boolean;
  lockMs: number;
}) {
  const { sections, active, setActive, scrollOffset, enable, lockMs } = opts;

  // bloqueio do spy durante rolagem programática
  const spyLockedRef = React.useRef(false);
  const spyTimerRef = React.useRef<number | null>(null);

  const lockSpy = React.useCallback(() => {
    spyLockedRef.current = true;
    if (spyTimerRef.current) window.clearTimeout(spyTimerRef.current);
    spyTimerRef.current = window.setTimeout(() => {
      spyLockedRef.current = false;
    }, lockMs) as unknown as number;
  }, [lockMs]);

  const scrollToId = React.useCallback(
    (id: string) => {
      const el = document.getElementById(id);
      if (!el) return;
      lockSpy();
      const y = el.getBoundingClientRect().top + window.scrollY - scrollOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    },
    [lockSpy, scrollOffset],
  );

  React.useEffect(() => {
    if (!enable) return;

    const handler = () => {
      if (spyLockedRef.current) return;

      let current: StepKey | undefined = undefined;
      let best = Number.POSITIVE_INFINITY;

      for (const { key, id } of sections) {
        const el = document.getElementById(id);
        if (!el) continue;
        const dist = Math.abs(el.getBoundingClientRect().top - scrollOffset - 8);
        if (dist < best) {
          best = dist;
          current = key;
        }
      }

      if (current && current !== active) {
        setActive(current);
      }
    };

    handler(); // avalia logo ao montar
    window.addEventListener('scroll', handler, { passive: true });
    return () => window.removeEventListener('scroll', handler);
  }, [enable, sections, active, scrollOffset, setActive]);

  return { scrollToId, lockSpy };
}

/** ==================
 * Subcomponente: StepLink
 * ================== */
function StepLink({
  active,
  onClick,
  icon,
  title,
  description,
}: {
  active?: boolean;
  onClick?: () => void;
  icon: React.ReactNode;
  title: string;
  description?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        'group w-full cursor-pointer rounded-xl p-4 text-left hover:bg-gray-100 dark:hover:bg-gray-700',
        active && 'ring-primary/60 ring-1',
      )}
      aria-current={active ? 'step' : undefined}
    >
      <span className="flex items-center gap-2">
        <span
          className={cn(
            'flex h-9 w-9 items-center justify-center rounded-full',
            'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-gray-100',
            'group-hover:bg-white dark:group-hover:bg-gray-800',
          )}
        >
          {icon}
        </span>
        <span className="flex flex-1 flex-col">
          <span className="font-bold">{title}</span>
          {description ? (
            <span className="text-muted-foreground text-sm">{description}</span>
          ) : null}
        </span>
      </span>
    </button>
  );
}

/** ===================
 * Componente principal
 * =================== */
export type StepNavigatorRef = {
  /** Rola até a seção pela key ou id */
  scrollTo: (target: StepKey | { id: string }) => void;
};

export const StepNavigator = React.forwardRef<StepNavigatorRef, StepNavigatorProps>(
  (
    {
      sections,
      active: activeProp,
      defaultActive,
      onChange,
      scrollOffset = DEFAULT_SCROLL_OFFSET,
      spyLockMs = DEFAULT_SPY_LOCK_MS,
      className,
      enableScrollSpy = true,
    },
    ref,
  ) => {
    // estado controlado/ não-controlado
    const [activeState, setActiveState] = React.useState<StepKey | undefined>(
      activeProp ?? defaultActive ?? sections[0]?.key,
    );

    // sincroniza quando for controlado
    React.useEffect(() => {
      if (activeProp !== undefined) setActiveState(activeProp);
    }, [activeProp]);

    const setActive = React.useCallback(
      (key: StepKey) => {
        if (activeProp === undefined) {
          setActiveState(key);
        }
        onChange?.(key);
      },
      [activeProp, onChange],
    );

    const { scrollToId, lockSpy } = useScrollSpy({
      sections,
      active: activeState,
      setActive,
      scrollOffset,
      enable: enableScrollSpy,
      lockMs: spyLockMs,
    });

    const scrollTo = React.useCallback(
      (target: StepKey | { id: string }) => {
        const id =
          typeof target === 'string' ? sections.find((s) => s.key === target)?.id : target.id;
        if (!id) return;
        scrollToId(id);
      },
      [sections, scrollToId],
    );

    React.useImperativeHandle(ref, () => ({ scrollTo }), [scrollTo]);

    return (
      <nav className={cn('flex flex-col gap-2', className)} aria-label="Steps">
        <ol className="flex flex-col gap-2">
          {sections.map((s) => (
            <li key={s.key}>
              <StepLink
                active={activeState === s.key}
                icon={s.icon}
                title={s.title}
                description={s.description}
                onClick={() => {
                  // ao clicar, trava o spy por um curto período e rola
                  lockSpy();
                  setActive(s.key);
                  scrollTo({ id: s.id });
                }}
              />
            </li>
          ))}
        </ol>
      </nav>
    );
  },
);
StepNavigator.displayName = 'StepNavigator';
