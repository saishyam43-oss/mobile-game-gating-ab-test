WITH valid_data AS (
    SELECT *
    FROM game_events
    WHERE user_id NOT IN (
        SELECT user_id
        FROM game_events
        GROUP BY user_id
        HAVING COUNT(DISTINCT "group") > 1
    )
),
deduplicated AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY user_id
                   ORDER BY event_timestamp DESC
               ) AS row_num
        FROM valid_data
    ) t
    WHERE row_num = 1
)
SELECT *
FROM deduplicated;
