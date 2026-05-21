import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

import {
  GUsuarioAuth2FALoginFormValues,
  GUsuarioAuth2FALoginSchema,
} from '@/packages/administrativo/schemas/GUsuario/GUsuarioAuth2FALoginSchema';

export function useGUsuarioAuth2FAFormHook(defaults?: Partial<GUsuarioAuth2FALoginFormValues>) {
  return useForm<GUsuarioAuth2FALoginFormValues>({
    resolver: zodResolver(GUsuarioAuth2FALoginSchema),
    defaultValues: {
      codigo_seguranca: '',
      ...defaults,
    },
  });
}
