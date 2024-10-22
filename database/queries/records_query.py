QUERY_INSERT_RECORDS = """
    INSERT INTO records (date, max_temperature, min_temperature, precipitation, station_id)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
"""
