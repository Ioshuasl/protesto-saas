import { useGEmolumentoItemIndexHook } from '@/packages/administrativo/hooks/GEmolumentoItem/useGEmolumentoItemIndexHook';
import { useGEmolumentoItemSaveHook } from '@/packages/administrativo/hooks/GEmolumentoItem/useGEmolumentoItemSaveHook';
import { useGEmolumentoItemShowHook } from '@/packages/administrativo/hooks/GEmolumentoItem/useGEmolumentoItemShowHook';
import { useGEmolumentoItemUpdateHook } from '@/packages/administrativo/hooks/GEmolumentoItem/useGEmolumentoItemUpdateHook';

export const useGEmolumentoItemHooks = () => {
  const index = useGEmolumentoItemIndexHook();
  const show = useGEmolumentoItemShowHook();
  const save = useGEmolumentoItemSaveHook();
  const update = useGEmolumentoItemUpdateHook();

  return {
    index,
    show,
    save,
    update,
  };
};
