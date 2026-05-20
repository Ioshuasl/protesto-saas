/** Atraso artificial para simular rede (mock / `db.json`). */
export function mockDbDelay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
