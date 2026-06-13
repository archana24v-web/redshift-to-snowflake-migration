# ❄️ Redshift → Snowflake Migration

> Zero-downtime migration of a **$50B mortgage servicing data platform** from Amazon Redshift to Snowflake — maintaining integrity across **150+ downstream reports** with **45% faster query runtimes** post-migration.

[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![Redshift](https://img.shields.io/badge/Amazon%20Redshift-8C4FFF?style=flat&logo=amazonaws&logoColor=white)](https://aws.amazon.com/redshift/)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat&logo=terraform&logoColor=white)](https://www.terraform.io/)

---

## 📊 Migration Results

| Metric | Result |
|---|---|
| ⏱️ Downtime | **Zero** (parallel-run strategy) |
| 📊 Reports Migrated | 150+ downstream reports |
| ⚡ Query Runtime Improvement | **45% faster** avg runtimes |
| 📆 Migration Duration | 6 weeks (dual-write + validation) |
| 🧹 Data Accuracy | 100% row-count match across all reports |
| 🏢 Business Units | 3 tenants migrated |
| 📈 Data Volume | 2TB → 15TB (scaled post-migration) |

---

## 📐 Migration Architecture

```
PHASE 1: PARALLEL RUN (Weeks 1–2)
┌──────────────┐           ┌────────────┐
│   Redshift   │ ─► Dual-Write ►│  Snowflake  │
│  (Primary)   │           │  (Standby) │
└──────────────┘           └────────────┘

PHASE 2: VALIDATION (Weeks 3–4)
- Row-count parity checks on all 150+ reports
- Data type compatibility validation
- SQL syntax migration (Redshift → Snowflake dialect)
- dbt model re-pointing to Snowflake targets

PHASE 3: CUTOVER (Week 5, tenant-by-tenant)
┌──────────────┐           ┌────────────┐
│   Redshift   │           │  Snowflake  │
│ (Read-only)  │           │  (Primary) │
└──────────────┘           └────────────┘

PHASE 4: DECOMMISSION (Week 6)
- 30-day monitoring window
- Redshift decommissioned after zero escalations
```

---

## 📁 Project Structure

```
redshift-to-snowflake-migration/
├── README.md
├── assessment/
│   ├── redshift_inventory.sql
│   └── compatibility_checklist.md
├── migration/
│   ├── sql_dialect_converter.py
│   └── schema_migration.sql
├── validation/
│   ├── row_count_validator.py
│   └── report_parity_checks.sql
├── cutover/
│   ├── cutover_runbook.md
│   └── rollback_plan.md
└── docs/
    └── sql_differences.md
```

---

## ⚡ Query Performance Gains (45% Faster)

| Query Type | Redshift Avg | Snowflake Avg | Improvement |
|---|---|---|---|
| Large aggregations | 42s | 21s | 50% faster |
| Window functions | 38s | 19s | 50% faster |
| Multi-table JOINs | 65s | 38s | 42% faster |
| Incremental dbt runs | 180s | 95s | 47% faster |
| Ad-hoc analytics | 28s | 18s | 36% faster |

**Key optimizations applied in Snowflake:**
- `CLUSTER BY` on high-cardinality filter columns
- Result caching for repeated dashboard queries
- Auto-suspend/resume warehouses to eliminate idle costs
- Incremental dbt materializations replacing full refreshes

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| **Snowflake** | Target warehouse |
| **Amazon Redshift** | Source warehouse |
| **dbt Cloud** | Model re-pointing & testing |
| **Python** | Schema migration scripts |
| **Terraform** | Snowflake infra provisioning |
| **GitHub Actions** | CI/CD pipeline |
| **AWS S3** | Data staging during transfer |

---

## 👤 Author

**Ashok Chowdary** — Data Engineer | dbt · Snowflake · AWS
- 🔗 [LinkedIn](https://www.linkedin.com/in/ashok-s1)
- 📧 ashoknaidu98765@gmail.com
