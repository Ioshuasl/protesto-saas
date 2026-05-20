// app/src/app/_response/response.tsx
'use client';

import { useEffect } from 'react';
import { toast } from 'sonner';

import { useResponse } from './ResponseContext';

export default function Response() {
  const { response, clearResponse } = useResponse();
  useEffect(() => {
    switch (Number(response?.status)) {

      case 200:
        // toast.success(response.message);
        console.log(response.message)
        break;

      case 201:
        toast.success(response.message);
        break;
      case 422: {

        let renderDetail: React.ReactNode;
        const detail = response.detail ?? (response as any).details ?? response.message;

        if (typeof detail === 'string') {
          renderDetail = detail;
        } else if (Array.isArray(detail)) {
          renderDetail = (
            <ul className="list-disc pl-4 text-xs">
              {(detail as any[]).map((err, i) => (
                <li key={i}>{err.message || JSON.stringify(err)}</li>
              ))}
            </ul>
          );
        } else {
          renderDetail = JSON.stringify(detail);
        }

        toast.error(response.error || 'Erro de validação', {
          description: renderDetail,
        });
        break;
      }
      case 400:
        toast.error(response.error, {
          description: response.message,
        });
        break;
      case 404:
        toast.error(response.error, {
          description: response.message || response.detail,
        });
        break;
      case 600:
        toast.error(response.error, {
          description: response.message,
        });
        break;
    }
  }, [response, clearResponse]);
  return <div></div>;
}
