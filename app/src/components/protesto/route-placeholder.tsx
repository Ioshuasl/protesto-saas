export function RoutePlaceholder({ title }: { title: string }) {
  return (
    <div className="text-muted-foreground p-8 text-center">
      <h1 className="text-foreground mb-2 text-2xl font-semibold">{title}</h1>
      <p>Página em construção (migrada do protótipo).</p>
    </div>
  );
}
