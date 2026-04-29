'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { LogOut, User, Sun, Moon, Bell, BellOff, ChevronDown } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useTheme } from 'next-themes';
import { useEffect, useRef, useState } from 'react';
import { useNotificationPreferences } from '@/hooks/useNotificationPreferences';

export function Navbar() {
  const { user, loading, signOut } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const { enabled: notifEnabled, loading: notifLoading, fetched: notifFetched, toggle: toggleNotif } =
    useNotificationPreferences(user?.id ?? null);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSignOut = async () => {
    setDropdownOpen(false);
    await signOut();
    router.push('/');
    router.refresh();
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
        <div className="flex items-center justify-between h-16 rounded-full bg-[var(--surface)] backdrop-blur-xl border border-[var(--border)] px-6 shadow-md">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <span className="font-bold text-lg tracking-tight text-[var(--text-primary)]">CPE Veille</span>
          </Link>

          {/* Nav links – desktop */}
          <nav className="hidden sm:flex items-center gap-1">
            <Link
              href="/"
              className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                pathname === '/'
                  ? 'bg-neutral-900 dark:bg-white text-white dark:text-black'
                  : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-neutral-200 dark:hover:bg-white/10'
              }`}
            >
              Feed
            </Link>
            {user && (
              <Link
                href="/bookmarks"
                className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                  pathname === '/bookmarks'
                    ? 'bg-neutral-900 dark:bg-white text-white dark:text-black'
                    : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-neutral-200 dark:hover:bg-white/10'
                }`}
              >
                Favoris
              </Link>
            )}
          </nav>

          {/* Actions & Auth */}
          <div className="flex items-center gap-3">
            {/* Theme toggle */}
            {mounted && (
              <button
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className="p-2 rounded-full text-[var(--text-secondary)] hover:bg-neutral-200 dark:hover:bg-white/10 hover:text-[var(--text-primary)] transition-colors"
                aria-label="Toggle theme"
              >
                {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
              </button>
            )}

            {!loading && (
              <>
                {user ? (
                  /* Profile dropdown */
                  <div className="relative" ref={dropdownRef}>
                    <button
                      onClick={() => setDropdownOpen((o) => !o)}
                      className="flex items-center gap-2 px-3 py-2 rounded-full text-sm font-medium text-[var(--text-secondary)] border border-[var(--border)] hover:bg-neutral-200 dark:hover:bg-white/10 hover:text-[var(--text-primary)] transition-all duration-200"
                    >
                      <User size={14} />
                      <span className="hidden sm:block max-w-[100px] truncate text-xs">{user.email}</span>
                      <ChevronDown
                        size={14}
                        className={`transition-transform duration-200 ${dropdownOpen ? 'rotate-180' : ''}`}
                      />
                    </button>

                    {/* Dropdown panel */}
                    {dropdownOpen && (
                      <div className="absolute right-0 mt-2 w-64 rounded-2xl bg-[var(--surface)] backdrop-blur-xl border border-[var(--border)] shadow-xl overflow-hidden animate-fade-in-up">
                        {/* Notification toggle */}
                        <div className="px-4 py-3 border-b border-[var(--border)]">
                          <p className="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider mb-2">
                            Notifications
                          </p>
                          <button
                            onClick={toggleNotif}
                            disabled={notifLoading || !notifFetched}
                            className="w-full flex items-center justify-between gap-3 group"
                          >
                            <div className="flex items-center gap-2 text-sm text-[var(--text-primary)]">
                              {notifEnabled
                                ? <Bell size={15} className="text-[#a1ff00]" />
                                : <BellOff size={15} className="text-[var(--text-muted)]" />
                              }
                              <span>Alertes email</span>
                            </div>
                            {/* Toggle switch */}
                            <div
                              className={`relative w-10 h-5 rounded-full transition-all duration-300 ${
                                notifEnabled
                                  ? 'bg-[#a1ff00]'
                                  : 'bg-neutral-300 dark:bg-neutral-600'
                              } ${notifLoading ? 'opacity-50' : ''}`}
                            >
                              <div
                                className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform duration-300 ${
                                  notifEnabled ? 'translate-x-5' : 'translate-x-0'
                                }`}
                              />
                            </div>
                          </button>
                          {notifEnabled && (
                            <p className="text-[10px] text-[var(--text-muted)] mt-1.5 leading-tight">
                              Tu recevras un email à <strong>{user.email}</strong> à chaque nouveau post.
                            </p>
                          )}
                        </div>

                        {/* Sign out */}
                        <button
                          onClick={handleSignOut}
                          className="w-full flex items-center gap-2 px-4 py-3 text-sm text-[var(--text-secondary)] hover:bg-neutral-100 dark:hover:bg-white/5 hover:text-red-500 transition-colors duration-150"
                        >
                          <LogOut size={14} />
                          Déconnexion
                        </button>
                      </div>
                    )}
                  </div>
                ) : (
                  <Link
                    href="/auth/login"
                    className="flex items-center gap-1.5 px-5 py-2 rounded-full text-sm font-semibold text-[var(--text-primary)] border border-[var(--border)] hover:bg-neutral-200 dark:hover:bg-white/10 transition-all duration-200"
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
