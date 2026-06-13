# Redshift vs Snowflake SQL Differences

## Key Syntax Differences

| Feature | Redshift | Snowflake |
|---|---|---|
| Current timestamp | `GETDATE()` | `CURRENT_TIMESTAMP()` |
| String position | `CHARINDEX(str, col)` | `POSITION(str IN col)` |
| String length | `LEN(col)` | `LENGTH(col)` |
| Interval add | `DATEADD('day', 1, col)` | `DATEADD(day, 1, col)` |
| Max varchar | `VARCHAR(MAX)` | `VARCHAR(16777216)` |
| Boolean | `BOOL` | `BOOLEAN` |
| Distribution key | `DISTKEY(col)` | N/A (automatic micro-partitioning) |
| Sort key | `SORTKEY(col)` | `CLUSTER BY (col)` |
| Approximate count | `APPROXIMATE COUNT(DISTINCT col)` | `APPROX_COUNT_DISTINCT(col)` |
| Copy from S3 | `COPY ... FROM 's3://...'` | `COPY INTO ... FROM @stage` |

## Performance Equivalents

| Redshift | Snowflake |
|---|---|
| Distribution styles (EVEN/KEY/ALL) | Automatic micro-partitioning |
| Sort keys | `CLUSTER BY` |
| Vacuum / Analyze | Automatic |
| WLM queues | Multi-cluster warehouses |
| Spectrum (external tables) | External stages / Snowpipe |
