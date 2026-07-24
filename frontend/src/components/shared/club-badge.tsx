"use client";

import Image from "next/image";
import { useState } from "react";

type ClubBadgeProps = {
  shortName: string;
  badgeUrl?: string | null;
  size?: "sm" | "md" | "lg";
};

const sizeClasses = {
  sm: "h-8 w-8",
  md: "h-11 w-11",
  lg: "h-14 w-14",
};

const textClasses = {
  sm: "text-[10px]",
  md: "text-xs",
  lg: "text-sm",
};

export function ClubBadge({
  shortName,
  badgeUrl,
  size = "md",
}: ClubBadgeProps) {
  const [failed, setFailed] = useState(false);

  if (!badgeUrl || failed) {
    return (
      <div
        className={[
          "flex shrink-0 items-center justify-center rounded-2xl",
          "border border-white/10 bg-white/10 font-black",
          "tracking-wide text-emerald-300 shadow-inner",
          sizeClasses[size],
          textClasses[size],
        ].join(" ")}
      >
        {shortName}
      </div>
    );
  }

  return (
    <div
      className={[
        "relative shrink-0 overflow-hidden rounded-2xl",
        "border border-white/10 bg-white/5 p-1.5",
        sizeClasses[size],
      ].join(" ")}
    >
      <Image
        src={badgeUrl}
        alt={`${shortName} badge`}
        fill
        sizes="56px"
        className="object-contain p-1"
        onError={() => setFailed(true)}
      />
    </div>
  );
}
