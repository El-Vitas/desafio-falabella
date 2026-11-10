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

CREATE INDEX IF NOT EXISTS pokemon_types_type_id_idx ON pokemon_types (type_id);
