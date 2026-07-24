import type { ReactNode } from "react";
import { Crown, Swords } from "lucide-react";

import type {
  CaptainProjection,
  DifferentialProjection,
} from "@/types/fpl";

type Props = {
  captains: CaptainProjection[];
  differentials: DifferentialProjection[];
};

export function RecommendationPanels({
  captains,
  differentials,
}: Props) {
  return (
    <div className="grid gap-6 xl:grid-cols-2">
      <Panel title="Captain picks" icon={<Crown className="h-5 w-5" />}>
        {captains.map((player) => (
          <Row
            key={player.captain_rank}
            rank={player.captain_rank}
            name={player.web_name}
            description={player.team_name}
            value={player.captain_points_next_3.toFixed(1)}
          />
        ))}
      </Panel>

      <Panel
        title="Differential targets"
        icon={<Swords className="h-5 w-5" />}
      >
        {differentials.slice(0, 5).map((player) => (
          <Row
            key={player.differential_rank}
            rank={player.differential_rank}
            name={player.web_name}
            description={`${player.team_name} · ${player.selected_by_percent.toFixed(1)}% owned`}
            value={player.expected_points_next_5.toFixed(1)}
          />
        ))}
      </Panel>
    </div>
  );
}

function Row({
  rank,
  name,
  description,
  value,
}: {
  rank: number;
  name: string;
  description: string;
  value: string;
}) {
  return (
    <div className="grid grid-cols-[2rem_1fr_auto] items-center gap-3 border-b border-white/5 py-3 last:border-0">
      <span className="text-sm font-black text-emerald-300">
        {rank}
      </span>
      <div className="min-w-0">
        <p className="truncate font-bold text-white">{name}</p>
        <p className="truncate text-xs text-slate-500">
          {description}
        </p>
      </div>
      <p className="font-black text-white">{value}</p>
    </div>
  );
}

function Panel({
  title,
  icon,
  children,
}: {
  title: string;
  icon: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="rounded-3xl border border-white/10 bg-[#0d1929] p-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-white/5 p-2 text-emerald-300">
          {icon}
        </div>
        <h2 className="text-xl font-black text-white">{title}</h2>
      </div>
      <div className="mt-5">{children}</div>
    </section>
  );
}
