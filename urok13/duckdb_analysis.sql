-- =========================================================
-- DuckDB analysis: Transfers to external wallets
-- Source: Excel files
-- Period: September – November
-- =========================================================


-- =========================
-- 0. Enable Excel extension
-- =========================
INSTALL excel;
LOAD excel;


-- =========================
-- 1. Preview source files
-- =========================

-- Clients file preview
SELECT *
FROM read_xlsx('D:/duckdb/data/clients.xlsx')
LIMIT 5;

DESCRIBE
SELECT *
FROM read_xlsx('D:/duckdb/data/clients.xlsx');


-- Transfers file preview (example: September)
SELECT *
FROM read_xlsx(
  'D:/duckdb/data/transfers.xlsx',
  sheet = 'september',
  all_varchar = true
)
LIMIT 5;


-- =========================
-- 2. Create CLIENTS table
-- =========================

DROP TABLE IF EXISTS clients;

CREATE TABLE clients AS
SELECT DISTINCT
  CAST("номер кошелека" AS BIGINT)::VARCHAR AS wallet_id
FROM read_xlsx(
  'D:/duckdb/data/clients.xlsx',
  all_varchar = true
)
WHERE "номер кошелека" IS NOT NULL;

-- Check clients count
SELECT COUNT(*) AS total_clients FROM clients;


-- =========================
-- 3. Create TRANSFERS table (all months)
-- =========================

DROP TABLE IF EXISTS transfers;

CREATE TABLE transfers AS
SELECT
  'September' AS month,
  regexp_replace("номер кошелька получателя", '[^0-9]', '', 'g') AS wallet_id
FROM read_xlsx('D:/duckdb/data/transfers.xlsx', sheet = 'september', all_varchar = true)
WHERE "номер кошелька получателя" IS NOT NULL

UNION ALL
SELECT
  'October',
  regexp_replace("номер кошелька получателя", '[^0-9]', '', 'g')
FROM read_xlsx('D:/duckdb/data/transfers.xlsx', sheet = 'october', all_varchar = true)
WHERE "номер кошелька получателя" IS NOT NULL

UNION ALL
SELECT
  'November',
  regexp_replace("номер кошелька получателя", '[^0-9]', '', 'g')
FROM read_xlsx('D:/duckdb/data/transfers.xlsx', sheet = 'november', all_varchar = true)
WHERE "номер кошелька получателя" IS NOT NULL;


-- =========================
-- 4. Data quality checks
-- =========================

-- Total transfers
SELECT COUNT(*) AS total_transfers FROM transfers;

-- Empty / broken wallet IDs
SELECT COUNT(*) AS broken_wallets
FROM transfers
WHERE wallet_id IS NULL OR wallet_id = '';

-- Optional cleanup
DELETE FROM transfers
WHERE wallet_id IS NULL OR wallet_id = '';


-- =========================
-- 5. Overall duplicates analysis
-- =========================

SELECT
  COUNT(*) AS total_transfers,
  COUNT(DISTINCT wallet_id) AS unique_receivers,
  COUNT(*) - COUNT(DISTINCT wallet_id) AS duplicate_transfers
FROM transfers;


-- =========================
-- 6. Transfers volume by month
-- =========================

SELECT
  month,
  COUNT(*) AS total_transfers
FROM transfers
GROUP BY month
ORDER BY month;


-- =========================
-- 7. Unique receivers by month
-- =========================

SELECT
  month,
  COUNT(DISTINCT wallet_id) AS unique_receivers
FROM transfers
GROUP BY month
ORDER BY month;


-- =========================
-- 8. Duplicates by month
-- =========================

SELECT
  month,
  COUNT(*) AS total_transfers,
  COUNT(DISTINCT wallet_id) AS unique_receivers,
  COUNT(*) - COUNT(DISTINCT wallet_id) AS duplicate_transfers
FROM transfers
GROUP BY month
ORDER BY month;


-- =========================
-- 9. Clients vs non-clients (overall)
-- =========================

-- Clients
SELECT
  COUNT(DISTINCT t.wallet_id) AS receivers_are_clients
FROM transfers t
JOIN clients c
  ON t.wallet_id = c.wallet_id;

-- Non-clients
SELECT
  COUNT(DISTINCT wallet_id) AS receivers_not_clients
FROM transfers
WHERE wallet_id NOT IN (
  SELECT wallet_id FROM clients
);


-- =========================
-- 10. Clients vs non-clients by month
-- =========================

SELECT
  t.month,
  COUNT(DISTINCT t.wallet_id) AS total_unique_receivers,
  COUNT(DISTINCT CASE WHEN c.wallet_id IS NOT NULL THEN t.wallet_id END) AS receivers_clients,
  COUNT(DISTINCT CASE WHEN c.wallet_id IS NULL THEN t.wallet_id END) AS receivers_not_clients
FROM transfers t
LEFT JOIN clients c
  ON t.wallet_id = c.wallet_id
GROUP BY t.month
ORDER BY t.month;


-- =========================
-- 11. Quick sanity checks
-- =========================

SELECT * FROM clients LIMIT 10;
SELECT * FROM transfers LIMIT 10;

-- =========================================================
-- End of file
-- =========================================================
