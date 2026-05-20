import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";

export type PCertidaoSavePayload = Omit<PCertidaoInterface, "certidao_id"> & {
  certidao_id?: number;
};

export function isPCertidaoSaveResult(value: unknown): value is PCertidaoInterface {
  return Boolean(
    value &&
      typeof value === "object" &&
      "certidao_id" in (value as Record<string, unknown>) &&
      typeof (value as Record<string, unknown>).certidao_id === "number",
  );
}
