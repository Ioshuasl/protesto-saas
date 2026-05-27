import { useGEmolumentoListHook } from '@/packages/administrativo/hooks/GEmolumentoList/useGEmolumentoListHook';

export const useGEmolumentoListHooks = () => {
  const list = useGEmolumentoListHook();

  return {
    list,
  };
};
