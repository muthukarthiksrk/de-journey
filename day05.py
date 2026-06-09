import psycopg2
import psycopg2.extras
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

CONNECTION_STRING = "postgresql://neondb_owner:npg_4GrAjo1bMTqB@ep-icy-frog-aqit13g4.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_connection():
    return psycopg2.connect(CONNECTION_STRING)

# ============================================
# PART 1 - Create tables
# ============================================
def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Main weather table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_raw (
                id            SERIAL PRIMARY KEY,
                city          VARCHAR(100) NOT NULL,
                temperature_c DECIMAL(5,2),
                feels_like_c  DECIMAL(5,2),
                humidity_pct  INTEGER,
                weather       VARCHAR(200),
                wind_speed    DECIMAL(5,2),
                heat_index    VARCHAR(50),
                extracted_at  TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
        logging.info("Tables created successfully")
    except Exception as e:
        conn.rollback()
        logging.error(f"Create table failed: {e}")
    finally:
        cur.close()
        conn.close()

# ============================================
# PART 2 - Insert data
# ============================================
def load_weather_data(records: list):
    conn = get_connection()
    cur = conn.cursor()
    try:
        psycopg2.extras.execute_batch(cur, """
            INSERT INTO weather_raw
                (city, temperature_c, feels_like_c, humidity_pct,
                 weather, wind_speed, heat_index, extracted_at)
            VALUES
                (%(city)s, %(temperature_c)s, %(feels_like_c)s,
                 %(humidity_pct)s, %(weather)s, %(wind_speed)s,
                 %(heat_index)s, %(extracted_at)s)
        """,records)
        conn.commit()
        logging.info(f"Inserted {len(records)} rows into weather_raw")
    except Exception as e:
        conn.rollback()
        logging.error(f"Insert failed: {e}")
    finally:
        cur.close()
        conn.close()

# ============================================
# PART 3 - Query with EXPLAIN
# ============================================
def query_with_explain(city: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # EXPLAIN shows how PostgreSQL executes a query
        cur.execute("""
            EXPLAIN ANALYZE
            SELECT city, temperature_c, heat_index
            FROM weather_raw
            WHERE city = %s
            ORDER BY extracted_at DESC
            LIMIT 5
        """, (city,))
        print(f"\n=== EXPLAIN ANALYZE for city={city} ===")
        for row in cur.fetchall():
            print(row[0])
    except exception as e:
        logging.error(f"Query with explain failed: {e}")
    finally:
        cur.close()
        conn.close()

# ============================================
# PART 4 - Add index and compare
# ============================================
def add_index():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_weather_city
            ON weather_raw(city)
        """)
        conn.commit()
        logging.info("Index created on city column")
    except Exception as e:
        conn.rollback()
        logging.error(f"Index creation failed: {e}")
    finally:
        cur.close()
        conn.close()

# ============================================
# PART 5 - Transactions demo
# ============================================
def demo_transaction():
    conn = get_connection()
    cur = conn.cursor()
    try:
        logging.info("Transaction started")
        cur.execute("""
            UPDATE weather_raw
            SET heat_index = 'Extreme'
            WHERE temperature_c > 43
        """)
        rows_updated = cur.rowcount
        logging.info(f"Updated {rows_updated} rows to Extreme heat index")
        conn.commit()
        logging.info("Transaction committed")
    except Exception as e:
        conn.rollback()
        logging.error(f"Transaction rolled back: {e}")
    finally:
        cur.close()
        conn.close()

# ============================================
# RUN ALL PARTS
# ============================================
if __name__ == "__main__":
    # Sample data
    records = [
        {"city": "Chennai", "temperature_c": 37.89, "feels_like_c": 46.18,
         "humidity_pct": 45, "weather": "overcast clouds", "wind_speed": 2.24,
         "heat_index": "Dangerous", "extracted_at": datetime.now()},
        {"city": "Delhi", "temperature_c": 43.36, "feels_like_c": 41.88,
         "humidity_pct": 13, "weather": "clear sky", "wind_speed": 5.78,
         "heat_index": "Very Hot", "extracted_at": datetime.now()},
        {"city": "Mumbai", "temperature_c": 31.66, "feels_like_c": 38.61,
         "humidity_pct": 66, "weather": "broken clouds", "wind_speed": 5.43,
         "heat_index": "Very Hot", "extracted_at": datetime.now()},
        {"city": "Bengaluru", "temperature_c": 27.09, "feels_like_c": 30.27,
         "humidity_pct": 65, "weather": "overcast clouds", "wind_speed": 18.33,
         "heat_index": "Warm", "extracted_at": datetime.now()},
        {"city": "Hyderabad", "temperature_c": 34.40, "feels_like_c": 35.97,
         "humidity_pct": 42, "weather": "overcast clouds", "wind_speed": 7.28,
         "heat_index": "Hot", "extracted_at": datetime.now()},
    ]

    logging.info("=== Day 5: Database Internals ===")
    create_tables()
    load_weather_data(records)

    # Before index
    print("\n--- BEFORE INDEX ---")
    query_with_explain("Chennai")

    # Add index
    add_index()

    # After index
    print("\n--- AFTER INDEX ---")
    query_with_explain("Chennai")

    # Transaction demo
    demo_transaction()

    logging.info("=== Day 5 complete ===")



