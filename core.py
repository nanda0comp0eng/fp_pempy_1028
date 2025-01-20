from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
import sqlite3
from dataclasses import dataclass

class CaseType(str, Enum):
    PROCUREMENT = "pengadaan"
    BRIBERY = "suap"
    GRATIFICATION = "gratifikasi"
    MONEY_LAUNDERING = "pencucian_uang"

class CaseStatus(str, Enum):
    INVESTIGATION = "investigasi"
    PROSECUTION = "penuntutan"
    COURT = "pengadilan"
    CLOSED = "selesai"

@dataclass
class TimelineEntry:
    date: datetime
    description: str

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "description": self.description
        }

class DatabaseManager:
    def __init__(self, db_name="data.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create cases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year INTEGER,
                    case_type TEXT,
                    description TEXT,
                    institution TEXT,
                    loss_amount REAL,
                    status TEXT,
                    sanctions TEXT
                )
            """)
            
            # Create timeline table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS timeline (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER,
                    date TIMESTAMP,
                    description TEXT,
                    FOREIGN KEY (case_id) REFERENCES cases (id)
                )
            """)
            
            conn.commit()

class CorruptionCaseManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_case(self, case_data: dict) -> dict:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cases (year, case_type, description, institution, 
                                 loss_amount, status, sanctions)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                case_data["year"],
                case_data["case_type"],
                case_data["description"],
                case_data["institution"],
                case_data["loss_amount"],
                case_data["status"],
                case_data.get("sanctions")
            ))
            case_id = cursor.lastrowid
            conn.commit()
            
            return self.get_case(case_id)

    def get_case(self, case_id: int) -> Optional[dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
            case = cursor.fetchone()
            
            if not case:
                return None
                
            # Get timeline entries
            cursor.execute("SELECT date, description FROM timeline WHERE case_id = ?", (case_id,))
            timeline = [{"date": date, "description": desc} for date, desc in cursor.fetchall()]
            
            return {
                "id": case[0],
                "year": case[1],
                "case_type": case[2],
                "description": case[3],
                "institution": case[4],
                "loss_amount": case[5],
                "status": case[6],
                "sanctions": case[7],
                "timeline": timeline
            }

    def get_all_cases(self) -> List[dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cases")
            case_ids = cursor.fetchall()
            return [self.get_case(case_id[0]) for case_id in case_ids]

    def update_case_status(self, case_id: int, new_status: str, timeline_desc: str) -> Optional[dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE cases SET status = ? WHERE id = ?", (new_status, case_id))
            
            if cursor.rowcount == 0:
                return None
                
            # Add timeline entry
            cursor.execute("""
                INSERT INTO timeline (case_id, date, description)
                VALUES (?, ?, ?)
            """, (case_id, datetime.now().isoformat(), timeline_desc))
            
            conn.commit()
            return self.get_case(case_id)

    def delete_case(self, case_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM timeline WHERE case_id = ?", (case_id,))
            cursor.execute("DELETE FROM cases WHERE id = ?", (case_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted