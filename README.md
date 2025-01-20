# Corruption Case Management System
## TUGAS UAS PEMROGRAMAN PYTHON

A comprehensive system for managing and tracking corruption cases, including case details, timelines, and statistics. The system consists of a FastAPI-based server, SQLite database, and a command-line client interface.

## Features

- Track multiple types of corruption cases (procurement, bribery, gratification, money laundering)
- Maintain case status and timeline
- RESTful API for integration
- Command-line interface for easy management
- SQLite database for data persistence

## System Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nanda0comp0eng/fp_pempy_1028
cd fp_pempy_1028
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database(optional):
```bash
python databases.py
```

## Project Structure

- `core.py` - Core classes and database management
- `corruption-server.py` - FastAPI server implementation
- `corruption-client.py` - Command-line client interface
- `databases.py` - Database initialization and sample data
- `data.db` - SQLite database file

## Usage

1. Start the server:
```bash
python corruption-server.py
```
The server will run on `http://localhost:8000`

2. In a separate terminal, run the client:
```bash
python corruption-client.py
```

3. Use the client menu to:
   - View all cases
   - View case details
   - Add new cases
   - Update case status
   - Delete cases

## API Endpoints

- `GET /cases` - Get all cases
- `GET /cases/{case_id}` - Get specific case details
- `GET /cases/types` - Get available case types
- `POST /cases` - Create new case
- `PUT /cases/{case_id}` - Update case status
- `DELETE /cases/{case_id}` - Delete case

## Data Models

### Case Types
- Procurement (pengadaan)
- Bribery (suap)
- Gratification (gratifikasi)
- Money Laundering (pencucian_uang)

### Case Status
- Investigation (investigasi)
- Prosecution (penuntutan)
- Court (pengadilan)
- Closed (selesai)

## Database Schema

### Cases Table
- id (INTEGER PRIMARY KEY)
- year (INTEGER)
- case_type (TEXT)
- description (TEXT)
- institution (TEXT)
- loss_amount (REAL)
- status (TEXT)
- sanctions (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Timeline Table
- id (INTEGER PRIMARY KEY)
- case_id (INTEGER, FOREIGN KEY)
- date (TIMESTAMP)
- description (TEXT)
- created_at (TIMESTAMP)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
