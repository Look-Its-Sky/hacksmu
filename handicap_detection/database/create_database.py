import sqlite3

# Create a connection to the database
conn = sqlite3.connect("parking_database.db")
cursor = conn.cursor()

# Create the cameras table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cameras (
        id INTEGER PRIMARY KEY,
        camera_id TEXT NOT NULL
    );
""")

# Create the license_plates table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS license_plates (
        id INTEGER PRIMARY KEY,
        license_plate TEXT NOT NULL,
        camera_id INTEGER NOT NULL,
        FOREIGN KEY (camera_id) REFERENCES cameras (id)
    );
""")

# Create the handicap_status table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS handicap_status (
        id INTEGER PRIMARY KEY,
        license_plate_id INTEGER NOT NULL,
        is_handicapped BOOLEAN NOT NULL,
        FOREIGN KEY (license_plate_id) REFERENCES license_plates (id)
    );
""")

# Commit the changes
conn.commit()

# Close the connection
conn.close()