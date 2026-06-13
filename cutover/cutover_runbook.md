# Migration Cutover Runbook

## Pre-Cutover Checklist

- [ ] All 150+ report row counts match between Redshift and Snowflake
- [ ] All dbt models successfully run on Snowflake target
- [ ] All dbt tests pass on Snowflake
- [ ] Fivetran connectors re-pointed to Snowflake
- [ ] Airflow connections updated to Snowflake
- [ ] BI tool (Tableau/Power BI) connections tested on Snowflake
- [ ] Rollback plan reviewed and approved
- [ ] Stakeholders notified of maintenance window

## Cutover Steps (Tenant-by-Tenant)

### Step 1: Freeze Redshift writes (per tenant)
```sql
-- Revoke write access for tenant
REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA tenant_a FROM loader_role;
```

### Step 2: Final sync validation
```bash
python validation/row_count_validator.py --tenant tenant_a --final-check
```

### Step 3: Switch reads to Snowflake
```bash
# Update Airflow connections
airflow connections set snowflake_mortgage_conn \
    --conn-type snowflake \
    --host $SNOWFLAKE_ACCOUNT
```

### Step 4: Validate downstream reports
```bash
python validation/row_count_validator.py --tenant tenant_a --post-cutover
```

### Step 5: Monitor for 24 hours
- Check Monte Carlo for anomalies
- Verify Slack #data-alerts is quiet
- Review Airflow DAG run history

## Rollback Plan

If issues detected within 30 minutes of cutover:
1. Re-grant write access to Redshift
2. Revert Airflow connections to Redshift
3. Notify stakeholders
4. Post-mortem within 24 hours

**RTO (Recovery Time Objective): < 15 minutes**
