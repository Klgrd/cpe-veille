'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { LogOut, User, Sun, Moon } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';

export function Navbar() {
  const { user, loading, signOut } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleSignOut = async () => {
    await signOut();
    router.push('/');
    router.refresh();
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
        <div className="flex items-center justify-between h-16 rounded-full bg-[var(--surface)] backdrop-blur-xl border border-[var(--border)] px-6 shadow-sm">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <span className="font-bold text-lg tracking-tight">CPE Veille</span>
          </Link>

          {/* Nav links – desktop */}
          <nav className="hidden sm:flex items-center gap-1">
            <Link
              href="/"
              className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                pathname === '/'
                  ? 'bg-neutral-800/10 dark:bg-white/10 text-neutral-900 dark:text-white'
                  : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'
              }`}
            >
              Feed
            </Link>
            {user && (
              <Link
                href="/bookmarks"
                className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                  pathname === '/bookmarks'
                    ? 'bg-neutral-800/10 dark:bg-white/10 text-neutral-900 dark:text-white'
                    : 'text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'
                }`}
              >
                Favoris
              </Link>
            )}
          </nav>

          {/* Actions & Auth */}
          <div className="flex items-center gap-3">
            {mounted && (
              <button
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className="p-2 rounded-full hover:bg-neutral-200 dark:hover:bg-white/10 transition-colors"
                aria-label="Toggle theme"
              >
                {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
              </button>
            )}

            {!loading && (
              <>
                {user ? (
                  <div className="flex items-center gap-2">
                    <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-neutral-500 dark:text-neutral-400 text-xs">
                      <User size={14} />
                      <span className="max-w-[120px] truncate">{user.email}</span>
                    </div>
                    <button
                      onClick={handleSignOut}
                      className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm border border-[var(--border)] hover:bg-neutral-200 dark:hover:bg-white/10 transition-all duration-200"
                    >
                      <span className="hidden sm:block">Déconnexion</span>
                      <LogOut size={14} className="sm:hidden" />
                    </button>
                  </div>
                ) : (
                  <Link
                    href="/auth/login"
                    className="flex items-center gap-1.5 px-5 py-2 rounded-full bg-transparent border border-[var(--border)] hover:bg-neutral-200 dark:hover:bg-white/10 text-sm font-medium transition-all duration-200"
                  >
                    Connexion
                  </Link>
                )}
              </>
            )}
          </div>

        </div>
      </div>
    </header>
  );
}
