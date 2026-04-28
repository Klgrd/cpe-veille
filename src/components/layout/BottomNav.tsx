'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Newspaper, Bookmark, LogIn } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export function BottomNav() {
  const { user } = useAuth();
  const pathname = usePathname();

  const links = [
    { href: '/', icon: Newspaper, label: 'Feed', always: true },
    { href: '/bookmarks', icon: Bookmark, label: 'Favoris', always: false },
    { href: '/auth/login', icon: LogIn, label: 'Connexion', always: false, authOnly: false },
  ];

  const visibleLinks = links.filter((l) => {
    if (l.href === '/bookmarks') return !!user;
    if (l.href === '/auth/login') return !user;
    return true;
  });

  return (
    <nav className="sm:hidden fixed bottom-0 left-0 right-0 z-50 bg-black/40 backdrop-blur-xl border-t border-[var(--border)] safe-area-pb">
      <div className="flex items-center justify-around h-16 px-2">
        {visibleLinks.map(({ href, icon: Icon, label }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex flex-col items-center justify-center gap-1 flex-1 h-full transition-all duration-200 ${
                active ? 'text-indigo-400' : 'text-slate-500 hover:text-slate-300'
              }`}
            >
              <div
                className={`p-1.5 rounded-xl transition-all duration-200 ${
                  active ? 'bg-indigo-500/15' : ''
                }`}
              >
                <Icon size={20} strokeWidth={active ? 2.5 : 1.8} />
              </div>
              <span className="text-[10px] font-medium">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
