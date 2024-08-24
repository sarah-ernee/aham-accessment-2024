import pytest
import psycopg
import csv
from pathlib import Path

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "password",
    "host": "localhost"
}

@pytest.fixture(scope="module")
def db_connection():
    with psycopg.connect(**DB_PARAMS) as conn:
        yield conn

def execute_sql_file(conn, file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

def test_create_tables(db_connection):
    create_sql_path = Path.cwd() / "migration/create.sql"
    print (create_sql_path)
    execute_sql_file(db_connection, create_sql_path)

    with db_connection.cursor() as cur:
        cur.execute("SELECT to_regclass('public.manager')")
        assert cur.fetchone()[0] == 'manager'
        cur.execute("SELECT to_regclass('public.fund')")
        assert cur.fetchone()[0] == 'fund'

def test_data_migration(db_connection):
    csv_path = Path.cwd() / "temp_db.csv"
    assert csv_path.exists(), "CSV file not found"

    # Count rows in CSV
    with open(csv_path, 'r') as f:
        csv_row_count = sum(1 for row in csv.reader(f)) - 1

    migrate_sql_path = Path.cwd() / "migration/migrate.sql"
    execute_sql_file(db_connection, migrate_sql_path)

    with db_connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM manager")
        manager_count = cur.fetchone()[0]
        assert manager_count > 0, "No managers were inserted"

        cur.execute("SELECT COUNT(*) FROM fund")
        fund_count = cur.fetchone()[0]
        assert fund_count == csv_row_count, f"Expected {csv_row_count} funds, but found {fund_count}"

        cur.execute("SELECT COUNT(*) FROM fund f LEFT JOIN manager m ON f.manager_id = m.id WHERE m.id IS NULL")
        orphaned_funds = cur.fetchone()[0]
        assert orphaned_funds == 0, f"Found {orphaned_funds} funds with invalid manager_id"

def test_data_integrity(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("SELECT * FROM fund WHERE fund_id IS NULL OR fund_name IS NULL OR net_asset IS NULL OR performance IS NULL")
        problematic_rows = cur.fetchall()
        assert not problematic_rows, f"Found rows with NULL values: {problematic_rows}"

        cur.execute("SELECT COUNT(*) FROM (SELECT fund_id FROM fund GROUP BY fund_id HAVING COUNT(*) > 1) AS dup")
        duplicate_count = cur.fetchone()[0]
        assert duplicate_count == 0, f"Found {duplicate_count} duplicate fund IDs"

if __name__ == "__main__":
    pytest.main([__file__])