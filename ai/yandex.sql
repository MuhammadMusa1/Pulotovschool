WITH cleaned AS (
    SELECT
        lower(trim(master_id))      AS master,
        lower(trim(sculpture_type)) AS stype
    FROM Sheet1
),
ben_types AS (
    SELECT DISTINCT stype
    FROM cleaned
    WHERE master = 'benjamin'
      AND stype IS NOT NULL
      AND stype <> ''
)
SELECT DISTINCT m.master
FROM (
    SELECT DISTINCT master
    FROM cleaned
    WHERE master IS NOT NULL AND master <> ''
) AS m
WHERE m.master <> 'benjamin'
  -- у мастера должен быть хотя бы один валидный тип
  AND EXISTS (
      SELECT 1
      FROM cleaned c1
      WHERE c1.master = m.master
        AND c1.stype IS NOT NULL
        AND c1.stype <> ''
  )
  -- у мастера нет типов, которых нет у Benjamin
  AND NOT EXISTS (
      SELECT 1
      FROM cleaned c2
      WHERE c2.master = m.master
        AND c2.stype IS NOT NULL
        AND c2.stype <> ''
        AND c2.stype NOT IN (SELECT stype FROM ben_types)
  )
ORDER BY m.master;
