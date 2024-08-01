import psycopg2
import yaml

# Load configuration
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS events (
            event_id SERIAL PRIMARY KEY,
            event_name VARCHAR(255) NOT NULL,
            event_date TIMESTAMP NOT NULL,
            event_type VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS odds (
            odd_id SERIAL PRIMARY KEY,
            event_id INTEGER NOT NULL,
            bookmaker VARCHAR(255),
            odds_value FLOAT,
            FOREIGN KEY (event_id)
                REFERENCES events (event_id)
                ON UPDATE CASCADE ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            host=config['database']['host'],
            database=config['database']['name'],
            user=config['database']['user'],
            password=config['database']['password']
        )
        cur = conn.cursor()
        
        # Execute each command in the commands tuple
        for command in commands:
            cur.execute(command)
        
        # Close the communication with the PostgreSQL database
        cur.close()
        conn.commit()
        conn.close()
        print("Tables created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    create_tables()
