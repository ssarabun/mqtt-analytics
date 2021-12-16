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
INSERT INTO "counter_value_min" VALUES(19,1,'2021-12-16 14:25',0);
INSERT INTO "counter_value_min" VALUES(24,1,'2021-12-16 14:26',0);
INSERT INTO "counter_value_min" VALUES(27,1,'2021-12-16 14:29',0);
INSERT INTO "counter_value_min" VALUES(30,1,'2021-12-16 14:30',0);
INSERT INTO "counter_value_min" VALUES(33,1,'2021-12-16 14:31',0);
INSERT INTO "counter_value_min" VALUES(36,1,'2021-12-16 14:32',0);
INSERT INTO "counter_value_min" VALUES(39,1,'2021-12-16 14:33',0);
INSERT INTO "counter_value_min" VALUES(42,1,'2021-12-16 14:34',0);
INSERT INTO "counter_value_min" VALUES(45,1,'2021-12-16 14:35',0);
INSERT INTO "counter_value_min" VALUES(48,1,'2021-12-16 14:36',0);
INSERT INTO "counter_value_min" VALUES(51,1,'2021-12-16 14:37',0);
INSERT INTO "counter_value_min" VALUES(54,1,'2021-12-16 14:38',0);
INSERT INTO "counter_value_min" VALUES(57,1,'2021-12-16 14:39',0);
INSERT INTO "counter_value_min" VALUES(60,1,'2021-12-16 14:40',0);
INSERT INTO "counter_value_min" VALUES(63,1,'2021-12-16 14:41',0);
INSERT INTO "counter_value_min" VALUES(66,1,'2021-12-16 14:42',0);
INSERT INTO "counter_value_min" VALUES(69,1,'2021-12-16 14:43',0);
INSERT INTO "counter_value_min" VALUES(72,1,'2021-12-16 14:44',0);
INSERT INTO "counter_value_min" VALUES(75,1,'2021-12-16 14:45',0);
INSERT INTO "counter_value_min" VALUES(78,1,'2021-12-16 14:46',0);
INSERT INTO "counter_value_min" VALUES(81,1,'2021-12-16 14:47',0);
INSERT INTO "counter_value_min" VALUES(84,1,'2021-12-16 14:48',0);
INSERT INTO "counter_value_min" VALUES(87,1,'2021-12-16 14:49',0);
INSERT INTO "counter_value_min" VALUES(90,1,'2021-12-16 14:50',0);
INSERT INTO "counter_value_min" VALUES(93,1,'2021-12-16 14:51',0);
INSERT INTO "counter_value_min" VALUES(96,1,'2021-12-16 14:52',0);
INSERT INTO "counter_value_min" VALUES(99,1,'2021-12-16 14:53',0);
INSERT INTO "counter_value_min" VALUES(102,1,'2021-12-16 14:54',0);
INSERT INTO "counter_value_min" VALUES(105,1,'2021-12-16 14:55',0);
INSERT INTO "counter_value_min" VALUES(108,1,'2021-12-16 14:56',0);
INSERT INTO "counter_value_min" VALUES(111,1,'2021-12-16 14:57',0);
INSERT INTO "counter_value_min" VALUES(114,1,'2021-12-16 14:58',0);
INSERT INTO "counter_value_min" VALUES(117,1,'2021-12-16 14:59',0);
INSERT INTO "counter_value_min" VALUES(120,1,'2021-12-16 15:00',0);
INSERT INTO "counter_value_min" VALUES(123,1,'2021-12-16 15:01',0);
INSERT INTO "counter_value_min" VALUES(134,1,'2021-12-16 15:24',0);
INSERT INTO "counter_value_min" VALUES(143,1,'2021-12-16 15:25',0);
INSERT INTO "counter_value_min" VALUES(166,1,'2021-12-16 15:26',0);
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
INSERT INTO "counter_value_raw" VALUES(167,1,'2021-12-16 15:27:00',0);
COMMIT;
