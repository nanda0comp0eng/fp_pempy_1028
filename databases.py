# setup_database.py
import sqlite3
import os
from datetime import datetime

def setup_database(db_name="data.db"):
    """Setup the SQLite database with necessary tables"""
    
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Removed existing database: {db_name}")
    
    # Create new database connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create cases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                case_type TEXT NOT NULL,
                description TEXT NOT NULL,
                institution TEXT NOT NULL,
                loss_amount REAL NOT NULL,
                status TEXT NOT NULL,
                sanctions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create timeline table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timeline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL,
                date TIMESTAMP NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (case_id) REFERENCES cases (id) ON DELETE CASCADE
            )
        """)
        
        # Create trigger to update cases.updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_cases_timestamp 
            AFTER UPDATE ON cases
            BEGIN
                UPDATE cases SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = NEW.id;
            END;
        """)
        
        # Insert sample data
        sample_cases = [
            (2024, "suap", "Kasus suap pengadaan alat kesehatan", 
             "Dinas Kesehatan", 500000000, "investigasi", None),
            (2024, "pengadaan", "Kasus mark-up pengadaan komputer", 
             "Dinas Pendidikan", 750000000, "penuntutan", "Denda 1M"),
            (2023, "gratifikasi", "Kasus gratifikasi perizinan", 
             "Dinas Perizinan", 250000000, "pengadilan", None)
        ]
        
        cursor.executemany("""
            INSERT INTO cases (year, case_type, description, institution, 
                             loss_amount, status, sanctions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_cases)
        
        # Insert sample timeline entries
        sample_timeline = [
            (1, datetime.now().isoformat(), "Kasus mulai diselidiki"),
            (2, datetime.now().isoformat(), "Berkas dilimpahkan ke kejaksaan"),
            (3, datetime.now().isoformat(), "Sidang pertama dimulai")
        ]
        
        cursor.executemany("""
            INSERT INTO timeline (case_id, date, description)
            VALUES (?, ?, ?)
        """, sample_timeline)
        
        # Commit the changes
        conn.commit()
        print("Database setup completed successfully!")
        print(f"Created tables: cases, timeline")
        print(f"Inserted {len(sample_cases)} sample cases")
        print(f"Inserted {len(sample_timeline)} sample timeline entries")
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        conn.rollback()
        
    finally:
        conn.close()

def verify_database(db_name="data.db"):
    """Verify the database setup by checking tables and sample data"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\nDatabase verification:")
        print("Tables found:", [table[0] for table in tables])
        
        # Check cases count
        cursor.execute("SELECT COUNT(*) FROM cases")
        cases_count = cursor.fetchone()[0]
        print(f"Number of cases: {cases_count}")
        
        # Check timeline entries count
        cursor.execute("SELECT COUNT(*) FROM timeline")
        timeline_count = cursor.fetchone()[0]
        print(f"Number of timeline entries: {timeline_count}")
        
        # Display sample case
        cursor.execute("""
            SELECT c.*, GROUP_CONCAT(t.description)
            FROM cases c
            LEFT JOIN timeline t ON c.id = t.case_id
            GROUP BY c.id
            LIMIT 1
        """)
        sample = cursor.fetchone()
        print("\nSample case:")
        print(f"ID: {sample[0]}")
        print(f"Year: {sample[1]}")
        print(f"Type: {sample[2]}")
        print(f"Description: {sample[3]}")
        print(f"Timeline entries: {sample[9]}")
        
    except Exception as e:
        print(f"Error verifying database: {str(e)}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    DB_NAME = "data.db"
    setup_database(DB_NAME)
    verify_database(DB_NAME)