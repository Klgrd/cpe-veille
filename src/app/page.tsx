import { PostFeed } from '@/components/feed/PostFeed';

export default function Home() {
  return (
    <div className="max-w-2xl mx-auto px-4">
      {/* Header section */}
      <div className="py-8 animate-fade-in-up">
        <h1 className="text-3xl font-semibold text-white mb-3">
          L'essentiel pour le concours CPE
        </h1>
        <p className="text-[#a3a3a3] text-sm leading-relaxed max-w-xl">
          Veille informationnelle automatisée (BOEN, Légifrance, Café Pédagogique). 
          Les textes officiels et actualités éducatives résumés par IA pour optimiser vos révisions.
        </p>
      </div>

      {/* Feed */}
      <PostFeed />
    </div>
  );
}
