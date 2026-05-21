import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

import {
  GUsuarioFormValues,
  GUsuarioSchema,
} from '@/packages/administrativo/schemas/GUsuario/GUsuarioSchema';

export function useGUsuarioFormHook(defaults?: Partial<GUsuarioFormValues>) {
  return useForm<GUsuarioFormValues>({
    resolver: zodResolver(GUsuarioSchema),
    defaultValues: {
      usuario_id: 0,
      nome_completo: '',
      email: '',
      cpf: '',
      funcao: '',
      senha_api: '',
      confirma_senha_api: '',      
      ...defaults,
    },
  });
}
