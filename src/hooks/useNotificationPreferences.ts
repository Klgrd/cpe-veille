'use client';

import { useState, useEffect, useCallback } from 'react';
import { createClient } from '@/lib/supabase/client';

export function useNotificationPreferences(userId: string | null) {
  const supabase = createClient();
  const [enabled, setEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fetched, setFetched] = useState(false);

  // Fetch the current preference from Supabase
  const fetchPreference = useCallback(async () => {
    if (!userId) return;
    setLoading(true);
    const { data } = await supabase
      .from('user_preferences')
      .select('email_notifications')
      .eq('user_id', userId)
      .maybeSingle();

    if (data) {
      setEnabled(data.email_notifications);
    }
    setFetched(true);
    setLoading(false);
  }, [userId, supabase]);

  useEffect(() => {
    fetchPreference();
  }, [fetchPreference]);

  // Toggle the preference (upsert)
  const toggle = async () => {
    if (!userId || loading) return;
    const next = !enabled;
    setEnabled(next); // Optimistic update
    setLoading(true);

    const { error } = await supabase
      .from('user_preferences')
      .upsert(
        { user_id: userId, email_notifications: next, updated_at: new Date().toISOString() },
        { onConflict: 'user_id' }
      );

    if (error) {
      console.error('Failed to update notification preference:', error);
      setEnabled(!next); // Revert on error
    }
    setLoading(false);
  };

  return { enabled, loading, fetched, toggle };
}
