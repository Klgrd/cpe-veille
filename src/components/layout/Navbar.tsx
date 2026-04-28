'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Newspaper, Bookmark, LogIn, LogOut, User } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

export function Navbar() {
  const { user, loading, signOut } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const handleSignOut = async () => {
    await signOut();
    router.push('/');
    router.refresh();
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-[var(--border)] bg-black/40 backdrop-blur-xl">
      <div className="max-w-2xl mx-auto px-4 h-14 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 rounded bg-white flex items-center justify-center transition-all duration-300">
            <span className="text-black text-sm font-bold">C</span>
          </div>
          <span className="font-bold text-white hidden sm:block">
            CPE Veille
          </span>
        </Link>

        {/* Nav links – desktop */}
        <nav className="hidden sm:flex items-center gap-1">
          <Link
            href="/"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
              pathname === '/'
                ? 'bg-neutral-900 text-white'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <Newspaper size={15} />
            Feed
          </Link>
          {user && (
            <Link
              href="/bookmarks"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                pathname === '/bookmarks'
                  ? 'bg-neutral-900 text-white'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              <Bookmark size={15} />
              Favoris
            </Link>
          )}
        </nav>

        {/* Auth */}
        <div className="flex items-center gap-2">
          {!loading && (
            <>
              {user ? (
                <div className="flex items-center gap-2">
                  <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 text-neutral-400 text-xs">
                    <User size={13} />
                    <span className="max-w-[120px] truncate">{user.email}</span>
                  </div>
                  <button
                    onClick={handleSignOut}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm text-neutral-400 hover:text-white transition-all duration-200"
                  >
                    <LogOut size={15} />
                    <span className="hidden sm:block">Déconnexion</span>
                  </button>
                </div>
              ) : (
                <Link
                  href="/auth/login"
                  className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-white hover:bg-neutral-200 text-black text-sm font-medium transition-all duration-200"
                >
                  <LogIn size={15} />
                  Connexion
                </Link>
              )}
            </>
          )}
        </div>
      </div>
    </header>
  );
}
