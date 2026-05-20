import * as React from 'react';

const MOBILE_BREAKPOINT = 768;

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined);

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`);
    const onChange = (event?: MediaQueryListEvent) => {
      if (event?.matches !== undefined) {
        setIsMobile(event.matches);
        return;
      }
      setIsMobile(mql.matches);
    };

    // Set initial value before wiring listeners (important for older mobile browsers).
    setIsMobile(mql.matches);

    if (typeof mql.addEventListener === 'function') {
      mql.addEventListener('change', onChange);
      return () => mql.removeEventListener('change', onChange);
    }

    // Safari < 14 and some embedded browsers.
    mql.addListener(onChange);
    return () => mql.removeListener(onChange);
  }, []);

  return !!isMobile;
}
