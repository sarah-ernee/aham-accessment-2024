-- Parent table with manager as the entity
-- One to many relationship, one manager can manage multiple funds
CREATE TABLE manager IF NOT EXISTS (
  id INT GENERATED ALWAYS AS IDENTITY,
  manager_name text,
  PRIMARY KEY (id)
);

-- Child table with fund as the entity
-- Avoid repetition of manager_name and store it as manager_id instead
CREATE TABLE fund IF NOT EXISTS (
  id INT GENERATED ALWAYS AS IDENTITY,
  fund_id varchar NOT NULL,
  fund_name text NOT NULL,
  desc text,
  net_asset float NOT NULL,
  created_at timestamp NOT NULL DEFAULT (now()),
  performance float NOT NULL,
  manager_id int,
  PRIMARY KEY (id),
  CONSTRAINT manager_id FOREIGN KEY (manager_id) REFERENCES manager (id)
);

