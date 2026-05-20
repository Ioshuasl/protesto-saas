import withClientErrorHandlerInterface from './withClientErrorHandlerInterface';

/**
 * Códigos de erro que começam com 6, são do front entd, na ordem do alfabeto o F de frontend é a sexta letra
 */
export function withClientErrorHandler<T extends (...args: any[]) => Promise<any>>(action: T) {
  return async (...args: Parameters<T>): Promise<withClientErrorHandlerInterface> => {
    try {
      // Executa a função definida
      const data = await action(...args);
      // Retorna exatamente a mesma resposta retornada pela função
      return data;
    } catch (error: any) {
      // Retorna o erro de execuçãformatado
      return {
        status: 600,
        message: error?.message || 'Erro interno do servidor',
        data: error,
      };
    }
  };
}
