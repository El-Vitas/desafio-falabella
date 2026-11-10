CREATE OR REPLACE VIEW pokemon_type_summary AS
SELECT
    t.id                             AS type_id,
    t.name                           AS type_name,
    COUNT(p.id)                      AS pokemon_count,
    ROUND(AVG(p.base_experience), 2) AS avg_base_experience
FROM types t
LEFT JOIN pokemon_types pt ON pt.type_id = t.id
LEFT JOIN pokemon p ON p.id = pt.pokemon_id
GROUP BY t.id, t.name;
