CREATE TABLE restaurant (
  id serial PRIMARY KEY,
  name varchar
);

CREATE TABLE reviewer (
  id serial PRIMARY KEY,
  name varchar,
  karma integer
);

CREATE TABLE review (
  id serial PRIMARY KEY,
  title varchar,
  content varchar,
  stars integer CHECK (stars > 0 and stars <=5),
  reviewer_id integer NOT NULL REFERENCES reviewer (id),
  restaurant_id integer NOT NULL REFERENCES restaurant (id)
);
