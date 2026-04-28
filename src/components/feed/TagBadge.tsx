'use client';

import type { Tag } from '@/types';
import { TAG_COLORS } from '@/lib/utils';

interface TagBadgeProps {
  tag: Tag;
}

export function TagBadge({ tag }: TagBadgeProps) {
  const colorClass = TAG_COLORS[tag] ?? 'bg-slate-500/20 text-slate-300 border-slate-500/30';

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${colorClass} transition-all duration-200`}
    >
      {tag}
    </span>
  );
}
