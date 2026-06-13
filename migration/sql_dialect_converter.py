"""SQL dialect converter: Redshift → Snowflake.

Automates conversion of Redshift-specific SQL syntax
to Snowflake-compatible equivalents.
"""

import re
from typing import Optional


class RedshiftToSnowflakeConverter:
    """Converts Redshift SQL dialect to Snowflake SQL."""

    CONVERSIONS = [
        # Data types
        (r'\bVARCHAR\s*\(\s*MAX\s*\)', 'VARCHAR(16777216)'),
        (r'\bNVARCHAR\b', 'VARCHAR'),
        (r'\bINT2\b', 'SMALLINT'),
        (r'\bINT4\b', 'INTEGER'),
        (r'\bINT8\b', 'BIGINT'),
        (r'\bFLOAT4\b', 'FLOAT'),
        (r'\bFLOAT8\b', 'DOUBLE'),
        (r'\bBOOL\b', 'BOOLEAN'),

        # Date/time functions
        (r'\bGETDATE\(\)', 'CURRENT_TIMESTAMP()'),
        (r'\bSYSDATE\b', 'CURRENT_DATE'),
        (r"DATEADD\s*\(\s*'(\w+)'\s*,", r'DATEADD(\1,'),
        (r"DATEDIFF\s*\(\s*'(\w+)'\s*,", r'DATEDIFF(\1,'),
        (r'\bTO_DATE\s*\(([^,]+),\s*\'(.*?)\'\)', r"TO_DATE(\1, '\2')"),

        # String functions
        (r'\bSTRPOS\s*\(', 'POSITION('),
        (r'\bCHARINDEX\s*\(([^,]+),([^)]+)\)', r'POSITION(\1 IN \2)'),
        (r'\bLEN\s*\(', 'LENGTH('),
        (r'\bNVL\s*\(', 'NVL('),  # same in Snowflake

        # Redshift-specific removals (no equivalent needed)
        (r'\bDISTKEY\s*\([^)]+\)', ''),
        (r'\bSORTKEY\s*\([^)]+\)', ''),
        (r'\bCOMPENODE\b[^;]*', ''),
        (r'\bENCODE\s+\w+', ''),
        (r'\bDISTSTYLE\s+\w+', ''),
    ]

    def convert(self, sql: str) -> str:
        """Convert Redshift SQL to Snowflake SQL."""
        result = sql
        for pattern, replacement in self.CONVERSIONS:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

    def convert_file(self, input_path: str, output_path: str):
        """Convert an entire SQL file."""
        with open(input_path, 'r') as f:
            sql = f.read()
        converted = self.convert(sql)
        with open(output_path, 'w') as f:
            f.write(converted)
        print(f"Converted: {input_path} → {output_path}")
