-- Ensure users are assigned to only one experimental group
SELECT
    user_id,
    COUNT(DISTINCT "group") AS group_count
FROM game_events
GROUP BY user_id
HAVING COUNT(DISTINCT "group") > 1;
