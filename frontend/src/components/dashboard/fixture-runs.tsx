import { ClubBadge } from "@/components/shared/club-badge";
import type { TeamFixtureSummary } from "@/types/fpl";

type Props = {
  teams: TeamFixtureSummary[];
};

export function FixtureRuns({ teams }: Props) {
  return (
    <section className="rounded-3xl border border-white/10 bg-[#0d1929] p-6">
      <h2 className="text-2xl font-black text-white">
        Best fixture runs
      </h2>

      <div className="mt-6 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {teams.slice(0, 8).map((team, index) => (
          <article
            key={team.team_id}
            className="rounded-2xl border border-white/5 bg-white/[0.035] p-4"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex min-w-0 items-center gap-3">
                <ClubBadge
                  shortName={team.team_short_name}
                  badgeUrl={team.badge_url}
                  size="md"
                />

                <div className="min-w-0">
                  <span className="text-xs font-black text-violet-300">
                    #{index + 1}
                  </span>

                  <h3 className="truncate font-black text-white">
                    {team.team_name}
                  </h3>
                </div>
              </div>

              <span className="rounded-full bg-emerald-400/10 px-2 py-1 text-xs font-black text-emerald-300">
                {team.average_difficulty_next_five.toFixed(2)}
              </span>
            </div>

            <p className="mt-4 text-xs leading-5 text-slate-400">
              {team.next_five_opponents}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
