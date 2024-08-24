CREATE TEMPORARY TABLE temp_fund_data (
  data JSONB
);

-- Make sure file properties has Full Control allowed for everyone
COPY temp_fund_data(data) from 'C:/Users/Sarah/Downloads/Miscellaneous/Affin Hwang (AHAM)/aham-accessment-2024/temp_db.json';

INSERT INTO manager (manager_name)
SELECT DISTINCT data->>'manager_name'
FROM temp_fund_data;

DROP TABLE IF EXISTS temp_fund_data;
