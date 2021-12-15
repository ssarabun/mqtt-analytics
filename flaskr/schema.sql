DROP TABLE IF EXISTS counter;

CREATE TABLE counter
(
    counter_id    INTEGER PRIMARY KEY,
    counter_key   TEXT    NOT NULL UNIQUE,
    interval      INTEGER NOT NULL,
    multiplicator REAL    NOT NULL DEFAULT (1),
    unit          TEXT,
    delta         BOOLEAN NOT NULL,
    delta_value   INTEGER,
    enabled       BOOLEAN NOT NULL
);

INSERT INTO counter (counter_key, interval, delta, enabled) VALUES ('test.key', 30, false, true);


DROP TABLE IF EXISTS counter_value_raw;

CREATE TABLE counter_value_raw
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER   NOT NULL,
    created       TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    counter_value INTEGER   NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


DROP TABLE IF EXISTS counter_value_min;

CREATE TABLE counter_value_min
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER   NOT NULL,
    created       TIMESTAMP NOT NULL,
    counter_value INTEGER   NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


DROP TABLE IF EXISTS counter_value_hour;

CREATE TABLE counter_value_hour
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER   NOT NULL,
    created       TIMESTAMP NOT NULL,
    counter_value INTEGER   NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


DROP TABLE IF EXISTS counter_value_day;

CREATE TABLE counter_value_day
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER NOT NULL,
    created       DATE    NOT NULL,
    counter_value INTEGER NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


DROP TABLE IF EXISTS counter_value_month;

CREATE TABLE counter_value_month
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER NOT NULL,
    created       DATE    NOT NULL,
    counter_value INTEGER NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);

