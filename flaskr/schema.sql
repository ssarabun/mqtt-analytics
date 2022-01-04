BEGIN TRANSACTION;
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


INSERT INTO "counter" VALUES(1,'test.key',30,1.0,NULL,0,NULL,1);


CREATE TABLE counter_value_day
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER NOT NULL,
    created       DATE    NOT NULL,
    counter_value INTEGER NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


CREATE TABLE counter_value_hour
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER   NOT NULL,
    created       TIMESTAMP NOT NULL,
    counter_value INTEGER   NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


CREATE TABLE counter_value_min
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER   NOT NULL,
    created       TIMESTAMP NOT NULL,
    counter_value INTEGER   NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


CREATE TABLE counter_value_month
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER NOT NULL,
    created       DATE    NOT NULL,
    counter_value INTEGER NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


CREATE TABLE counter_value_raw
(
    id            INTEGER PRIMARY KEY,
    counter_id    INTEGER   NOT NULL,
    created       TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    counter_value INTEGER   NOT NULL,
    FOREIGN KEY (counter_id) REFERENCES counter (counter_id)
);


COMMIT;