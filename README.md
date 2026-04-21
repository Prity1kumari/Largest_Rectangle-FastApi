# Largest Rectangle in Matrix — FastAPI Service

## Overview

A FastAPI service that finds the **largest rectangle formed by identical numbers** in a 2D integer matrix. All requests and responses are logged to a SQLite database with turnaround time.

---

## Project Structure

```
largest_rectangle_api/
├── main.py          # FastAPI app, routes
├── algorithm.py     # Core rectangle algorithm
├── database.py      # SQLAlchemy models & DB setup
├── tests.py         # Unit tests
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: http://localhost:8000

Interactive docs: http://localhost:8000/docs

---

## API Endpoints

### POST `/largest-rectangle`

Find the largest rectangle in a matrix.

**Request body:**
```json
{
  "matrix": [
    [1, 1, 1, 0, 1, -9],
    [1, 1, 1, 1, 2, -9],
    [1, 1, 1, 1, 2, -9],
    [1, 0, 0, 0, 5, -9],
    [5, 0, 0, 0, 5]
  ]
}
```

**Response:**
```json
{
  "number": 1,
  "area": 8,
  "turnaround_time_ms": 0.312
}
```

**cURL example:**
```bash
curl -X POST http://localhost:8000/largest-rectangle \
  -H "Content-Type: application/json" \
  -d '{"matrix": [[1,1,1,0],[1,1,1,1],[1,1,1,1],[1,0,0,0]]}'
```

---

### GET `/logs`

View all logged requests from the database.

```bash
curl http://localhost:8000/logs
```

---

## Running Tests

```bash
python tests.py
```

Or with pytest:
```bash
pip install pytest
pytest tests.py -v
```

---

## Algorithm Explanation

For each unique number in the matrix:
1. Build a **heights array** row by row — height[c] = consecutive rows upward where that value appears at column c.
2. Apply the classic **"Largest Rectangle in Histogram"** algorithm (O(n) using a stack) on each row's heights.
3. Track the best (number, area) pair globally.

**Time Complexity:** O(rows × cols × unique_values)  
**Space Complexity:** O(cols)

---

## Database

SQLite file: `request_logs.db` (auto-created on startup)

Schema (`request_logs` table):

| Column             | Type    | Description                     |
|--------------------|---------|---------------------------------|
| id                 | INTEGER | Auto-increment primary key      |
| matrix             | TEXT    | String representation of input  |
| result_number      | INTEGER | The winning number              |
| result_area        | INTEGER | Area of largest rectangle       |
| turnaround_time_ms | FLOAT   | Request processing time (ms)    |
| created_at         | DATETIME| UTC timestamp                   |
