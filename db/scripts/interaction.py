import psycopg2
import yaml

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def insert_event(event_name, event_date, event_type):
    try:
        conn = psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['name'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO events (event_name, event_date, event_type) VALUES (%s, %s, %s) RETURNING event_id",
            (event_name, event_date, event_type)
        )
        event_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return event_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

def insert_odds(event_id, bookmaker, odds_value):
    try:
        conn = psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['name'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO odds (event_id, bookmaker, odds_value) VALUES (%s, %s, %s)",
            (event_id, bookmaker, odds_value)
        )
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def query_upcoming_events():
    try:
        conn = psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['name'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM events WHERE event_date > CURRENT_TIMESTAMP ORDER BY event_date ASC LIMIT 10")
        events = cur.fetchall()
        cur.close()
        conn.close()
        return events
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []

# Example Usage
if __name__ == "__main__":
    event_id = insert_event("UFC 259", "2024-03-06 10:00:00", "MMA")
    if event_id:
        insert_odds(event_id, "Bet365", 1.85)
    events = query_upcoming_events()
    for event in events:
        print(event)
