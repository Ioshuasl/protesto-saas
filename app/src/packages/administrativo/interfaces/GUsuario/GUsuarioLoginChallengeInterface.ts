/** Payload retornado no primeiro passo de authenticate quando two_factor_required é true */
export default interface GUsuarioLoginChallengeInterface {
  usuario_id: number;
  nome: string | null;
  email: string;
  two_factor_required: boolean;
  challenge_expires_in: number;
}
