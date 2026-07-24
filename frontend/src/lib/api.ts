import type {
  CaptainProjection,
  DifferentialProjection,
  PlayerProjection,
  TeamFixtureSummary,
} from "@/types/fpl";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`,
    );
  }

  return (await response.json()) as T;
}

export function getPlayerProjections(
  limit = 20,
): Promise<PlayerProjection[]> {
  return fetchJson<PlayerProjection[]>(
    `/players/projections?limit=${limit}`,
  );
}

export function getCaptainProjections(
  limit = 5,
): Promise<CaptainProjection[]> {
  return fetchJson<CaptainProjection[]>(
    `/players/captains?limit=${limit}`,
  );
}

export function getDifferentials(
  limit = 10,
): Promise<DifferentialProjection[]> {
  return fetchJson<DifferentialProjection[]>(
    `/players/differentials?limit=${limit}`,
  );
}

export function getTeamFixtureSummary(): Promise<
  TeamFixtureSummary[]
> {
  return fetchJson<TeamFixtureSummary[]>(
    "/fixtures/team-summary",
  );
}
