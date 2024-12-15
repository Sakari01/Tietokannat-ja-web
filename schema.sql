CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    zone_id INT REFERENCES zones(id) ON DELETE CASCADE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    board_id INTEGER REFERENCES boards(id) ON DELETE CASCADE,
    sent_at TIMESTAMP
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    board_id INT REFERENCES boards(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

