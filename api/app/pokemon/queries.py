COUNT_POKEMON = "SELECT COUNT(*) AS total FROM pokemon"

POKEMON_TOTALS = """
    SELECT COUNT(*) AS total_pokemon,
           COUNT(*) FILTER (WHERE base_experience IS NULL) AS pokemon_without_base_experience
    FROM pokemon
"""

LIST_POKEMON = """
    SELECT id, name, sprite
    FROM pokemon
    ORDER BY id
    LIMIT %(limit)s OFFSET %(offset)s
"""

POKEMON_DETAIL = """
    SELECT p.id, p.name, p.height, p.weight, p.base_experience, p.sprite,
           COALESCE(
               json_agg(json_build_object('id', t.id, 'name', t.name, 'slot', pt.slot)
                        ORDER BY pt.slot)
               FILTER (WHERE t.id IS NOT NULL),
               '[]'
           ) AS types,
           (SELECT MAX(id) FROM pokemon WHERE id < p.id) AS previous_id,
           (SELECT MIN(id) FROM pokemon WHERE id > p.id) AS next_id
    FROM pokemon p
    LEFT JOIN pokemon_types pt ON pt.pokemon_id = p.id
    LEFT JOIN types t ON t.id = pt.type_id
    WHERE p.id = %(pokemon_id)s
    GROUP BY p.id
"""

TYPE_SUMMARY = """
    SELECT type_id, type_name, pokemon_count, avg_base_experience
    FROM pokemon_type_summary
    ORDER BY type_name
"""
