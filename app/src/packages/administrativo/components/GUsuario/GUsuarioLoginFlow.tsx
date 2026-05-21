'use client';

import { AnimatePresence, motion } from 'framer-motion';
import Image from 'next/image';
import { useCallback, useState } from 'react';
import { Toaster } from 'sonner';

import { Card, CardContent } from '@/components/ui/card';
import { GUsuarioAuth2FALoginForm } from '@/packages/administrativo/components/GUsuario/GUsuarioAuth2FALoginForm';
import { GUsuarioLoginForm } from '@/packages/administrativo/components/GUsuario/GUsuarioLoginForm';
import { AtendimentoOnlineHelpButton } from '@/shared/components/atendimentoOnline/AtendimentoOnlineHelpButton';

type TwoFactorContext = {
  identificador: string;
  senha_api: string;
  notificationEmail: string;
  challengeExpiresIn: number;
};

const easeSmooth = [0.22, 1, 0.36, 1] as const;

export default function GUsuarioLoginFlow() {
  const [step, setStep] = useState<'credentials' | 'twoFactor'>('credentials');
  const [twoFactorContext, setTwoFactorContext] = useState<TwoFactorContext | null>(null);

  /** Só chamado quando a API retorna two_factor_required (sem data.token) */
  const handleRequiresTwoFactor = useCallback(
    (payload: {
      identificador: string;
      senha_api: string;
      notificationEmail: string;
      challengeExpiresIn: number;
    }) => {
      setTwoFactorContext({
        identificador: payload.identificador,
        senha_api: payload.senha_api,
        notificationEmail: payload.notificationEmail,
        challengeExpiresIn: payload.challengeExpiresIn,
      });
      setStep('twoFactor');
    },
    [],
  );

  const handleBack = useCallback(() => {
    setTwoFactorContext(null);
    setStep('credentials');
  }, []);

  const isOtp = step === 'twoFactor';

  return (
    <div className="flex flex-col gap-6">
      <Card className="overflow-hidden p-0 shadow-md">
        <CardContent className="p-0">
          <div className="flex min-h-[min(28rem,70vh)] flex-col overflow-hidden md:min-h-[420px] md:flex-row">
            <motion.div
              className="relative z-10 flex min-w-0 flex-col bg-card"
              initial={false}
              animate={{
                flex: isOtp ? '1 1 100%' : '1 1 50%',
              }}
              transition={{ duration: 0.55, ease: easeSmooth }}
            >
              <motion.div
                className="flex min-h-0 flex-1 flex-col"
                initial={false}
                animate={isOtp ? { x: [0, 12, 0] } : { x: 0 }}
                transition={{
                  duration: 0.65,
                  ease: easeSmooth,
                  times: [0, 0.45, 1],
                }}
              >
                <AnimatePresence mode="wait">
                  {step === 'credentials' && (
                    <motion.div
                      key="credentials"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -16 }}
                      transition={{ duration: 0.35, ease: easeSmooth }}
                      className="flex min-h-0 w-full flex-1 flex-col justify-center"
                    >
                      <GUsuarioLoginForm
                        variant="embedded"
                        onRequiresTwoFactor={handleRequiresTwoFactor}
                      />
                    </motion.div>
                  )}
                  {step === 'twoFactor' && twoFactorContext && (
                    <motion.div
                      key="twoFactor"
                      initial={{ opacity: 0, x: 28 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      transition={{ duration: 0.38, ease: easeSmooth }}
                      className="flex min-h-0 w-full flex-1 flex-col justify-center"
                    >
                      <GUsuarioAuth2FALoginForm variant="embedded" {...twoFactorContext} onBack={handleBack} />
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            </motion.div>

            <motion.div
              className="relative hidden min-h-0 overflow-hidden bg-brand md:flex"
              aria-hidden={isOtp}
              initial={false}
              animate={{
                flex: isOtp ? '0 1 0%' : '1 1 50%',
                opacity: isOtp ? 0 : 1,
              }}
              transition={{ duration: 0.55, ease: easeSmooth }}
              style={{ pointerEvents: isOtp ? 'none' : 'auto' }}
            >
              <div className="flex min-w-[200px] flex-1 items-center justify-center p-8">
                <Image
                  src="/images/logo-login.svg"
                  alt=""
                  width={300}
                  height={300}
                  priority
                  className="h-auto w-full max-w-[280px] object-contain dark:brightness-[0.2] dark:grayscale"
                  style={{ width: 'auto', height: 'auto' }}
                />
              </div>
            </motion.div>
          </div>
        </CardContent>
      </Card>

      <div className="text-muted-foreground text-center text-xs">
        Ao clicar você concorda com <a href="#">Nossos termos de serviços</a> e{' '}
        <a href="#">Políticas de Privacidade</a>.
      </div>

      <Toaster position="top-center" />

      <AtendimentoOnlineHelpButton />
    </div>
  );
}
