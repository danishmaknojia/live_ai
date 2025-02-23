# WR Rankings Data Pipeline

This repository contains a Python script that transforms and loads wide receiver (WR) rankings data into an SQLite3 database. The script extracts key insights and maintains a query log for analysis.

## Files in this Repository

- `main.py`: Main script for data transformation and loading into the SQLite3 database.
- `lib/lib.py`: Contains helper functions for processing data.
- `WRRankingsWeek5.csv`: Dataset containing WR rankings data.
- `query_log.md`: Markdown file documenting SQL queries executed on the database.

## Installation and Usage

### Prerequisites

Ensure you have Python installed along with the required dependencies:

```sh
pip install pandas sqlite3
```

### Running the Script

Execute the main script to transform and load data into the SQLite3 database:

```sh
python main.py
```

### Querying the Database

To analyze WR rankings, interact with the SQLite database by executing SQL queries stored in `query_log.md`.

## License

This project is for educational purposes.
