import db from "@/db.json";
import type { PBancoInterface } from "@/packages/administrativo/interfaces/PBanco/PBancoInterface";

export const pbancoListRef: { current: PBancoInterface[] } = {
  current: [...(db.bancos || [])],
};
