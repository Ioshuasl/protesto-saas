'use client';

import { useCallback, useRef } from 'react';

export function useSoundHook(soundPath: string) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  if (!audioRef.current) {
    audioRef.current = new Audio(soundPath);
  }

  const play = useCallback(() => {
    audioRef.current?.play().catch(() => {});
  }, []);

  return play;
}
