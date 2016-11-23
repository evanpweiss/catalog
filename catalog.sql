-- Drop database if it exists so that we may recreate it
\c postgres;
DROP DATABASE IF EXISTS catalog;

-- Initialize database and connect to it
CREATE DATABASE catalog;
\c catalog;

-- Create tables
CREATE TABLE users (
    id serial PRIMARY KEY,
    name text,
    email text
    );

CREATE TABLE categories (
    id serial PRIMARY KEY,
    name text
    );

CREATE TABLE item_table (
    id serial PRIMARY KEY,
    name text,
    description text,
    category_id integer REFERENCES categories,
    user_id integer REFERENCES users
    );

-- Pre-populate categories and items
INSERT INTO categories (name) VALUES ('Speakers');
INSERT INTO categories (name) VALUES ('Receivers');
INSERT INTO categories (name) VALUES ('Cables');
INSERT INTO categories (name) VALUES ('Televisions');
INSERT INTO categories (name) VALUES ('Projectors');
INSERT INTO categories (name) VALUES ('Screens');
INSERT INTO categories (name) VALUES ('Bluray Players');
INSERT INTO categories (name) VALUES ('Game Consoles');
INSERT INTO categories (name) VALUES ('Furniture');
INSERT INTO categories (name) VALUES ('Media');