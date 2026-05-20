import { useCallback, useRef } from 'react';

export default function useRunOnceByKey() {
  const done = useRef(new Set<string>());

  const run = useCallback(
    async (key: string, tasks: Array<() => Promise<unknown>>, opts?: { signal?: AbortSignal }) => {
      if (done.current.has(key)) return;
      done.current.add(key);

      await Promise.allSettled(tasks.map((fn) => fn()));
    },
    [],
  );

  const resetKey = useCallback((key: string) => {
    done.current.delete(key);
  }, []);

  return { run, resetKey };
}
