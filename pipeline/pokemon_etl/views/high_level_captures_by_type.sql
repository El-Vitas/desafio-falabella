CREATE OR REPLACE VIEW high_level_captures_by_type AS
SELECT t.id                                       AS type_id,
       t.name                                     AS type_name,
       COUNT(c.id) FILTER (WHERE c.level >= 50)   AS high_level_captures,
       COUNT(c.id)                                AS total_captures,
       ROUND(100.0 * COUNT(c.id) FILTER (WHERE c.level >= 50) / NULLIF(COUNT(c.id), 0), 2)
                                                  AS high_level_percent
FROM types t
LEFT JOIN pokemon_types pt ON pt.type_id = t.id
LEFT JOIN captures c ON c.pokemon_id = pt.pokemon_id
GROUP BY t.id, t.name;
