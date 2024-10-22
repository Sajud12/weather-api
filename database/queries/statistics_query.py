QUERY_INSERT_STATISTICS = """
    INSERT INTO statistics (avg_max_temperature, avg_min_temperature, total_precipitation, station_id, year)
    SELECT
        AVG(max_temperature / 10) AS avg_max_temperature,
        AVG(min_temperature / 10) AS avg_min_temperature,
        SUM(precipitation / 100.0) AS total_precipitation,
        station_id,
        EXTRACT(YEAR FROM date) AS year
    FROM
        records
    WHERE
        max_temperature IS NOT NULL
        AND min_temperature IS NOT NULL
        AND precipitation IS NOT NULL
    GROUP BY
        station_id, year
    ON CONFLICT DO NOTHING;
"""
