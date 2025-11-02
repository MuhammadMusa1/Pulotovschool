WITH benjamin_types AS (
    SELECT DISTINCT sculpture_type
    FROM Sheet1
    WHERE LOWER(master_id) = 'benjamin'
),
masters_with_wrong_types AS (
    SELECT DISTINCT LOWER(master_id) as master_name
    FROM Sheet1
    WHERE LOWER(master_id) != 'benjamin'
      AND sculpture_type NOT IN (SELECT sculpture_type FROM benjamin_types)
)
SELECT DISTINCT LOWER(master_id) as master_name
FROM Sheet1
WHERE LOWER(master_id) != 'benjamin'
  AND LOWER(master_id) NOT IN (SELECT master_name FROM masters_with_wrong_types)
  AND master_id IS NOT NULL
ORDER BY master_name;