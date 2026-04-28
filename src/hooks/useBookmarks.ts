'use client';

import { useState, useEffect, useCallback } from 'react';
import { createClient } from '@/lib/supabase/client';

export function useBookmarks(userId: string | null) {
  const supabase = createClient();
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!userId) {
      setBookmarkedIds(new Set());
      return;
    }
    setLoading(true);
    supabase
      .from('bookmarks')
      .select('post_id')
      .eq('user_id', userId)
      .then(({ data }) => {
        if (data) setBookmarkedIds(new Set(data.map((b) => b.post_id)));
        setLoading(false);
      });
  }, [userId]); // eslint-disable-line react-hooks/exhaustive-deps

  const toggle = useCallback(
    async (postId: string) => {
      if (!userId) return;

      const isBookmarked = bookmarkedIds.has(postId);

      // Optimistic update
      setBookmarkedIds((prev) => {
        const next = new Set(prev);
        if (isBookmarked) next.delete(postId);
        else next.add(postId);
        return next;
      });

      const res = await fetch('/api/bookmarks', {
        method: isBookmarked ? 'DELETE' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ postId }),
      });

      if (!res.ok) {
        // Rollback
        setBookmarkedIds((prev) => {
          const next = new Set(prev);
          if (isBookmarked) next.add(postId);
          else next.delete(postId);
          return next;
        });
      }
    },
    [userId, bookmarkedIds],
  );

  return { bookmarkedIds, loading, toggle };
}
