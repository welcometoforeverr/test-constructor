-- CulinaryLab: схема базы данных ПР7
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    change_description TEXT NOT NULL,
    temperature INTEGER NOT NULL CHECK (temperature > 0),
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    experiment_date TEXT NOT NULL,
    is_cancelled INTEGER NOT NULL DEFAULT 0
        CHECK (is_cancelled IN (0, 1)),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

CREATE TABLE IF NOT EXISTS experiment_results (
    id INTEGER PRIMARY KEY,
    experiment_id INTEGER NOT NULL UNIQUE,
    taste_score INTEGER NOT NULL CHECK (taste_score BETWEEN 1 AND 10),
    status TEXT NOT NULL,
    FOREIGN KEY (experiment_id)
        REFERENCES experiments(id) ON DELETE CASCADE
);
