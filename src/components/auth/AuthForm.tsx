'use client';

import { useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { useRouter } from 'next/navigation';
import { Loader2, Mail, Lock } from 'lucide-react';
import Link from 'next/link';

interface AuthFormProps {
  view: 'login' | 'register';
}

export function AuthForm({ view }: AuthFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const router = useRouter();
  const supabase = createClient();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = view === 'login'
      ? await supabase.auth.signInWithPassword({ email, password })
      : await supabase.auth.signUp({ email, password });

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      router.push('/');
      router.refresh();
    }
  };

  const handleGoogleLogin = async () => {
    setLoading(true);
    setError(null);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-8 bg-[var(--surface)] border border-[var(--border)] rounded-[2rem] shadow-xl backdrop-blur-xl animate-fade-in-up">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-extrabold text-[var(--text-primary)] mb-2 tracking-tight">
          {view === 'login' ? 'Bon retour !' : 'Créer un compte'}
        </h2>
        <p className="text-sm text-[var(--text-secondary)]">
          {view === 'login' 
            ? 'Connectez-vous pour accéder à vos favoris.' 
            : 'Rejoignez-nous pour sauvegarder vos articles.'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-sm text-red-400 text-center">
            {error}
          </div>
        )}

        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-[var(--text-secondary)] ml-2 uppercase tracking-wider">Email</label>
          <div className="relative">
            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--text-muted)]" size={18} />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="votre@email.com"
              className="w-full bg-black/5 dark:bg-white/5 border border-[var(--border)] rounded-full py-3.5 pl-12 pr-4 text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:border-[var(--text-secondary)] transition-all"
            />
          </div>
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-[var(--text-secondary)] ml-2 uppercase tracking-wider">Mot de passe</label>
          <div className="relative">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--text-muted)]" size={18} />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              minLength={6}
              className="w-full bg-black/5 dark:bg-white/5 border border-[var(--border)] rounded-full py-3.5 pl-12 pr-4 text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:outline-none focus:border-[var(--text-secondary)] transition-all"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 py-3.5 bg-gradient-to-r from-[#eaff66] to-[#a1ff00] hover:opacity-90 active:scale-[0.98] text-black text-sm font-bold rounded-full transition-all disabled:opacity-50 disabled:pointer-events-none mt-8 shadow-[0_0_20px_rgba(161,255,0,0.3)]"
        >
          {loading && <Loader2 size={16} className="animate-spin" />}
          {view === 'login' ? 'Se connecter' : "S'inscrire"}
        </button>
      </form>

      <div className="relative my-8">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-[var(--border)]"></div>
        </div>
        <div className="relative flex justify-center text-xs">
          <span className="bg-[var(--background)] px-4 rounded-full text-[var(--text-muted)] font-medium">Ou continuer avec</span>
        </div>
      </div>

      <button
        onClick={handleGoogleLogin}
        disabled={loading}
        className="w-full flex items-center justify-center gap-2 py-3.5 bg-white dark:bg-neutral-800 hover:bg-neutral-100 dark:hover:bg-neutral-700 active:scale-[0.98] text-black dark:text-white text-sm font-bold rounded-full transition-all disabled:opacity-50 disabled:pointer-events-none shadow-sm border border-neutral-200 dark:border-neutral-700"
      >
        <svg className="w-5 h-5" viewBox="0 0 24 24">
          <path
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            fill="#4285F4"
          />
          <path
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            fill="#34A853"
          />
          <path
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            fill="#FBBC05"
          />
          <path
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            fill="#EA4335"
          />
        </svg>
        Google
      </button>

      <div className="mt-8 text-center text-sm text-[var(--text-muted)]">
        {view === 'login' ? (
          <p>
            Pas encore de compte ?{' '}
            <Link href="/auth/register" className="text-[var(--text-primary)] hover:text-[#a1ff00] font-bold transition-colors">
              S'inscrire
            </Link>
          </p>
        ) : (
          <p>
            Déjà un compte ?{' '}
            <Link href="/auth/login" className="text-[var(--text-primary)] hover:text-[#a1ff00] font-bold transition-colors">
              Se connecter
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
