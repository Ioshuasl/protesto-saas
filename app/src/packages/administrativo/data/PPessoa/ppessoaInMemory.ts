import db from "@/db.json";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";

/** Estado mutável em memória (substituir por API). */
export const ppessoaListRef: { current: PPessoaInterface[] } = {
  current: [...(db.pessoas || [])],
};
