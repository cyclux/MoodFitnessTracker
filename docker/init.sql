\c moodfit_db;

CREATE TABLE diary (
  date DATE PRIMARY KEY,
  tasks INTEGER[],
  sleep FLOAT,
  bodybattery_min INTEGER,
  bodybattery_max INTEGER,
  steps INTEGER,
  body INTEGER,
  psyche INTEGER,
  dizzy BOOLEAN,
  comment TEXT
);
