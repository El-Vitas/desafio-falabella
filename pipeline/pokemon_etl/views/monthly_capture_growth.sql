CREATE OR REPLACE VIEW monthly_capture_growth AS
WITH bounds AS (
    SELECT date_trunc('month', MIN(captured_at)) AS first_month,
           date_trunc('month', MAX(captured_at)) AS last_month
    FROM captures
),
months AS (
    SELECT generate_series(first_month, last_month, INTERVAL '1 month') AS month_start
    FROM bounds
),
monthly AS (
    SELECT m.month_start, COUNT(c.id) AS captures
    FROM months m
    LEFT JOIN captures c
        ON c.captured_at >= m.month_start
       AND c.captured_at < m.month_start + INTERVAL '1 month'
    GROUP BY m.month_start
),
with_previous AS (
    SELECT month_start,
           captures,
           LAG(captures) OVER (ORDER BY month_start) AS previous_captures
    FROM monthly
)
SELECT month_start::date AS month,
       captures,
       previous_captures,
       ROUND(100.0 * (captures - previous_captures) / NULLIF(previous_captures, 0), 2)
           AS change_percent
FROM with_previous;
