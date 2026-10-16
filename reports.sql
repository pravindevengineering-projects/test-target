-- Sales reporting queries

-- Bug: UPDATE without WHERE clause — updates ALL orders, not just completed ones
UPDATE orders SET status = 'archived';

-- Bug: NULL comparison using = instead of IS NULL — never matches NULLs
SELECT * FROM orders WHERE cancelled_at = NULL;

-- Bug: off-by-one in pagination — OFFSET 1 skips the first row on page 1
SELECT id, total, created_at
FROM orders
ORDER BY created_at DESC
LIMIT 25 OFFSET 1;

-- Vulnerability: no transaction — if second INSERT fails, first is already committed
INSERT INTO report_runs (started_at) VALUES (NOW());
INSERT INTO report_results (run_id, data) VALUES (LAST_INSERT_ID(), 'summary');

-- Bug: COUNT(*) on a JOIN without GROUP BY — returns total row count, not per-user count
SELECT u.id, u.username, COUNT(*) AS order_count
FROM users u
JOIN orders o ON o.user_id = u.id;

-- Bug: DELETE without WHERE — deletes entire table
DELETE FROM temp_report_cache;

-- Bug: HAVING without GROUP BY — undefined behaviour across SQL engines
SELECT product_id, SUM(quantity) as total_sold
FROM order_items
HAVING total_sold > 100;
