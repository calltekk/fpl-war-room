type ClubBadgeProps = {
  shortName: string;
  size?: "sm" | "md" | "lg";
};

const sizeClasses = {
  sm: "h-8 w-8 text-[10px]",
  md: "h-11 w-11 text-xs",
  lg: "h-14 w-14 text-sm",
};

export function ClubBadge({
  shortName,
  size = "md",
}: ClubBadgeProps) {
  return (
    <div
      className={[
        "flex shrink-0 items-center justify-center rounded-2xl",
        "border border-white/10 bg-white/10 font-black",
        "tracking-wide text-emerald-300 shadow-inner",
        sizeClasses[size],
      ].join(" ")}
    >
      {shortName}
    </div>
  );
}
