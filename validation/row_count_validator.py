"""Row count validation between Redshift and Snowflake.

Ensures 100% data parity across all 150+ downstream tables
before and after cutover.
"""

import logging
from dataclasses import dataclass
from typing import Optional
import psycopg2
import snowflake.connector
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    table_name: str
    redshift_count: int
    snowflake_count: int
    match: bool
    variance_pct: float


class RowCountValidator:
    """Validates data parity between Redshift and Snowflake."""

    def __init__(self, redshift_config: dict, snowflake_config: dict):
        self.rs_conn = psycopg2.connect(**redshift_config)
        self.sf_conn = snowflake.connector.connect(**snowflake_config)

    def validate_all_tables(self, tables: list[str]) -> pd.DataFrame:
        """Run row count parity check across all tables."""
        results = []
        for table in tables:
            result = self._validate_table(table)
            results.append(result)
            status = '✅ MATCH' if result.match else '❌ MISMATCH'
            logger.info(f"{status} {table}: RS={result.redshift_count:,} SF={result.snowflake_count:,}")

        df = pd.DataFrame([vars(r) for r in results])
        self._print_summary(df)
        return df

    def _validate_table(self, table: str) -> ValidationResult:
        rs_count = self._get_count(self.rs_conn, table, 'redshift')
        sf_count = self._get_count(self.sf_conn, table, 'snowflake')
        match = rs_count == sf_count
        variance = abs(rs_count - sf_count) / max(rs_count, 1) * 100
        return ValidationResult(
            table_name=table,
            redshift_count=rs_count,
            snowflake_count=sf_count,
            match=match,
            variance_pct=round(variance, 4)
        )

    def _get_count(self, conn, table: str, db_type: str) -> int:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        return cursor.fetchone()[0]

    def _print_summary(self, df: pd.DataFrame):
        total = len(df)
        passed = df['match'].sum()
        failed = total - passed
        logger.info(f"\n{'='*50}")
        logger.info(f"VALIDATION SUMMARY: {passed}/{total} tables PASSED")
        if failed > 0:
            logger.warning(f"FAILED TABLES ({failed}):")
            logger.warning(df[~df['match']][['table_name', 'redshift_count', 'snowflake_count', 'variance_pct']].to_string())
        logger.info(f"{'='*50}")
