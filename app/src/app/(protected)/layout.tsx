import { ProtestoAppShell } from "@/components/protesto/protesto-app-shell";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return <ProtestoAppShell>{children}</ProtestoAppShell>;
}
