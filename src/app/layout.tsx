import type { Metadata, Viewport } from 'next';
import './globals.css';
import { Navbar } from '@/components/layout/Navbar';
import { BottomNav } from '@/components/layout/BottomNav';

export const metadata: Metadata = {
  title: 'CPE Veille — Révisions Concours CPE',
  description:
    'Plateforme de veille informationnelle automatisée dédiée aux révisions du concours de Conseiller Principal d\'Éducation (CPE) en France. Retrouvez les derniers décrets, circulaires et actualités du BOEN, Légifrance et Café Pédagogique.',
  keywords: ['CPE', 'concours', 'Conseiller Principal d\'Éducation', 'BOEN', 'vie scolaire', 'révisions'],
  robots: 'index, follow',
  openGraph: {
    title: 'CPE Veille',
    description: 'Veille informationnelle automatisée pour le concours CPE',
    type: 'website',
  },
};

export const viewport: Viewport = {
  themeColor: '#0a0a0f',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" className="dark">
      <body>
        <Navbar />
        <main className="pt-14 pb-20 sm:pb-6 min-h-screen">
          {children}
        </main>
        <BottomNav />
      </body>
    </html>
  );
}
