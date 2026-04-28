import { createClient } from '@/lib/supabase/server';
import { notFound } from 'next/navigation';
import { PostCard } from '@/components/feed/PostCard';
import { BookmarkWrapper } from './BookmarkWrapper';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default async function PostPage(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;
  const supabase = await createClient();

  // Fetch post details
  const { data: post, error } = await supabase
    .from('posts')
    .select('*')
    .eq('id', params.id)
    .single();

  if (error || !post) {
    notFound();
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white mb-6 transition-colors duration-200"
      >
        <ArrowLeft size={16} />
        Retour au feed
      </Link>
      
      <div className="animate-fade-in-up">
        <BookmarkWrapper post={post} />
      </div>
    </div>
  );
}
