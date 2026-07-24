import {
  BarChart3,
  CalendarDays,
  Crown,
  Goal,
  Shield,
  Swords,
  Users,
} from "lucide-react";

const navigation = [
  { label: "Command Centre", icon: BarChart3, active: true },
  { label: "My Squad", icon: Shield },
  { label: "Transfer Planner", icon: Swords },
  { label: "Captaincy", icon: Crown },
  { label: "Rivals", icon: Users },
  { label: "Fixtures", icon: CalendarDays },
];

export function Sidebar() {
  return (
    <aside className="hidden min-h-screen w-72 shrink-0 border-r border-white/10 bg-[#07111f] lg:block">
      <div className="sticky top-0 p-6">
        <div className="mb-10 flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-400 text-[#07111f]">
            <Goal className="h-6 w-6" />
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-[0.22em] text-emerald-300">
              FPL Intelligence
            </p>
            <h1 className="text-xl font-black text-white">
              War Room
            </h1>
          </div>
        </div>

        <nav className="space-y-2">
          {navigation.map(({ label, icon: Icon, active }) => (
            <button
              key={label}
              type="button"
              className={[
                "flex w-full items-center gap-3 rounded-xl px-4 py-3",
                "text-left text-sm font-semibold transition",
                active
                  ? "bg-violet-500 text-white"
                  : "text-slate-400 hover:bg-white/5 hover:text-white",
              ].join(" ")}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </nav>
      </div>
    </aside>
  );
}
