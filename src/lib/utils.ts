import type { Tag } from '@/types';

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffHours < 1) return "À l'instant";
  if (diffHours < 24) return `Il y a ${diffHours}h`;
  if (diffDays < 7) return `Il y a ${diffDays}j`;

  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

export const TAG_COLORS: Record<Tag, string> = {
  'Décret': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Circulaire': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Arrêté': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Pédagogie': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Vie scolaire': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Actualité': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Harcèlement': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Absentéisme': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Formation': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Numérique': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Inclusion': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
  'Orientation': 'bg-[#171717] text-[#e5e5e5] border-[#262626]',
};

export const TAGS_LIST: Tag[] = Object.keys(TAG_COLORS) as Tag[];
