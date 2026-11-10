CREATE OR REPLACE VIEW top_trainers_by_region AS
WITH trainer_captures AS (
    SELECT t.id, t.name, t.region, COUNT(*) AS captures
    FROM trainers t
    JOIN captures c ON c.trainer_id = t.id
    GROUP BY t.id
),
ranked AS (
    SELECT id, name, region, captures,
           RANK() OVER (PARTITION BY region ORDER BY captures DESC) AS position
    FROM trainer_captures
),
regions AS (
    SELECT DISTINCT region FROM trainers
)
SELECT r.region,
       ranked.position,
       ranked.id   AS trainer_id,
       ranked.name AS trainer_name,
       ranked.captures
FROM regions r
LEFT JOIN ranked ON ranked.region = r.region AND ranked.position <= 3;
