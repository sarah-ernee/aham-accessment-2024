BEGIN;

CREATE TEMPORARY TABLE temp_fund_data (
    fund_id VARCHAR,
    fund_name TEXT,
    manager_name TEXT,
    description TEXT,
    net_asset FLOAT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    performance FLOAT
);

--- Use CSV converted from JSON since Postgres cannot COPY JSON format
--- !IMPORTANT: replace absolute path to CSV with your local machine path to try out
COPY 
    temp_fund_data
FROM 
    'C:/Users/Sarah/Downloads/Miscellaneous/Affin Hwang (AHAM)/aham-accessment-2024/temp_db.csv'
WITH 
    (FORMAT csv, HEADER true)
;

--- Account for non-nullable float values
UPDATE temp_fund_data
SET 
    net_asset = COALESCE(NULLIF(net_asset::TEXT, '')::FLOAT, 0.0),
    performance = COALESCE(NULLIF(performance::TEXT, '')::FLOAT, 0.0)
WHERE 
    net_asset IS NULL OR performance IS NULL;
;

--- Migrate parent table data first
INSERT INTO 
    manager (manager_name)
SELECT DISTINCT 
    manager_name
FROM 
    temp_fund_data
;

--- Supply foreign key and migrate data
INSERT INTO 
    fund (fund_id, fund_name, description, net_asset, created_at, performance, manager_id)
SELECT 
    b.fund_id,
    b.fund_name,
    b.description,
    b.net_asset,
    b.created_at,
    b.performance,
    a.id AS manager_id
FROM 
    temp_fund_data b
LEFT JOIN 
    manager a
ON 
    b.manager_name = a.manager_name
ORDER BY
    b.fund_id
;

--- Cleanup
DROP TABLE IF EXISTS temp_fund_data;

COMMIT;
