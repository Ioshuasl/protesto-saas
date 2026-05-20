export default function SkeletonEditor() {
  return (
    <div className="bg-muted/30 flex h-full w-full animate-pulse flex-col">
      {/* Toolbar */}
      <div className="bg-background flex items-center gap-2 border-b px-4 py-3">
        <div className="bg-muted h-6 w-10 rounded" />
        <div className="bg-muted h-6 w-10 rounded" />
        <div className="bg-muted h-6 w-10 rounded" />
        <div className="bg-muted mx-2 h-6 w-px" />
        <div className="bg-muted h-6 w-14 rounded" />
        <div className="bg-muted h-6 w-14 rounded" />
      </div>

      {/* Ruler */}
      <div className="bg-background border-b px-6 py-2">
        <div className="bg-muted h-3 w-full rounded" />
      </div>

      {/* Editor area */}
      <div className="bg-muted/20 flex flex-1 justify-center overflow-auto p-6">
        <div className="bg-background w-full max-w-[800px] rounded-md p-8 shadow">
          {/* Fake text lines */}
          <div className="space-y-3">
            <div className="bg-muted h-4 w-3/4 rounded" />
            <div className="bg-muted h-4 w-full rounded" />
            <div className="bg-muted h-4 w-11/12 rounded" />
            <div className="bg-muted h-4 w-full rounded" />
            <div className="bg-muted h-4 w-2/3 rounded" />

            <div className="bg-muted mt-6 h-4 w-full rounded" />
            <div className="bg-muted h-4 w-10/12 rounded" />
            <div className="bg-muted h-4 w-full rounded" />
            <div className="bg-muted h-4 w-8/12 rounded" />
          </div>
        </div>
      </div>
    </div>
  );
}
