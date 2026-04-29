'use client';

import { useEffect, useRef, useCallback, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { PostCard } from './PostCard';
import { PostSkeleton } from '@/components/ui/Skeleton';
import { useAuth } from '@/hooks/useAuth';
import { useBookmarks } from '@/hooks/useBookmarks';
import type { Post } from '@/types';
import { Newspaper } from 'lucide-react';

const PAGE_SIZE = 10;

export function PostFeed() {
  const supabase = createClient();
  const { user } = useAuth();
  const { bookmarkedIds, toggle } = useBookmarks(user?.id ?? null);

  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const loaderRef = useRef<HTMLDivElement>(null);

  const loadPosts = useCallback(
    async (pageIndex: number) => {
      setLoading(true);
      const from = pageIndex * PAGE_SIZE;
      const to = from + PAGE_SIZE - 1;

      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .order('published_at', { ascending: false })
        .range(from, to);

      if (!error && data) {
        setPosts((prev) => (pageIndex === 0 ? data : [...prev, ...data]));
        setHasMore(data.length === PAGE_SIZE);
      }
      setLoading(false);
    },
    [supabase],
  );

  useEffect(() => {
    loadPosts(0);
  }, [loadPosts]);

  // Infinite scroll observer
  useEffect(() => {
    const el = loaderRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          const nextPage = page + 1;
          setPage(nextPage);
          loadPosts(nextPage);
        }
      },
      { threshold: 0.1 },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [hasMore, loading, page, loadPosts]);

  if (!loading && posts.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 text-center px-4">
        <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4">
          <Newspaper size={28} className="text-slate-500" />
        </div>
        <h3 className="text-lg font-semibold text-slate-300 mb-2">Aucun article pour le moment</h3>
        <p className="text-sm text-slate-500 max-w-xs">
          Le scraper n&apos;a pas encore détecté de nouveaux contenus liés au concours CPE. Revenez demain !
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {posts.map((post, i) => (
        <div
          key={post.id}
          className="animate-fade-in-up"
          style={{ animationDelay: `${Math.min(i, 5) * 60}ms` }}
        >
          <PostCard
            post={post}
            isBookmarked={bookmarkedIds.has(post.id)}
            onBookmarkToggle={toggle}
            userId={user?.id ?? null}
          />
        </div>
      ))}

      {/* Infinite scroll trigger */}
      <div ref={loaderRef} className="space-y-4">
        {loading &&
          Array.from({ length: 3 }).map((_, i) => <PostSkeleton key={i} />)}
      </div>

      {!hasMore && posts.length > 0 && (
        <p className="text-center text-slate-600 text-sm py-6">
          — Vous avez tout vu —
        </p>
      )}
    </div>
  );
}
