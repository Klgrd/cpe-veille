-- Enable the UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Table: posts
CREATE TABLE posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  source_url TEXT[] NOT NULL,
  tags TEXT[] NOT NULL,
  published_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  source_name TEXT,
  source_id TEXT UNIQUE
);

-- Table: bookmarks
CREATE TABLE bookmarks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, post_id)
);

-- Indexes for performance
CREATE INDEX idx_posts_published_at ON posts(published_at DESC);
CREATE INDEX idx_bookmarks_user_id ON bookmarks(user_id);

-- Enable Row Level Security
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookmarks ENABLE ROW LEVEL SECURITY;

-- RLS Policies for `posts`
-- Everyone can read posts
CREATE POLICY "Public profiles are viewable by everyone." 
  ON posts FOR SELECT 
  USING ( true );

-- Only Service Role can insert/update/delete posts
CREATE POLICY "Service role can manage posts." 
  ON posts FOR ALL 
  USING ( auth.role() = 'service_role' )
  WITH CHECK ( auth.role() = 'service_role' );

-- RLS Policies for `bookmarks`
-- Users can only see their own bookmarks
CREATE POLICY "Users can view their own bookmarks." 
  ON bookmarks FOR SELECT 
  USING ( auth.uid() = user_id );

-- Users can insert their own bookmarks
CREATE POLICY "Users can insert their own bookmarks." 
  ON bookmarks FOR INSERT 
  WITH CHECK ( auth.uid() = user_id );

-- Users can delete their own bookmarks
CREATE POLICY "Users can delete their own bookmarks." 
  ON bookmarks FOR DELETE 
  USING ( auth.uid() = user_id );

-- ============================================================
-- Table: user_preferences
-- ============================================================
CREATE TABLE user_preferences (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,
  email_notifications BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Users can read their own preferences
CREATE POLICY "Users can view their own preferences."
  ON user_preferences FOR SELECT
  USING ( auth.uid() = user_id );

-- Users can insert their own preferences
CREATE POLICY "Users can insert their own preferences."
  ON user_preferences FOR INSERT
  WITH CHECK ( auth.uid() = user_id );

-- Users can update their own preferences
CREATE POLICY "Users can update their own preferences."
  ON user_preferences FOR UPDATE
  USING ( auth.uid() = user_id );

-- Service role can read all preferences (for the scraper to fetch subscribed emails)
CREATE POLICY "Service role can read all preferences."
  ON user_preferences FOR SELECT
  USING ( auth.role() = 'service_role' );

-- ============================================================
-- View: notification_subscribers
-- Returns emails of users who opted in for email notifications.
-- Only accessible via service_role (used by the scraper).
-- ============================================================
CREATE VIEW notification_subscribers AS
  SELECT au.email, up.user_id
  FROM user_preferences up
  JOIN auth.users au ON au.id = up.user_id
  WHERE up.email_notifications = TRUE;

