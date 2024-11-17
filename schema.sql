CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE boards (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    board_id INTEGER REFERENCES boards,
    sent_at TIMESTAMP
);

