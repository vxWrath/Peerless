CREATE TABLE players (
    id BIGINT NOT NULL PRIMARY KEY,
    blacklisted BOOL DEFAULT FALSE
);

CREATE TABLE leagues (
    id BIGINT NOT NULL PRIMARY KEY,
    teams JSONB DEFAULT '{}'::JSONB
);

CREATE TABLE player_leagues (
    player_id BIGINT REFERENCES players(id) ON DELETE CASCADE,
    league_id BIGINT REFERENCES leagues(id) ON DELETE CASCADE,
    demands INTEGER,
    PRIMARY KEY (player_id, league_id)
);