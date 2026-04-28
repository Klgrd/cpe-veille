'use client';

import { PostCard } from '@/components/feed/PostCard';
import { useAuth } from '@/hooks/useAuth';
import { useBookmarks } from '@/hooks/useBookmarks';
import type { Post } from '@/types';

export function BookmarkWrapper({ post }: { post: Post }) {
  const { user } = useAuth();
  const { bookmarkedIds, toggle } = useBookmarks(user?.id ?? null);

  return (
    <PostCard
      post={post}
      isBookmarked={bookmarkedIds.has(post.id)}
      onBookmarkToggle={toggle}
      userId={user?.id ?? null}
    />
  );
}
