-- ═══════════════════════════════════════════════════════════════════════════
-- QuizSimple Supabase Schema Setup
-- ═══════════════════════════════════════════════════════════════════════════
-- 
-- INSTRUCTIONS:
-- 1. Go to your Supabase project dashboard
-- 2. Navigate to SQL Editor (left menu)
-- 3. Click "New Query"
-- 4. Copy entire contents of this file
-- 5. Click "Run" (green play button)
-- 6. Verify all queries execute successfully (no red errors)
-- 
-- This creates:
--  • quiz_scores table (leaderboard/results)
--  • Indexes for fast lookups
--  • Row-Level Security policies
--  • Service role permissions for backend
-- ═══════════════════════════════════════════════════════════════════════════

-- ───────────────────────────────────────────────────────────────────────────
-- 1. CREATE QUIZ SCORES TABLE (Leaderboard)
-- ───────────────────────────────────────────────────────────────────────────
create table if not exists public.quiz_scores (
  id bigserial primary key,
  quiz_id text not null,
  name text not null,
  score integer not null check (score >= 0),
  max_score integer not null check (max_score >= 0),
  created_at timestamptz not null default now()
);

comment on table public.quiz_scores is 'Stores quiz submission scores and leaderboard data';
comment on column public.quiz_scores.quiz_id is 'Unique identifier for the quiz (e.g., "html-101", "js-basics")';
comment on column public.quiz_scores.name is 'Player name as entered in quiz';
comment on column public.quiz_scores.score is 'Points earned by player';
comment on column public.quiz_scores.max_score is 'Maximum possible points for this quiz attempt';
comment on column public.quiz_scores.created_at is 'Timestamp when quiz was submitted';

-- ───────────────────────────────────────────────────────────────────────────
-- 2. CREATE INDEXES FOR PERFORMANCE
-- ───────────────────────────────────────────────────────────────────────────

-- Fast lookups by quiz_id with score ordering (for leaderboard queries)
create index if not exists idx_quiz_scores_quiz_id_score
  on public.quiz_scores (quiz_id, score desc, created_at asc);

-- Fast lookups by quiz_id only (for admin deletion, leaderboard filters)
create index if not exists idx_quiz_scores_quiz_id
  on public.quiz_scores (quiz_id);

-- Recent submissions (for monitoring)
create index if not exists idx_quiz_scores_created_at
  on public.quiz_scores (created_at desc);

-- ───────────────────────────────────────────────────────────────────────────
-- 3. ENABLE ROW LEVEL SECURITY
-- ───────────────────────────────────────────────────────────────────────────
alter table public.quiz_scores enable row level security;

-- ───────────────────────────────────────────────────────────────────────────
-- 4. CREATE RLS POLICIES
-- ───────────────────────────────────────────────────────────────────────────

-- Policy: PUBLIC READ (allow anyone to view leaderboard)
do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public'
      and tablename = 'quiz_scores'
      and policyname = 'quiz_scores_select_public'
  ) then
    create policy quiz_scores_select_public
      on public.quiz_scores
      for select
      to anon, authenticated
      using (true);
  end if;
end$$;

-- Policy: SERVICE ROLE ONLY (backend can insert/update/delete with service role key)
-- Note: Service role bypasses RLS, so no explicit policy needed,
-- but we make it explicit for clarity in security audit.
do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public'
      and tablename = 'quiz_scores'
      and policyname = 'quiz_scores_service_role_all'
  ) then
    create policy quiz_scores_service_role_all
      on public.quiz_scores
      for all
      to service_role
      using (true)
      with check (true);
  end if;
end$$;

-- ───────────────────────────────────────────────────────────────────────────
-- 5. GRANT PERMISSIONS
-- ───────────────────────────────────────────────────────────────────────────

-- Grant anonymous users SELECT only (for public leaderboard views)
grant select on public.quiz_scores to anon;

-- Grant authenticated users SELECT only (for logged-in users to view results)
grant select on public.quiz_scores to authenticated;

-- Service role already has full access (admin operations)
grant all on public.quiz_scores to service_role;

-- ═══════════════════════════════════════════════════════════════════════════
-- VERIFICATION & TESTING
-- ═══════════════════════════════════════════════════════════════════════════
-- After running this SQL, verify in Supabase dashboard:
-- 1. Go to Tables → public.quiz_scores (should exist)
-- 2. Go to Authentication → Users → Service Role (verify it has table access)
-- 3. Try inserting test data:
--    INSERT INTO public.quiz_scores (quiz_id, name, score, max_score) 
--    VALUES ('test-quiz', 'Test Player', 75, 100);
-- 4. Verify leaderboard query:
--    SELECT * FROM public.quiz_scores WHERE quiz_id = 'test-quiz' 
--    ORDER BY score DESC, created_at ASC LIMIT 10;
-- ═══════════════════════════════════════════════════════════════════════════
