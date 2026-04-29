'use client';

import { Bookmark, ExternalLink } from 'lucide-react';
import Link from 'next/link';
import type { Post } from '@/types';
import { TagBadge } from './TagBadge';
import { ShareButton } from '@/components/ui/ShareButton';
import { formatDate } from '@/lib/utils';

interface PostCardProps {
  post: Post;
  isBookmarked: boolean;
  onBookmarkToggle: (postId: string) => void;
  userId: string | null;
}

const SOURCE_ICONS: Record<string, string> = {
  'BOEN': '📚',
  'Légifrance': '⚖️',
  'Café Pédagogique': '☕',
  'MEN': '🏫',
};

export function PostCard({ post, isBookmarked, onBookmarkToggle, userId }: PostCardProps) {
  const icon = post.source_name ? SOURCE_ICONS[post.source_name] ?? '📰' : '📰';

  return (
    <article className="group bg-[var(--surface)] backdrop-blur-md border border-[var(--border)] hover:border-[var(--border-hover)] rounded-xl p-5 transition-all duration-200">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3 min-w-0">
          <div className="w-9 h-9 rounded-full bg-[var(--surface)] border border-[var(--border)] flex items-center justify-center text-sm shrink-0">
            {icon}
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-[var(--text-secondary)] truncate">
              {post.source_name ?? 'Veille CPE'}
            </p>
            <time
              dateTime={post.published_at}
              className="text-xs text-[var(--text-muted)]"
            >
              {formatDate(post.published_at)}
            </time>
          </div>
        </div>
      </div>

      {/* Title */}
      <Link href={`/post/${post.id}`}>
        <h2 className="text-lg font-bold text-[var(--text-primary)] mb-2 leading-snug hover:text-[var(--text-secondary)] transition-colors duration-200 cursor-pointer line-clamp-2">
          {post.title}
        </h2>
      </Link>

      {/* Description */}
      <p className="text-sm text-[var(--text-muted)] leading-relaxed mb-4 line-clamp-3">
        {post.description}
      </p>

      {/* Tags */}
      {post.tags && post.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-4">
          {post.tags.map((tag) => (
            <TagBadge key={tag} tag={tag} />
          ))}
        </div>
      )}

      {/* Source links */}
      {post.source_url && post.source_url.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {post.source_url.slice(0, 2).map((url, i) => (
            <a
              key={i}
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] underline-offset-2 hover:underline transition-colors duration-200"
            >
              <ExternalLink size={12} />
              Source {post.source_url.length > 1 ? i + 1 : ''}
            </a>
          ))}
        </div>
      )}

      {/* Divider */}
      <div className="h-px bg-[var(--border)] mb-3" />

      {/* Actions */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => {
            if (!userId) {
              window.location.href = '/auth/login';
              return;
            }
            onBookmarkToggle(post.id);
          }}
          className={`flex items-center gap-1.5 text-sm transition-all duration-200 group/bm ${
            isBookmarked
              ? 'text-[#a1ff00] dark:text-[#a1ff00]'
              : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
          }`}
          aria-label={isBookmarked ? 'Retirer des favoris' : 'Sauvegarder dans les favoris'}
        >
          <Bookmark
            size={16}
            className={`transition-all duration-200 group-hover/bm:scale-110 ${
              isBookmarked ? 'fill-[#a1ff00]' : ''
            }`}
          />
          <span>{isBookmarked ? 'Sauvegardé' : 'Sauvegarder'}</span>
        </button>

        <ShareButton postId={post.id} title={post.title} />
      </div>
    </article>
  );
}
