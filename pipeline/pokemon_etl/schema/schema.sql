CREATE TABLE IF NOT EXISTS types (
    id   INTEGER PRIMARY KEY CHECK (id > 0),
    name TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS pokemon (
    id              INTEGER PRIMARY KEY CHECK (id > 0),
    name            TEXT    NOT NULL,
    height          INTEGER NOT NULL CHECK (height >= 0),
    weight          INTEGER NOT NULL CHECK (weight >= 0),
    base_experience INTEGER CHECK (base_experience >= 0),
    sprite          TEXT
);

CREATE TABLE IF NOT EXISTS pokemon_types (
    pokemon_id INTEGER NOT NULL REFERENCES pokemon (id),
    type_id    INTEGER NOT NULL REFERENCES types (id),
    slot       INTEGER NOT NULL CHECK (slot > 0),
    PRIMARY KEY (pokemon_id, type_id),
    UNIQUE (pokemon_id, slot)
);

CREATE TABLE IF NOT EXISTS trainers (
    id         INTEGER PRIMARY KEY CHECK (id > 0),
    name       TEXT    NOT NULL,
    region     TEXT    NOT NULL,
    created_at DATE    NOT NULL
);

CREATE TABLE IF NOT EXISTS captures (
    id          INTEGER   PRIMARY KEY CHECK (id > 0),
    trainer_id  INTEGER   NOT NULL REFERENCES trainers (id),
    pokemon_id  INTEGER   NOT NULL REFERENCES pokemon (id),
    captured_at TIMESTAMP NOT NULL,
    level       INTEGER   NOT NULL CHECK (level BETWEEN 1 AND 100),
    location    TEXT      NOT NULL
);

CREATE TABLE IF NOT EXISTS battles (
    id               INTEGER   PRIMARY KEY CHECK (id > 0),
    pokemon_a_id     INTEGER   NOT NULL REFERENCES pokemon (id),
    pokemon_b_id     INTEGER   NOT NULL REFERENCES pokemon (id),
    winner_id        INTEGER   NOT NULL REFERENCES pokemon (id),
    fought_at        TIMESTAMP NOT NULL,
    duration_seconds INTEGER   NOT NULL,
    CHECK (pokemon_a_id <> pokemon_b_id),
    CHECK (winner_id IN (pokemon_a_id, pokemon_b_id))
);

CREATE INDEX IF NOT EXISTS pokemon_types_type_id_idx ON pokemon_types (type_id);
CREATE INDEX IF NOT EXISTS captures_trainer_id_idx ON captures (trainer_id);
CREATE INDEX IF NOT EXISTS captures_pokemon_id_idx ON captures (pokemon_id);
