'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useAuth } from '@/hooks/useAuth';
import { PostCard } from '@/components/feed/PostCard';
import { PostSkeleton } from '@/components/ui/Skeleton';
import { useBookmarks } from '@/hooks/useBookmarks';
import type { Post } from '@/types';
import { Bookmark as BookmarkIcon } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function BookmarksPage() {
  const supabase = createClient();
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const { bookmarkedIds, toggle } = useBookmarks(user?.id ?? null);
  
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/auth/login');
      return;
    }

    if (user) {
      const fetchBookmarks = async () => {
        setLoading(true);
        const { data, error } = await supabase
          .from('bookmarks')
          .select('posts(*)')
          .eq('user_id', user.id)
          .order('created_at', { ascending: false });

        if (!error && data) {
          // Flatten the response since post data is nested
          const validPosts = data
            .map((b) => b.posts)
            .filter((p): p is Post => p !== null);
          setPosts(validPosts);
        }
        setLoading(false);
      };

      fetchBookmarks();
    }
  }, [user, authLoading, router, supabase]);

  if (authLoading || loading) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-8 space-y-4">
        <div className="h-8 bg-slate-800 rounded w-48 mb-8 animate-pulse" />
        {Array.from({ length: 3 }).map((_, i) => (
          <PostSkeleton key={i} />
        ))}
      </div>
    );
  }

  // Filter out posts that have been optimistically removed from bookmarks
  const displayPosts = posts.filter((p) => bookmarkedIds.has(p.id));

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="mb-8 animate-fade-in-up">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <BookmarkIcon className="text-indigo-400" size={32} />
          Mes Favoris
        </h1>
        <p className="text-slate-400 mt-2">
          Retrouvez ici tous les articles que vous avez sauvegardés.
        </p>
      </div>

      {displayPosts.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 text-center px-4 bg-slate-900/50 rounded-2xl border border-slate-800">
          <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4">
            <BookmarkIcon size={28} className="text-slate-500" />
          </div>
          <h3 className="text-lg font-semibold text-slate-300 mb-2">Aucun favori</h3>
          <p className="text-sm text-slate-500 max-w-xs">
            Vous n'avez pas encore sauvegardé d'article. Explorez le feed pour trouver du contenu intéressant.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {displayPosts.map((post, i) => (
            <div
              key={post.id}
              className="animate-fade-in-up"
              style={{ animationDelay: `${Math.min(i, 5) * 60}ms` }}
            >
              <PostCard
                post={post}
                isBookmarked={true}
                onBookmarkToggle={toggle}
                userId={user?.id ?? null}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
