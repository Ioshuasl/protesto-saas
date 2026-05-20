import { PTituloForm } from "@/packages/administrativo/components/PTitulo";

export default async function TituloByIdPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <PTituloForm id={id} />;
}
