import os
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CI_DATA_ROOT = PROJECT_ROOT / "data" / "ci" / "silver"

CUSTOMER_PATH = CI_DATA_ROOT / "customer_events"
BILLING_PATH = CI_DATA_ROOT / "billing_events"
NETWORK_PATH = CI_DATA_ROOT / "network_events"

DATABASE_PATH = Path(
    os.environ.get(
        "CI_DUCKDB_PATH",
        PROJECT_ROOT / "ci.duckdb",
    )
)


def create_directories() -> None:
    CUSTOMER_PATH.mkdir(parents=True, exist_ok=True)
    BILLING_PATH.mkdir(parents=True, exist_ok=True)
    NETWORK_PATH.mkdir(parents=True, exist_ok=True)


def create_customer_events(connection: duckdb.DuckDBPyConnection) -> None:
    output_file = CUSTOMER_PATH / "customer_events.parquet"

    connection.execute(
        f"""
        COPY (
            SELECT
                'customer-001'::VARCHAR AS event_id,
                1001::INTEGER AS customer_id,
                'SIGNUP'::VARCHAR AS event_type,
                TIMESTAMP '2026-01-01 10:00:00' AS event_timestamp,
                TIMESTAMP '2026-01-01 10:00:05' AS processed_timestamp

            UNION ALL

            SELECT
                'customer-002',
                1002,
                'PACKAGE_UPGRADE',
                TIMESTAMP '2026-01-02 11:00:00',
                TIMESTAMP '2026-01-02 11:00:05'

            UNION ALL

            SELECT
                'customer-003',
                1003,
                'CUSTOMER_CHURN',
                TIMESTAMP '2026-01-03 12:00:00',
                TIMESTAMP '2026-01-03 12:00:05'
        )
        TO '{output_file.as_posix()}'
        (
            FORMAT PARQUET,
            OVERWRITE_OR_IGNORE TRUE
        )
        """
    )


def create_billing_events(connection: duckdb.DuckDBPyConnection) -> None:
    output_file = BILLING_PATH / "billing_events.parquet"

    connection.execute(
        f"""
        COPY (
            SELECT
                'billing-001'::VARCHAR AS event_id,
                1001::INTEGER AS customer_id,
                'PAYMENT_RECEIVED'::VARCHAR AS event_type,
                42.99::DOUBLE AS amount,
                'DIRECT_DEBIT'::VARCHAR AS payment_method,
                TIMESTAMP '2026-01-05 09:00:00' AS event_timestamp,
                TIMESTAMP '2026-01-05 09:00:05' AS processed_timestamp

            UNION ALL

            SELECT
                'billing-002',
                1002,
                'INVOICE_GENERATED',
                55.00,
                NULL,
                TIMESTAMP '2026-01-06 09:00:00',
                TIMESTAMP '2026-01-06 09:00:05'
        )
        TO '{output_file.as_posix()}'
        (
            FORMAT PARQUET,
            OVERWRITE_OR_IGNORE TRUE
        )
        """
    )


def create_network_events(connection: duckdb.DuckDBPyConnection) -> None:
    output_file = NETWORK_PATH / "network_events.parquet"

    connection.execute(
        f"""
        COPY (
            SELECT
                'network-001'::VARCHAR AS event_id,
                1001::INTEGER AS customer_id,
                'DATA_SESSION_ENDED'::VARCHAR AS event_type,
                250.50::DOUBLE AS mb_used,
                'CV1_001'::VARCHAR AS cell_tower,
                TIMESTAMP '2026-01-07 14:00:00' AS event_timestamp,
                TIMESTAMP '2026-01-07 14:00:05' AS processed_timestamp

            UNION ALL

            SELECT
                'network-002',
                1002,
                'DATA_SESSION_ENDED',
                125.25,
                'CV2_001',
                TIMESTAMP '2026-01-07 15:00:00',
                TIMESTAMP '2026-01-07 15:00:05'
        )
        TO '{output_file.as_posix()}'
        (
            FORMAT PARQUET,
            OVERWRITE_OR_IGNORE TRUE
        )
        """
    )


def create_source_views(connection: duckdb.DuckDBPyConnection) -> None:
    connection.execute("CREATE SCHEMA IF NOT EXISTS silver")

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW silver.customer_events AS
        SELECT *
        FROM read_parquet(
            '{CUSTOMER_PATH.as_posix()}/*.parquet'
        )
        """
    )

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW silver.billing_events AS
        SELECT *
        FROM read_parquet(
            '{BILLING_PATH.as_posix()}/*.parquet'
        )
        """
    )

    connection.execute(
        f"""
        CREATE OR REPLACE VIEW silver.network_events AS
        SELECT *
        FROM read_parquet(
            '{NETWORK_PATH.as_posix()}/*.parquet'
        )
        """
    )


def validate_environment(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    expected_counts = {
        "silver.customer_events": 3,
        "silver.billing_events": 2,
        "silver.network_events": 2,
    }

    for table_name, expected_count in expected_counts.items():
        actual_count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

        if actual_count != expected_count:
            raise RuntimeError(
                f"{table_name} contains {actual_count} rows; "
                f"expected {expected_count}"
            )

        print(f"{table_name}: {actual_count} rows")


def main() -> None:
    create_directories()

    connection = duckdb.connect(str(DATABASE_PATH))

    try:
        create_customer_events(connection)
        create_billing_events(connection)
        create_network_events(connection)
        create_source_views(connection)
        validate_environment(connection)
    finally:
        connection.close()

    print(f"CI DuckDB database created at: {DATABASE_PATH}")


if __name__ == "__main__":
    main()
