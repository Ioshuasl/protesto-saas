'use client';

import Image from 'next/image';
import { isRedirectError } from 'next/dist/client/components/redirect-error';
import { useState } from 'react';
import { toast } from 'sonner';

import { useLoginFormHook } from '@/components/hooks/useLoginFormHook';
import { Card, CardContent } from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { HiddenInput } from '@/components/ui/hidden-input';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { GUsuarioLoginFormValues } from '@/packages/administrativo/schemas/GUsuario/GUsuarioLoginSchema';
import GUsuarioLoginService from '@/packages/administrativo/services/GUsuario/GUsuarioLogin';
import { AtendimentoOnlineHelpButton } from '@/shared/components/atendimentoOnline/AtendimentoOnlineHelpButton';
import LoadingButton from '@/shared/components/loadingButton/LoadingButton';

export type GUsuarioLoginFormProps = React.ComponentProps<'div'> & {
  variant?: 'card' | 'embedded';
  onRequiresTwoFactor?: (payload: {
    identificador: string;
    senha_api: string;
    notificationEmail: string;
    challengeExpiresIn: number;
    message?: string;
  }) => void;
};

export function GUsuarioLoginForm({
  className,
  variant = 'card',
  onRequiresTwoFactor,
  ...props
}: GUsuarioLoginFormProps) {
  const form = useLoginFormHook({});
  const [loading, setLoading] = useState(false);

  const onSubmit = async (values: GUsuarioLoginFormValues) => {
    setLoading(true);
    try {
      const result = await GUsuarioLoginService(values);

      if (!result.ok) {
        toast('Atenção', {
          description: result.message,
        });
        return;
      }

      if (result.requiresTwoFactor) {
        if (onRequiresTwoFactor) {
          onRequiresTwoFactor({
            identificador: result.identificador,
            senha_api: result.senha_api,
            notificationEmail: result.data.email,
            challengeExpiresIn: result.data.challenge_expires_in,
            message: result.message,
          });
        } else {
          toast('Verificação em duas etapas', {
            description: result.message,
          });
        }
      }
    } catch (error) {
      if (isRedirectError(error)) {
        throw error;
      }
      toast('Atenção', {
        description: 'Não foi possível concluir o login. Tente novamente.',
      });
    } finally {
      setLoading(false);
    }
  };

  const formInner = (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="mx-auto flex w-full max-w-[400px] flex-col gap-5 px-6 py-8 md:gap-6 md:px-10 md:py-10"
      >
        <div className="flex flex-col items-center gap-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight md:text-[1.75rem]">Bem-vindo de volta</h1>
          <p className="text-muted-foreground text-balance text-sm leading-relaxed md:text-base">
            Entre na sua conta Orius Tecnologia.
          </p>
        </div>
        <div className="flex flex-col gap-4">
          <FormField
            control={form.control}
            name="identificador"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Usuário</FormLabel>
                <FormControl>
                  <Input
                    type="text"
                    autoComplete="username"
                    className="h-10 md:h-11"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="senha_api"
            render={({ field }) => (
              <FormItem>
                <div className="flex flex-row flex-wrap items-center justify-between gap-x-2 gap-y-1">
                  <FormLabel>Senha</FormLabel>
                </div>
                <FormControl>
                  <HiddenInput
                    autoComplete="current-password"
                    className="h-10 md:h-11"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <LoadingButton
          text="Entrar"
          textLoading="Aguarde..."
          type="submit"
          loading={loading}
          className="h-11 w-full text-base font-medium shadow-sm"
        />
      </form>
    </Form>
  );

  if (variant === 'embedded') {
    return (
      <div className={cn('flex min-h-0 w-full flex-1 flex-col justify-center', className)} {...props}>
        {formInner}
      </div>
    );
  }

  return (
    <div className={cn('relative flex flex-col gap-6', className)} {...props}>
      <AtendimentoOnlineHelpButton />
      <Card className="overflow-hidden p-0">
        <CardContent className="grid items-center p-0 md:grid-cols-2">
          <div className="flex w-full flex-col justify-center md:min-h-[420px]">{formInner}</div>
          <div className="bg-brand relative hidden items-center justify-center md:flex">
            <Image
              src="/images/logo-login.svg"
              alt="Logo"
              width={300}
              height={300}
              priority
              className="h-auto max-h-[300px] w-auto max-w-[280px] object-contain dark:brightness-[0.2] dark:grayscale"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
