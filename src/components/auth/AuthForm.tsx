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
    <div className="w-full max-w-md mx-auto p-6 bg-slate-900/50 border border-slate-800 rounded-2xl shadow-xl backdrop-blur-sm animate-fade-in-up">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">
          {view === 'login' ? 'Bon retour !' : 'Créer un compte'}
        </h2>
        <p className="text-sm text-slate-400">
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

        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-400 ml-1">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="votre@email.com"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-400 ml-1">Mot de passe</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              minLength={6}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 py-2.5 bg-indigo-500 hover:bg-indigo-600 active:scale-[0.98] text-white text-sm font-semibold rounded-xl transition-all disabled:opacity-50 disabled:pointer-events-none mt-6 shadow-lg shadow-indigo-500/20"
        >
          {loading && <Loader2 size={16} className="animate-spin" />}
          {view === 'login' ? 'Se connecter' : "S'inscrire"}
        </button>
      </form>

      <div className="mt-6 text-center text-sm text-slate-400">
        {view === 'login' ? (
          <p>
            Pas encore de compte ?{' '}
            <Link href="/auth/register" className="text-indigo-400 hover:text-indigo-300 font-medium">
              S'inscrire
            </Link>
          </p>
        ) : (
          <p>
            Déjà un compte ?{' '}
            <Link href="/auth/login" className="text-indigo-400 hover:text-indigo-300 font-medium">
              Se connecter
            </Link>
          </p>
        )}
      </div>
    </div>
  );
}
