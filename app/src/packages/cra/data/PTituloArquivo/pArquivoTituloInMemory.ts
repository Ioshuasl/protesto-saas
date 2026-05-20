import db from "@/db.json";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";

export const pArquivoTituloListRef: { current: PArquivoTituloInterface[] } = {
  current: [...((db.arquivos_titulo as unknown as PArquivoTituloInterface[]) ?? [])],
};
