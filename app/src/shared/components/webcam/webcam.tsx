'use client';

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

type WebcamCaptureProps = {
  width?: number;
  height?: number;
  /** Recebe a base64 (sem o prefixo data:image/*;base64,) */
  onCapture?: (base64: string) => void;
  /** Opcional: nome do input hidden para enviar em forms */
  hiddenInputName?: string;
};

const WebcamCapture: React.FC<WebcamCaptureProps> = ({
  width = 320,
  height = 240,
  onCapture,
  hiddenInputName,
}) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const [devices, setDevices] = useState<MediaDeviceInfo[]>([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string>('');
  const [photoBase64, setPhotoBase64] = useState<string>('');

  const hasDevices = useMemo(() => devices.length > 0, [devices]);

  const stopWebcam = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsStreaming(false);
  }, []);

  const loadDevices = useCallback(async () => {
    if (!navigator.mediaDevices?.enumerateDevices) return;

    const all = await navigator.mediaDevices.enumerateDevices();
    const videoDevices = all.filter(
      (d) => d.kind === 'videoinput' && d.deviceId && d.deviceId.trim() !== '',
    );

    setDevices(videoDevices);

    // Se não houver selecionada, seleciona a primeira
    if (!selectedDeviceId && videoDevices.length > 0) {
      setSelectedDeviceId(videoDevices[0].deviceId);
      return;
    }

    // Se a selecionada não existir mais, seleciona a primeira disponível
    if (
      selectedDeviceId &&
      videoDevices.length > 0 &&
      !videoDevices.some((d) => d.deviceId === selectedDeviceId)
    ) {
      setSelectedDeviceId(videoDevices[0].deviceId);
    }

    // Se não houver câmera, limpa seleção
    if (videoDevices.length === 0) {
      setSelectedDeviceId('');
    }
  }, [selectedDeviceId]);

  const ensurePermission = useCallback(async () => {
    if (!navigator.mediaDevices?.getUserMedia) return false;

    try {
      // Necessário para liberar labels em alguns browsers
      const temp = await navigator.mediaDevices.getUserMedia({ video: true });
      temp.getTracks().forEach((t) => t.stop());
      return true;
    } catch {
      return false;
    }
  }, []);

  const startWebcam = useCallback(async () => {
    setError('');

    if (!navigator.mediaDevices?.getUserMedia) {
      setError('Seu navegador não suporta acesso à câmera.');
      return;
    }

    if (!selectedDeviceId) {
      setIsStreaming(false);
      return;
    }

    try {
      stopWebcam();

      const constraints: MediaStreamConstraints = {
        video: { deviceId: { exact: selectedDeviceId } },
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      setIsStreaming(true);
    } catch {
      setError('Não foi possível acessar a câmera selecionada. Verifique as permissões.');
      setIsStreaming(false);
    }
  }, [selectedDeviceId, stopWebcam]);

  const handleCapture = useCallback(() => {
    if (!videoRef.current || !isStreaming) return;

    const video = videoRef.current;

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || width;
    canvas.height = video.videoHeight || height;

    const ctx = canvas.getContext('2d');
    if (!ctx) {
      setError('Não foi possível capturar a imagem.');
      return;
    }

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/png');
    const base64Only = dataUrl.split(',')[1];

    setPhotoBase64(base64Only);

    if (onCapture) {
      onCapture(base64Only);
    }
  }, [isStreaming, onCapture, width, height]);

  // Inicialização: permissão -> lista de devices
  useEffect(() => {
    const init = async () => {
      setError('');

      const ok = await ensurePermission();
      if (!ok) {
        setError('Permissão de câmera negada ou indisponível.');
        return;
      }

      await loadDevices();
    };

    init();

    navigator.mediaDevices?.addEventListener('devicechange', loadDevices);

    return () => {
      navigator.mediaDevices?.removeEventListener('devicechange', loadDevices);
    };
  }, [ensurePermission, loadDevices]);

  // Start/restart quando seleciona câmera
  useEffect(() => {
    if (!selectedDeviceId) return;

    startWebcam();

    return () => {
      stopWebcam();
    };
  }, [selectedDeviceId, startWebcam, stopWebcam]);

  // Cleanup ao desmontar
  useEffect(() => {
    return () => {
      stopWebcam();
    };
  }, [stopWebcam]);

  return (
    <div className="space-y-3">
      {/* Lista de webcams + seleção */}
      <Select
        value={selectedDeviceId}
        onValueChange={(value) => setSelectedDeviceId(value)}
        disabled={!hasDevices}
      >
        <SelectTrigger className="w-full">
          <SelectValue
            placeholder={hasDevices ? 'Selecione a câmera' : 'Nenhuma câmera encontrada'}
          />
        </SelectTrigger>
        <SelectContent>
          {devices
            .filter((device) => device.deviceId && device.deviceId.trim() !== '')
            .map((device, index) => (
              <SelectItem key={device.deviceId} value={device.deviceId}>
                {device.label || `Câmera ${index + 1}`}
              </SelectItem>
            ))}
        </SelectContent>
      </Select>

      {/* Quadrado (live) com ação de captura */}
      <div className="bg-muted/10 relative aspect-square w-full overflow-hidden rounded-lg border">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="absolute inset-0 z-0 h-full w-full object-cover"
        />

        <div className="absolute inset-x-0 bottom-3 z-10 flex justify-center">
          <Button
            type="button"
            size="icon"
            disabled={!isStreaming}
            onClick={handleCapture}
            className="h-11 w-11 rounded-full"
            aria-label="Capturar foto"
          >
            <span className="sr-only">Capturar</span>
            {/* ...svg... */}
          </Button>
        </div>
      </div>

      {error && <p className="text-destructive text-sm">{error}</p>}

      {hiddenInputName && photoBase64 && (
        <input type="hidden" name={hiddenInputName} value={photoBase64} />
      )}
    </div>
  );
};

export default WebcamCapture;
