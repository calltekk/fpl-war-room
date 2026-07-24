export type PlayerProjection = {
  player_id: number;
  web_name: string;
  team_name: string;
  team_short_name: string;
  position_short_name: string;
  current_price: number;
  selected_by_percent: number;
  expected_points_next_3: number;
  expected_points_next_5: number;
  expected_points_per_million: number;
  average_difficulty_next_5: number;
  next_five_opponents: string;
  expected_points_rank_overall: number;
};

export type CaptainProjection = {
  captain_rank: number;
  web_name: string;
  team_name: string;
  expected_points_next_3: number;
  captain_points_next_3: number;
  next_five_opponents: string;
};

export type DifferentialProjection = {
  differential_rank: number;
  web_name: string;
  team_name: string;
  position_short_name: string;
  current_price: number;
  selected_by_percent: number;
  expected_points_next_5: number;
  differential_score: number;
  next_five_opponents: string;
};

export type TeamFixtureSummary = {
  team_id: number;
  team_name: string;
  average_difficulty_next_five: number;
  next_five_opponents: string;
};
