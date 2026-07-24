import { ArrowUpRight } from "lucide-react";

import { ClubBadge } from "@/components/shared/club-badge";
import { PlayerImage } from "@/components/shared/player-image";
import type { PlayerProjection } from "@/types/fpl";

type PlayerTargetCardProps = {
  player: PlayerProjection;
};

export function PlayerTargetCard({
  player,
}: PlayerTargetCardProps) {
  return (
    <article className="group rounded-3xl border border-white/10 bg-gradient-to-br from-violet-500/15 via-[#111f31] to-[#0c1726] p-5">
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-center gap-4">
          <PlayerImage
            imageUrl={player.player_image_url}
            playerName={player.web_name}
            teamShortName={player.team_short_name}
            badgeUrl={player.badge_url}
          />

          <div className="min-w-0">
            <p className="text-xs font-bold uppercase tracking-widest text-emerald-300">
              #{player.expected_points_rank_overall} target
            </p>

            <h3 className="mt-1 truncate text-xl font-black text-white">
              {player.web_name}
            </h3>

            <div className="mt-2 flex items-center gap-2">
              <ClubBadge
                shortName={player.team_short_name}
                badgeUrl={player.badge_url}
                size="sm"
              />

              <p className="truncate text-sm text-slate-400">
                {player.team_name} · {player.position_short_name}
              </p>
            </div>
          </div>
        </div>

        <ArrowUpRight className="h-5 w-5 shrink-0 text-slate-500" />
      </div>

      <div className="mt-6 grid grid-cols-3 gap-2">
        <Metric
          label="5-GW xPts"
          value={player.expected_points_next_5.toFixed(1)}
        />
        <Metric
          label="Price"
          value={`£${player.current_price.toFixed(1)}m`}
        />
        <Metric
          label="FDR"
          value={player.average_difficulty_next_5.toFixed(2)}
        />
      </div>

      <div className="mt-5 border-t border-white/10 pt-4">
        <p className="text-xs font-bold uppercase tracking-widest text-slate-500">
          Next five
        </p>
        <p className="mt-2 text-sm leading-6 text-slate-300">
          {player.next_five_opponents}
        </p>
      </div>
    </article>
  );
}

function Metric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl bg-white/[0.045] px-2 py-3 text-center">
      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
        {label}
      </p>
      <p className="mt-1 text-base font-black text-emerald-300">
        {value}
      </p>
    </div>
  );
}
