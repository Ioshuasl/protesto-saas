'use client';

import React, { createContext, ReactNode, useCallback, useContext, useMemo, useState } from 'react';

interface ResponseState {
  message?: string;
  type?: 'toast' | 'modal' | 'alert' | null;
  status?: number;
  error?: string;
  detail?: string;
}

interface ResponseContextProps {
  response: ResponseState;
  setResponse: (value: ResponseState) => void;
  clearResponse: () => void;
}

const ResponseContext = createContext<ResponseContextProps | undefined>(undefined);

export const ResponseProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [response, setResponseState] = useState<ResponseState>({
    message: '',
    type: null,
    status: 0,
  });

  const setResponse = useCallback((value: ResponseState) => setResponseState(value), []);
  const clearResponse = useCallback(
    () => setResponseState({ message: '', type: null, status: 0 }),
    [],
  );

  const value = useMemo(
    () => ({ response, setResponse, clearResponse }),
    [response, setResponse, clearResponse],
  );

  return <ResponseContext.Provider value={value}>{children}</ResponseContext.Provider>;
};

export const useResponse = () => {
  const context = useContext(ResponseContext);
  if (!context) throw new Error('useResponse must be used within ResponseProvider');
  return context;
};
