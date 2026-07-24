"use client";

import Image from "next/image";
import { useState } from "react";

import { ClubBadge } from "@/components/shared/club-badge";

type PlayerImageProps = {
  imageUrl: string | null;
  playerName: string;
  teamShortName: string;
  badgeUrl: string | null;
};

export function PlayerImage({
  imageUrl,
  playerName,
  teamShortName,
  badgeUrl,
}: PlayerImageProps) {
  const [failed, setFailed] = useState(false);

  if (!imageUrl || failed) {
    return (
      <ClubBadge
        shortName={teamShortName}
        badgeUrl={badgeUrl}
        size="lg"
      />
    );
  }

  return (
    <div className="relative h-20 w-20 shrink-0 overflow-hidden rounded-2xl border border-white/10 bg-white/5">
      <Image
        src={imageUrl}
        alt={playerName}
        fill
        sizes="80px"
        className="object-contain object-bottom"
        onError={() => setFailed(true)}
      />
    </div>
  );
}
