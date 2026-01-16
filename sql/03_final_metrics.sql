WITH base AS (
    SELECT *
    FROM deduplicated
    WHERE sum_gamerounds > 0
)

SELECT
    "group",
    COUNT(user_id) AS total_engaged_users,
    ROUND(AVG(sum_gamerounds), 1) AS avg_game_rounds
FROM base
GROUP BY "group";
