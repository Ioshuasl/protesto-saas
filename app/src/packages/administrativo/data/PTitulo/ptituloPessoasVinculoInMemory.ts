import db from "@/db.json";
import type { PPessoaVinculoInterface } from "@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoInterface";

export const pPessoaVinculoListRef: { current: PPessoaVinculoInterface[] } = {
  current: [...(db.pessoas_vinculo as unknown as PPessoaVinculoInterface[])],
};

