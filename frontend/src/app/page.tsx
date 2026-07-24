import type { ReactNode } from "react";
import { Activity, Database, Trophy, Users } from "lucide-react";

import { FixtureRuns } from "@/components/dashboard/fixture-runs";
import { PlayerTargetCard } from "@/components/dashboard/player-target-card";
import { RecommendationPanels } from "@/components/dashboard/recommendation-panels";
import { Sidebar } from "@/components/layout/sidebar";
import {
  getCaptainProjections,
  getDataRefreshStatus,
  getDifferentials,
  getPlayerProjections,
  getTeamFixtureSummary,
} from "@/lib/api";

export default async function Home() {
  const [
    players,
    captains,
    differentials,
    fixtureRuns,
    refreshStatus,
  ] =
    await Promise.all([
      getPlayerProjections(20),
      getCaptainProjections(5),
      getDifferentials(10),
      getTeamFixtureSummary(),
      getDataRefreshStatus(),
    ]);

  const topPlayers = players.slice(0, 4);

  const refreshedAt = refreshStatus.last_successful_refresh
    ? new Intl.DateTimeFormat("en-GB", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "Europe/London",
      }).format(new Date(refreshStatus.last_successful_refresh))
    : "Not yet refreshed";

  return (
    <main className="min-h-screen bg-[#091423] text-white">
      <div className="flex min-h-screen">
        <Sidebar />

        <div className="min-w-0 flex-1">
          <header className="border-b border-white/10 bg-[#0b1727]/85 px-6 py-5 backdrop-blur xl:px-10">
            <div className="mx-auto flex max-w-[1500px] items-center justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.22em] text-emerald-300">
                  Command Centre
                </p>
                <h1 className="mt-1 text-2xl font-black">
                  Pre-season intelligence
                </h1>
              </div>

              <div className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
                Last refreshed: {refreshedAt}
              </div>
            </div>
          </header>

          <div className="mx-auto max-w-[1500px] space-y-8 px-6 py-8 xl:px-10">
            <section className="overflow-hidden rounded-[2rem] border border-white/10 bg-gradient-to-r from-violet-600/35 via-[#172749] to-emerald-500/15 p-8">
              <p className="text-xs font-black uppercase tracking-[0.24em] text-emerald-300">
                Fantasy Premier League intelligence
              </p>

              <h2 className="mt-4 max-w-4xl text-4xl font-black tracking-tight md:text-5xl">
                Make decisions with data. Beat your brothers with evidence.
              </h2>

              <p className="mt-4 max-w-3xl text-base leading-7 text-slate-300">
                Fixture analysis, projected points, captaincy recommendations
                and low-owned transfer targets from your end-to-end data
                platform.
              </p>
            </section>

            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <SummaryCard
                label="Players modelled"
                value={players.length.toString()}
                icon={<Database className="h-5 w-5" />}
              />
              <SummaryCard
                label="Clubs analysed"
                value={fixtureRuns.length.toString()}
                icon={<Users className="h-5 w-5" />}
              />
              <SummaryCard
                label="Top 5-GW projection"
                value={topPlayers[0]?.expected_points_next_5.toFixed(1) ?? "—"}
                icon={<Activity className="h-5 w-5" />}
              />
              <SummaryCard
                label="Captain projection"
                value={captains[0]?.captain_points_next_3.toFixed(1) ?? "—"}
                icon={<Trophy className="h-5 w-5" />}
              />
            </section>

            <section>
              <div className="mb-5">
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-300">
                  Model recommendations
                </p>
                <h2 className="mt-2 text-3xl font-black">
                  Top projected targets
                </h2>
                <p className="mt-2 text-sm text-slate-400">
                  Baseline projection across each player&apos;s next five
                  fixtures.
                </p>
              </div>

              <div className="grid gap-5 md:grid-cols-2 2xl:grid-cols-4">
                {topPlayers.map((player) => (
                  <PlayerTargetCard
                    key={player.player_id}
                    player={player}
                  />
                ))}
              </div>
            </section>

            <RecommendationPanels
              captains={captains}
              differentials={differentials}
            />

            <FixtureRuns teams={fixtureRuns} />
          </div>
        </div>
      </div>
    </main>
  );
}

function SummaryCard({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon: ReactNode;
}) {
  return (
    <article className="rounded-3xl border border-white/10 bg-[#0d1929] p-5">
      <div className="w-fit rounded-xl bg-white/5 p-2 text-emerald-300">
        {icon}
      </div>

      <p className="mt-5 text-sm text-slate-400">{label}</p>
      <p className="mt-1 text-3xl font-black text-white">{value}</p>
    </article>
  );
}
