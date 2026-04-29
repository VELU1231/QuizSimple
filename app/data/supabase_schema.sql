-- Run this in Supabase SQL editor
-- Creates leaderboard table for QuizSimple backend.

create table if not exists public.quiz_scores (
  id bigserial primary key,
  quiz_id text not null,
  name text not null,
  score integer not null check (score >= 0),
  max_score integer not null check (max_score >= 0),
  created_at timestamptz not null default now()
);

create index if not exists idx_quiz_scores_quiz_id_score
  on public.quiz_scores (quiz_id, score desc, created_at asc);

alter table public.quiz_scores enable row level security;

-- Public read access for leaderboard API (anon/authenticated via Data API).
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

-- Writes should happen only from server using service role.
-- No insert/update/delete policies for anon/authenticated.
