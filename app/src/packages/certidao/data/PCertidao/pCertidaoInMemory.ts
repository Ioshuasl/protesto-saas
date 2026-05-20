import db from "@/db.json";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";

const dbRecord = db as Record<string, unknown>;
const certidaoSeed = (dbRecord.certidoes as PCertidaoInterface[] | undefined) ?? [];

export const pCertidaoListRef: { current: PCertidaoInterface[] } = {
  current: [...certidaoSeed],
};
