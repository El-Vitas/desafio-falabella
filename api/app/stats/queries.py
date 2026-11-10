MONTHLY_GROWTH = """
    SELECT month, captures, previous_captures, change_percent
    FROM monthly_capture_growth
    ORDER BY month
"""

TOP_TRAINERS = """
    SELECT region,
           COALESCE(
               json_agg(json_build_object('position', position, 'trainer_id', trainer_id,
                                          'trainer_name', trainer_name, 'captures', captures)
                        ORDER BY position, trainer_id)
               FILTER (WHERE trainer_id IS NOT NULL),
               '[]'
           ) AS trainers
    FROM top_trainers_by_region
    GROUP BY region
    ORDER BY region
"""

LEVEL_CLASSIFICATION = """
    SELECT type_id, type_name, high_level_captures, total_captures, high_level_percent
    FROM high_level_captures_by_type
    ORDER BY type_name
"""
