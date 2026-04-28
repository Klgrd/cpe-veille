export type Tag =
  | 'Décret'
  | 'Circulaire'
  | 'Arrêté'
  | 'Pédagogie'
  | 'Vie scolaire'
  | 'Actualité'
  | 'Harcèlement'
  | 'Absentéisme'
  | 'Formation'
  | 'Numérique'
  | 'Inclusion'
  | 'Orientation';

export interface Post {
  id: string;
  title: string;
  description: string;
  source_url: string[];
  tags: Tag[];
  published_at: string;
  created_at: string;
  source_name: string | null;
  source_id: string | null;
}

export interface Bookmark {
  id: string;
  user_id: string;
  post_id: string;
  created_at: string;
  posts?: Post;
}
