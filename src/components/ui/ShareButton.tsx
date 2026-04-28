'use client';

import { Share2 } from 'lucide-react';

interface ShareButtonProps {
  postId: string;
  title: string;
}

export function ShareButton({ postId, title }: ShareButtonProps) {
  const handleShare = async () => {
    const url = `${window.location.origin}/post/${postId}`;

    if (navigator.share) {
      try {
        await navigator.share({ title, url });
      } catch {
        // User cancelled, do nothing
      }
    } else {
      await navigator.clipboard.writeText(url);
      // Brief visual feedback via DOM (no state needed)
      const btn = document.getElementById(`share-btn-${postId}`);
      if (btn) {
        btn.textContent = 'Lien copié !';
        setTimeout(() => {
          btn.innerHTML = '';
          btn.appendChild(document.createTextNode('Partager'));
        }, 2000);
      }
    }
  };

  return (
    <button
      id={`share-btn-${postId}`}
      onClick={handleShare}
      className="flex items-center gap-1.5 text-slate-400 hover:text-sky-400 text-sm transition-colors duration-200 group"
      aria-label="Partager ce post"
    >
      <Share2
        size={16}
        className="group-hover:scale-110 transition-transform duration-200"
      />
      <span>Partager</span>
    </button>
  );
}
