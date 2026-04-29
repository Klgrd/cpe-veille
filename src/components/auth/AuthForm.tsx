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
