export function PostSkeleton() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-full bg-slate-800" />
        <div className="flex-1 space-y-2">
          <div className="h-3 bg-slate-800 rounded w-1/3" />
          <div className="h-2 bg-slate-800 rounded w-1/5" />
        </div>
      </div>
      <div className="space-y-2 mb-4">
        <div className="h-4 bg-slate-800 rounded w-3/4" />
        <div className="h-3 bg-slate-800 rounded w-full" />
        <div className="h-3 bg-slate-800 rounded w-5/6" />
        <div className="h-3 bg-slate-800 rounded w-2/3" />
      </div>
      <div className="flex gap-2 mb-4">
        <div className="h-5 bg-slate-800 rounded-full w-16" />
        <div className="h-5 bg-slate-800 rounded-full w-20" />
      </div>
      <div className="h-px bg-slate-800 mb-3" />
      <div className="flex gap-4">
        <div className="h-4 bg-slate-800 rounded w-12" />
        <div className="h-4 bg-slate-800 rounded w-12" />
      </div>
    </div>
  );
}
