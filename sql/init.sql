drop table messages cascade;
drop table users cascade;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(64) UNIQUE NOT NULL,
  password VARCHAR NOT NULL,
  description VARCHAR(256),
  timestamp timestamp default current_timestamp
);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  parent_id INTEGER REFERENCES messages(id),
  message VARCHAR(256),
  timestamp timestamp default current_timestamp
);

INSERT INTO users ("email", "password") VALUES ('123', '123');
INSERT INTO users ("email", "password") VALUES ('hello@hello.com', '123');
INSERT INTO users ("email", "password") VALUES ('hello@world.com', '123');

INSERT INTO messages ("user_id", message) VALUES (1, 'Foo baar lorem');
INSERT INTO messages ("user_id", message) VALUES (2, 'Bar foo foo');
INSERT INTO messages ("user_id", message, "parent_id") VALUES (2, 'Bar foo foo', 1);
