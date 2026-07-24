ALTER TABLE bronze.fpl_players
    ADD COLUMN IF NOT EXISTS player_code INTEGER,
    ADD COLUMN IF NOT EXISTS photo_filename TEXT;
