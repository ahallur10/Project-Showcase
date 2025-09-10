DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS deposits;
DROP TABLE IF EXISTS tutorials;
DROP TABLE IF EXISTS progress;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL
);

CREATE TABLE deposits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  amount_usd REAL NOT NULL DEFAULT 10.0,
  refund_eligible INTEGER DEFAULT 0,
  consumed INTEGER DEFAULT 0,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE tutorials (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE,
  title TEXT
);

CREATE TABLE progress (
  user_id INTEGER,
  tutorial_id INTEGER,
  percent REAL,
  PRIMARY KEY (user_id, tutorial_id)
);
