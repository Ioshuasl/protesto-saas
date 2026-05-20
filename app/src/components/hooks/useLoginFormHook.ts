import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

import {
  GUsuarioLoginFormValues,
  GUsuarioLoginSchema,
} from '@/packages/administrativo/schemas/GUsuario/GUsuarioLoginSchema';

export function useLoginFormHook(defaults?: Partial<GUsuarioLoginFormValues>) {
  return useForm<GUsuarioLoginFormValues>({
    resolver: zodResolver(GUsuarioLoginSchema),
    defaultValues: {
      login: '',
      senha_api: '',
      ...defaults,
    },
  });
}
