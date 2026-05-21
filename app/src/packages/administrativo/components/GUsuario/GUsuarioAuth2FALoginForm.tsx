'use client';

import Image from 'next/image';
import { isRedirectError } from 'next/dist/client/components/redirect-error';
import { useEffect, useRef, useState } from 'react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { InputOTP, InputOTPGroup, InputOTPSlot } from '@/components/ui/input-otp';
import { cn } from '@/lib/utils';
import { useGUsuarioAuth2FAFormHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioAuth2FAFormHook';
import { useGUsuarioAuth2FAHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioAuth2FAHook';
import {
  GUsuarioAuth2FALoginFormValues,
  GUsuarioAuth2FAOTP_LENGTH,
} from '@/packages/administrativo/schemas/GUsuario/GUsuarioAuth2FALoginSchema';
import { AtendimentoOnlineHelpButton } from '@/shared/components/atendimentoOnline/AtendimentoOnlineHelpButton';
import LoadingButton from '@/shared/components/loadingButton/LoadingButton';

export type GUsuarioAuth2FALoginFormProps = React.ComponentProps<'div'> & {
  variant?: 'card' | 'embedded';
  identificador: string;
  senha_api: string;
  /** E-mail cadastrado — usado só na mensagem do OTP (envio n8n) */
  notificationEmail: string;
  challengeExpiresIn: number;
  onBack: () => void;
};

function formatRemaining(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

export function GUsuarioAuth2FALoginForm({
  identificador,
  senha_api,
  notificationEmail,
  challengeExpiresIn,
  onBack,
  className,
  variant = 'card',
  ...props
}: GUsuarioAuth2FALoginFormProps) {
  if (!identificador?.trim() || !senha_api || !notificationEmail?.trim()) {
    return null;
  }
  const form = useGUsuarioAuth2FAFormHook({});
  const { verifyAuth2FA, loading } = useGUsuarioAuth2FAHook();

  const [remainingSec, setRemainingSec] = useState(challengeExpiresIn);
  const expiryNavigateSentinelRef = useRef(false);

  useEffect(() => {
    expiryNavigateSentinelRef.current = false;
    setRemainingSec(challengeExpiresIn);
  }, [challengeExpiresIn]);

  useEffect(() => {
    if (remainingSec <= 0) return;
    const t = window.setTimeout(() => setRemainingSec((s) => Math.max(0, s - 1)), 1000);
    return () => window.clearTimeout(t);
  }, [remainingSec]);

  useEffect(() => {
    if (remainingSec > 0) return;
    if (expiryNavigateSentinelRef.current) return;
    expiryNavigateSentinelRef.current = true;
    toast('Código expirado', {
      description: 'O tempo para informar o código acabou. Faça login novamente.',
    });
    onBack();
  }, [remainingSec, onBack]);

  const onSubmit = async (values: GUsuarioAuth2FALoginFormValues) => {
    try {
      const result = await verifyAuth2FA({
        identificador,
        senha_api,
        codigo_seguranca: values.codigo_seguranca,
      });

      if (result?.ok === false) {
        toast('Atenção', {
          description: result.message,
        });
      }
    } catch (error) {
      if (isRedirectError(error)) {
        throw error;
      }
      toast('Atenção', {
        description: 'Não foi possível concluir a verificação. Tente novamente.',
      });
    }
  };

  const otpIndexes = Array.from({ length: GUsuarioAuth2FAOTP_LENGTH }, (_, i) => i);

  const actionBtnClass = cn(
    'cursor-pointer font-medium shadow-sm',
    variant === 'embedded' ? 'h-11 sm:h-14' : 'h-11 sm:h-[3.25rem]',
    variant === 'embedded' ? 'px-4 text-sm sm:px-5 sm:text-base' : 'px-4 text-sm sm:px-5',
  );

  const formInner = (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="mx-auto flex w-full max-w-xl flex-col gap-6 px-6 py-8 md:max-w-3xl md:gap-7 md:px-10 md:py-10"
      >
        <div className="flex flex-col items-center gap-3 text-center">
          <h1 className="text-2xl font-semibold tracking-tight md:text-[1.75rem]">
            Verificação em duas etapas
          </h1>
          <p className="text-muted-foreground max-w-lg text-balance text-sm leading-relaxed md:text-base">
            Digite o código de {GUsuarioAuth2FAOTP_LENGTH} dígitos enviado para{' '}
            <span className="text-foreground font-medium">{notificationEmail}</span>
          </p>
          <p
            className={cn(
              'text-center text-xs font-medium sm:text-sm',
              remainingSec > 0
                ? 'bg-muted text-muted-foreground inline-flex items-center rounded-full px-3 py-1 tabular-nums tracking-wide'
                : 'bg-destructive/10 text-destructive max-w-md rounded-lg px-4 py-2 leading-snug',
            )}
            aria-live="polite"
          >
            {remainingSec > 0 ? (
              <>Expira em {formatRemaining(remainingSec)}</>
            ) : (
              <>O tempo do código pode ter expirado. Solicite um novo login.</>
            )}
          </p>
        </div>

        <FormField
          control={form.control}
          name="codigo_seguranca"
          render={({ field }) => (
            <FormItem className="flex flex-col items-center gap-4 md:gap-5">
              <FormLabel className="sr-only">Código de verificação</FormLabel>

              <div className="flex w-full flex-col items-center gap-5 md:flex-row md:flex-wrap md:items-center md:justify-center md:gap-x-6 md:gap-y-4">
                <FormControl>
                  <InputOTP
                    maxLength={GUsuarioAuth2FAOTP_LENGTH}
                    value={field.value}
                    onChange={field.onChange}
                    containerClassName="justify-center gap-0"
                  >
                    <InputOTPGroup
                      className={cn(
                        'justify-center',
                        variant === 'embedded' ? 'gap-3 sm:gap-4' : 'gap-2.5 sm:gap-3.5',
                      )}
                    >
                      {otpIndexes.map((index) => (
                        <InputOTPSlot
                          key={index}
                          index={index}
                          split
                          className={cn(
                            variant === 'embedded' &&
                              'font-semibold tracking-[0.12em] sm:size-14 sm:text-xl',
                          )}
                        />
                      ))}
                    </InputOTPGroup>
                  </InputOTP>
                </FormControl>

                <div className="flex w-full max-w-md flex-row items-center justify-center gap-3 md:w-auto md:max-w-none md:shrink-0 md:self-center">
                  <Button type="button" variant="outline" className={cn(actionBtnClass, 'flex-1 md:flex-initial')} onClick={onBack}>
                    Voltar
                  </Button>
                  <LoadingButton
                    text="Confirmar código"
                    textLoading="Verificando..."
                    type="submit"
                    loading={loading}
                    disabled={remainingSec <= 0}
                    className={cn(actionBtnClass, 'min-w-0 flex-1 md:min-w-[11rem] md:flex-initial')}
                  />
                </div>
              </div>

              <FormMessage className="text-center" />
            </FormItem>
          )}
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
