import sqlite3

def create_table():
    """Creates a table to store events"""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id TEXT, substation TEXT, snapshot_path TEXT, event_time TEXT, event_type TEXT)''')
    conn.commit()
    conn.close()
    print("Events table created in the database")

def store_event(event_id, substation, snapshot_path, event_time, event_type):
    """Stores an event in the database."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    event_time_str = event_time.strftime("%Y%m%d_%H%M%S")
    cursor.execute('INSERT INTO events (id, substation, snapshot_path, event_time, event_type) VALUES (?, ?, ?, ?, ?)',
                   (event_id, substation, snapshot_path, event_time_str, event_type))
    conn.commit()
    conn.close()


def find_common_events(substation_id, event_type):
    """Finds and returns common events from the database, optionally filtered."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    
    query = 'SELECT id, substation, snapshot_path, event_time, event_type FROM events'
    params = []
    filters = []

    # Add conditions dynamically based on provided arguments
    if substation_id is not None and substation_id != "server":
        filters.append('substation = ?')
        params.append(substation_id)
    
    if event_type is not None:
        filters.append('event_type = ?')
        params.append(event_type)
    
    # Add filters to the query if any
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)

    cursor.execute(query, params)
    events = cursor.fetchall()

    # Check if any events were retrieved
    if not events:
        print("No events found in the database.")
        return []

    # Transform into a list of dicts for easier manipulation
    events_dicts = [
        {
            'event_id': event[0],
            'substation': event[1],
            'snapshot_path': event[2],
            'timestamp': event[3],
            'event_type': event[4]  # Make sure this key matches your filtering logic
        }
        for event in events
    ]

    conn.close()
    
    # Return filtered results, or process them further
    return events_dicts

def get_all_events():
    """Retrieves all events from the database for debugging."""
    with sqlite3.connect('surveillance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        print("All Events in Database:", events)  # Debug line
    return events

def clear_database():
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    
    # Delete all records from the events table
    cursor.execute('DELETE FROM events')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("All records cleared from the database.")