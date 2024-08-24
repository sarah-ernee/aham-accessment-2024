CREATE TABLE IF NOT EXISTS manager (
  id INT GENERATED ALWAYS AS IDENTITY,
  manager_name text,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS fund (
  id INT GENERATED ALWAYS AS IDENTITY,
  fund_id varchar NOT NULL,
  fund_name text NOT NULL,
  description text,
  net_asset float NOT NULL,
  created_at timestamp without time zone NOT NULL DEFAULT (now()),
  performance float NOT NULL,
  manager_id int,
  PRIMARY KEY (id),
  CONSTRAINT manager_id FOREIGN KEY (manager_id) REFERENCES manager (id)
);

-- Parent table with manager as the entity
-- One to many relationship, one manager can manage multiple funds

-- Child table with fund as the entity
-- Avoid repetition of manager_name and store it as manager_id instead