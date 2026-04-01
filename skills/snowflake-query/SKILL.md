---
name: snowflake-query
description: Query Astronomer's Snowflake data warehouse efficiently. Use when the user asks questions that require Snowflake data — customer usage, costs, billing, product metrics, org/user lookups, ARR, or any analytical question about Astronomer customers. Knows the full table map, join patterns, and optimization rules so queries are fast and correct on the first try.
---

# Snowflake Query

Query Astronomer's Snowflake data warehouse using the MCP tools (`mcp__snowflake__*`). This skill provides the schema map, join patterns, and optimization rules needed to write efficient queries without trial and error.

## Input
The user has asked: {{args}}

---

## Connection & Warehouse

- **Account**: `fy02423-gp21411`
- **User**: `JOSEPHKENNEY`
- **Default warehouse**: `HUMANS` (X-Small, auto-suspend 60s) — **only valid warehouse; `ANALYST_WH` does not exist**
- **Primary database**: `HQ`
- **Auth**: RSA key pair via `PRIVATE_KEY_PASSPHRASE` env var (already configured)

---

## Database Architecture (HQ)

The HQ database follows a layered architecture. Always query the highest layer that satisfies the question — it's faster and pre-joined.

```
IN_*        Raw ingested data (Fivetran). Avoid unless you need raw event detail.
MODEL_*     Cleaned, modeled entities. Use for entity lookups and joins.
METRICS_*   Pre-aggregated time-series. Use for trend/cost/activity queries.
MART_*      Business-ready wide tables. Use first — already joined, widened.
REPORTING   Reporting-layer copies of key METRICS_ tables.
```

### Layer 4 — MART (start here)

| Table | What it is | Key columns |
|---|---|---|
| `MART_CUST.CURRENT_ASTRO_CUSTS` | Gold standard customer table. Every active Astro customer with usage, contract, ARR, projections, tags, team assignments. | `ACCT_NAME`, `ORG_ID`, `METRONOME_ID`, `ACCT_ID` (SF), `TOTAL_ARR_AMT`, `USAGE_AMT_1D/7D/30D`, `CONTRACT_END_DATE`, `OWNER_NAME`, `FIELD_ENGINEER`, `CUST_SUCCESS_MANAGER` |
| `MART_CUST.CURRENT_ASTRO_CUSTS_W_CRM` | Same as above but with CRM fields pre-joined. Skip the SF join step. | Same as above minus credit projections |
| `MART_CUST.CURRENT_ASTRO_CUSTS_SNAPSHOTS` | Historical daily snapshots of CURRENT_ASTRO_CUSTS | `DATE`, `ORG_ID` |
| `MART_GTM.SF_ACCT_FEATURE_STORE` | Per-account feature/signal store for GTM. Scored daily. | `DATE`, `ACCT_ID` |
| `MART_GTM.SF_ACCT_SCORES` | Propensity/health scores | `DATE`, `ACCT_ID` |
| `MART_FINANCE.USAGE_PERIODS_LOG` | Contract usage vs. period | `ORG_ID` |

### Layer 3 — METRICS (aggregated time-series)

All `*_MULTI` tables share the same schema pattern:
```
DATE         DATE       -- The period anchor date
TIME_GRAIN   VARCHAR    -- 'day', 'week', 'month' — ALWAYS filter this
START_DATE   DATE       -- Period start
END_DATE     DATE       -- Period end
[grain_key]             -- ORG_ID, DEPLOYMENT_ID, etc.
[metrics]               -- Cost, runtime, count columns
```

| Table | Grain key | Best for |
|---|---|---|
| `METRICS_FINANCE.ORG_COST_MULTI` | `ORG_ID` | Per-org daily/weekly/monthly spend |
| `METRICS_FINANCE.DEPLOYMENT_COST_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Per-deployment cost breakdown |
| `METRICS_FINANCE.DEPLOYMENT_REGION_COST_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Cost by cloud region |
| `METRICS_FINANCE.WORKER_QUEUE_COST_MULTI` | `WORKER_QUEUE_ID`, `ORG_ID` | Worker queue cost |
| `METRICS_FINANCE.CLUSTER_COST_MULTI` | `CLUSTER_ID`, `ORG_ID` | Cluster cost |
| `METRICS_FINANCE.METRONOME_USAGE_MULTI` | `METRONOME_ID` | Credit usage vs contract |
| `METRICS_FINANCE.METRONOME_REVENUE_DAILY` | `METRONOME_ID` | Daily revenue |
| `METRICS_ASTRO.ORG_ACTIVITY_MULTI` | `ORG_ID` | Org-level task/DAG activity |
| `METRICS_ASTRO.DEPLOYMENT_ACTIVITY_MULTI` | `DEPLOYMENT_ID`, `ORG_ID` | Deployment activity |
| `METRICS_ASTRO.DAG_ACTIVITY_DAILY` | `ORG_ID`, `DATE` | Daily DAG metrics |

### Layer 2 — MODEL (cleaned entities)

| Table | What it is |
|---|---|
| `MODEL_ASTRO.USERS` | All users. Has `USER_ID`, `EMAIL_DOMAIN`, `STATUS`. **No full email stored.** |
| `MODEL_ASTRO.USER_ROLES` | User-org role bindings with `EMAIL_DOMAIN`, `ROLE`, `IS_ACTIVE` |
| `MODEL_ASTRO.ORG_USERS` | User↔org membership with role |
| `MODEL_ASTRO.ORGANIZATIONS` | Org entities keyed on `ORG_ID` |
| `MODEL_ASTRO.DEPLOYMENTS` | All deployments |
| `MODEL_ASTRO.TASK_RUNS` | **7.4B rows / 1TB** — always filter by date |
| `MODEL_ASTRO.DAG_RUNS` | **1.5B rows** — always filter by date |
| `MODEL_CRM.SF_CONTACTS` | Salesforce contacts. Has `ASTRO_USER_ID` link. No email column (privacy) — use Salesforce URL. Has `CONTACT_URL`, `TITLE`, `PRIMARY_DOMAIN`. |
| `MODEL_CRM.SF_ACCOUNTS` | Salesforce accounts. Key columns: `ACCT_NAME`, `ACCT_ID`, `OWNER_NAME`, `SALES_TEAM` (Commercial/Enterprise/Strategic), `SALES_REGION`, `TOTAL_ARR_AMT`, `SMOKE_SCORE`, `ACCT_HEALTH`, `IS_CURRENT_CUST`, `IS_CHURN_RISK`, `NEXT_RENEWAL_DATE`, `HG_AIRFLOW/DATABRICKS/MWAA` (boolean tech flags). **No IS_DELETED column** — filter `ACCT_TYPE NOT IN ('Internal','Competitor')`. |
| `MODEL_CRM.SF_OPPS` | Opportunities. `OPP_TYPE`: New Business/Expansion/Renewal/Guided Trial/Churn/Downsell. Stages: `1-Discovery` → `2-QSO & Demo` → `3-EB Meeting` → `4-Tech Workshop/POV` → `5-Negotiate` → `7-Closed Won`/`8-Closed Lost`. Filter active: `IS_OPEN = TRUE`. Key: `AMT`, `INCREMENTAL_ARR_AMT`, `CLOSE_DATE`, `OWNER_FORECAST_CATEGORY`, `NEXT_STEPS`. |
| `MODEL_CRM.SF_MQLS` | MQL events. One row per MQL — contacts can have multiple. Key: `CONTACT_ID`, `ACCT_ID`, `MQL_TS`, `REPORTING_CHANNEL` (Webinar/Free Trial/Tradeshow/Paid Social/Paid Search/Field Event/etc), `ASSIGNED_AE_NAME`, `ASSIGNED_SDR_NAME`, `DISQUALIFICATION_REASON`. |
| `MODEL_CRM.SF_USERS` | SF users (reps, CSMs, FEs). `IS_ACTIVE`, `IS_ACCT_EXEC`. `ROLE` examples: `Commercial Sales (AE)`, `Enterprise Sales (AE) - East (Ritchie)`, `Field Engineer - Enterprise`, `CSM`. `SEGMENT`: Commercial/Enterprise/Enterprise+. |
| `MODEL_CRM.SF_RENEWALS` | Renewal opp summary. `ATR_AMT`, `RENEWAL_AMT`, `RENEWAL_OUTCOME`, `ATR_DATE`, `IS_PRODUCT_TRANSITION`. |
| `MODEL_CRM.SF_ASTRO_ORGS` | Maps `ORG_ID` → `ACCT_ID`. Also has `METRONOME_ID` — the bridge between product/billing and CRM. |
| `MODEL_CRM.LF_WEBSITE_VISITS` | Leadfeeder web visits. **FK is `SF_ACCT_ID` (not `ACCT_ID`)** — join to SF_ACCOUNTS on `SF_ACCT_ID = ACCT_ID`. Columns: `VISIT_TS`, `LANDING_PAGE`, `PAGE_VIEW_COUNT`, `SOURCE`, `MEDIUM`, `REFERRER`. |
| `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS` | Gong transcript text. Key columns: `CALL_ID`, `ACCT_NAME`, `CALL_TITLE`, `CALL_URL`, `SCHEDULED_TS`, `OPP_NAME`, `CALL_BRIEF`, `CALL_NEXT_STEPS`, `ATTENDEES`, `FULL_TRANSCRIPT`. Join to `GONG_CALLS` on `CALL_ID`. |
| `MODEL_CRM_SENSITIVE.GONG_CALLS` | Gong call metadata. Key columns: `CALL_ID`, `IS_DELETED`, `OPP_STAGE_AT_CALL`, `CALL_DURATION`, `PRIMARY_EMPLOYEE`. Always filter `IS_DELETED = FALSE`. |
| `MODEL_SUPPORT.ZD_TICKETS` | Zendesk tickets. **`ORG_ID` is Zendesk's ORG_ID (NUMBER type), NOT Astro ORG_ID.** Join chain: `ZD_TICKETS.ORG_ID → MAPS.ZD_ORGS.ZD_ORG_ID → ACCT_ID`. Key: `STATUS` (open/pending/hold/solved/closed), `PRIORITY` (p1-p4), `TYPE` (question/incident/problem/task), `PRODUCT`, `IS_ESCALATED`, `BUSINESS_IMPACT`, `CUSTOMER_SENTIMENT`. |
| `MODEL_SUPPORT.ZD_TICKET_COMMENTS` | Ticket thread. `BODY`, `IS_EMPLOYEE`. Join on `TICKET_ID`. Use `IS_EMPLOYEE = FALSE` for customer-only comments. |
| `MODEL_ASTRO.ORGANIZATIONS` | Org metadata. **FK to SF is `SF_ACCT_ID` (not `ACCT_ID`)** — naming inconsistency vs all other tables. Has `PRODUCT_TIER` (trial/paygo/team/enterprise/etc), `IS_TRIAL`, `IS_POV`, `IS_OBSERVE_ENABLED`, `METRONOME_ID`. Filter `IS_DELETED = FALSE AND IS_INTERNAL = FALSE`. |
| `MODEL_ASTRO.DEPLOYMENTS` | Deployment config. `EXECUTOR` (Celery/Astro/Kubernetes/Stellar), `SCHEDULER_SIZE` (small/medium/large), `CLUSTER_TYPE` (HOSTED/SHARED/BRING_YOUR_OWN_CLOUD), `AIRFLOW_VERSION`, `IS_REMOTE_EXECUTION_ENABLED`, `HAS_CICD_ENFORCEMENT`. Filter `IS_DELETED = FALSE`. |
| `MODEL_CONTRACTS.SF_CUST_CONTRACTS` | Contract terms per opp. `BASE_RATE`, `ON_DEMAND_RATE`, `RESERVED_CAPACITY`, `IS_ANNUAL`, `IS_M2M`, `ASTRO_ORG_ID`. Filter `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE` for current terms. More granular than `ACCT_PRODUCT_ARR`. |
| `MODEL_ECOSYSTEM.SCARF_COMPANY_ARTIFACT_EVENTS` | OSS download signals by company domain. `COMPANY_NAME`, `COMPANY_DOMAIN`, `ARTIFACT_NAME`, `EVENT_COUNT`, `IS_COSMOS_DOCS_PAGE_VIEW`, `IS_DAG_FACTORY_DOWNLOAD`. No direct SF join — match via domain → `SF_ACCOUNT_DOMAINS`. Good for prospecting. |
| `MODEL_EDU.SKILLJAR_COURSE_PROGRESS` | Training completion. `STUDENT_ID`, `COURSE_NAME`, `IS_COMPLETED`, `IS_CERTIFICATION`, `DAYS_TO_COMPLETE`. Good for onboarding health. |
| `MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES` | **Schema discovery tool.** `TABLE_FQID`, `TABLE_SIZE_GB`, `IS_STALE`, `PRIMARY_KEY`, `FOREIGN_KEY`. Query before running against unknown large tables. |
| `MAPS.ZD_ORGS` | Zendesk org → SF account. `ZD_ORG_ID`, `ZD_ORG_NAME`, `ACCT_ID`, `ACCT_NAME`. Filter `IS_DELETED = FALSE`. |
| `MAPS.ZD_ACCTS` | SF account → Zendesk orgs (reverse). `ACCT_ID`, `ZD_ORG_MAP` (array). |
| `MODEL_FINANCE.METRONOME_CONTRACTS` | Billing contracts. `PLAN_TYPE`: contract/paygo/trial/pov/internal. `IS_ACTIVE`, `START_TS`, `END_TS`, `RATE_CARD_ID`. Join via `METRONOME_ID`. |
| `MODEL_FINANCE.METRONOME_INVOICES` | Invoices. Filter `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE` for real revenue. `INV_TYPE`: usage/plan_arrears/scheduled/credit_purchase. `TOTAL_AMT`, `PERIOD_START_DATE`, `PERIOD_END_DATE`. |
| `MODEL_FINANCE.METRONOME_CREDIT_GRANTS` | Prepaid credits. `GRANTED_AMT`, `CURRENT_BALANCE_AMT`, `EXPIRED_AMT`. `IS_CONTRACT_CREDIT`, `IS_ACTIVE`, `EFFECTIVE_DATE`, `EXPIRATION_DATE`. Links to SF via `SF_OPP_ID`. |
| `MODEL_FINANCE.METRONOME_CREDITS_DAILY` | Daily credit burn. `CREDIT_DATE`, `DEDUCTED_AMT`, `PERIOD_CREDIT_AMT_CUMULATIVE`. Best for burn rate trends. |
| `MODEL_FINANCE.METRONOME_USAGE_DAILY` | Daily usage billing. **Always filter `IS_LATEST = TRUE`** to avoid snapshot double-counting. `USAGE_AMT`, `BILL_AMT`, `PERIOD_USAGE_AMT_CUMULATIVE`. |

### Layer 1 — IN (raw ingested)

| Table | What it is |
|---|---|
| `IN_ASTRO_DB_PROD.ORG_USER_RELATION` | Raw user↔org with `DELETED_AT` |
| `IN_ASTRO_DB_PROD.ORGANIZATION` | Raw org with `BILLING_EMAIL` |
| `IN_ASTRO_DB_PROD.USER_INVITE` | User invite records |

---

## Key Join Patterns

### Pattern 1: Account name → any metric (most common)

Always resolve account name to `ORG_ID` first in a CTE, then join:

```sql
WITH acct AS (
    SELECT ORG_ID, METRONOME_ID, ACCT_NAME
    FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
    WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
)
SELECT a.ACCT_NAME, m.DATE, m.TOTAL_COST
FROM HQ.METRICS_FINANCE.ORG_COST_MULTI m
JOIN acct a ON m.ORG_ID = a.ORG_ID
WHERE m.TIME_GRAIN = 'day'
  AND m.DATE = CURRENT_DATE - 1
```

### Pattern 2: Users for an account

```sql
WITH acct AS (
    SELECT ORG_ID FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS
    WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
)
SELECT DISTINCT
    ou.USER_ID, ou.ROLE,
    u.EMAIL_DOMAIN, u.STATUS
FROM HQ.IN_ASTRO_DB_PROD.ORG_USER_RELATION ou
JOIN HQ.MODEL_ASTRO.USERS u ON ou.USER_ID = u.USER_ID
JOIN acct a ON ou.ORGANIZATION_ID = a.ORG_ID
```

For Salesforce contact info (title, URL to get emails):
```sql
SELECT c.CONTACT_URL, c.TITLE, c.PRIMARY_DOMAIN, c.ASTRO_USER_ID
FROM HQ.MODEL_CRM.SF_CONTACTS c
WHERE c.ASTRO_USER_ID IN (<user_ids>)
  AND c.IS_DELETED = FALSE
```

### Pattern 3: Multi-period cost comparison

```sql
SELECT TIME_GRAIN, START_DATE, END_DATE, TOTAL_COST
FROM HQ.METRICS_FINANCE.ORG_COST_MULTI
WHERE ORG_ID = '<org_id>'
  AND TIME_GRAIN = 'month'
  AND DATE >= DATEADD('month', -3, CURRENT_DATE)
ORDER BY DATE
```

### Pattern 4: Usage vs contract target

```sql
SELECT
    c.ACCT_NAME,
    c.USAGE_AMT_30D,
    c.CONTRACT_TARGET_USAGE_AMT_30D,
    c.USAGE_VS_CONTRACT_TARGET_PCT_30D,
    c.CREDIT_BALANCE,
    c.PROJECTED_FULL_CREDIT_USE_DATE_30D
FROM HQ.MART_CUST.CURRENT_ASTRO_CUSTS c
WHERE UPPER(ACCT_NAME) LIKE '%CUSTOMER_NAME%'
```

### Pattern 5: Gong call fetch by account name

Two-step pattern: count check first, then full fetch.

```sql
-- Step 1: confirm calls exist (fast — uses result cache on repeat)
SELECT COUNT(*) AS call_count
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE UPPER(t.ACCT_NAME) LIKE UPPER('%ACCOUNT_NAME%')
  AND c.IS_DELETED = FALSE

-- Step 2: full fetch with all relevant fields
SELECT
    t.CALL_ID, t.CALL_TITLE, t.CALL_URL, t.SCHEDULED_TS,
    t.ACCT_NAME, t.OPP_NAME, c.OPP_STAGE_AT_CALL, c.CALL_DURATION,
    t.CALL_BRIEF, t.CALL_NEXT_STEPS, t.ATTENDEES,
    c.PRIMARY_EMPLOYEE, t.FULL_TRANSCRIPT
FROM HQ.MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS t
JOIN HQ.MODEL_CRM_SENSITIVE.GONG_CALLS c ON t.CALL_ID = c.CALL_ID
WHERE UPPER(t.ACCT_NAME) LIKE UPPER('%ACCOUNT_NAME%')
  AND c.IS_DELETED = FALSE
ORDER BY t.SCHEDULED_TS DESC
```

### Pattern 6: Zendesk org lookup for an account

```sql
SELECT z.ZD_ORG_ID, z.ZD_ORG_NAME, z.ACCT_NAME
FROM HQ.MAPS.ZD_ORGS z
WHERE z.ACCT_NAME ILIKE '%acme%'
  AND z.IS_DELETED = FALSE
```

### Pattern 7: Metronome credit balance for a customer

```sql
SELECT cg.CREDIT_NAME, cg.GRANTED_AMT, cg.CURRENT_BALANCE_AMT,
       cg.EFFECTIVE_DATE, cg.EXPIRATION_DATE, cg.IS_ACTIVE, cg.IS_EXPIRED
FROM HQ.MODEL_FINANCE.METRONOME_CREDIT_GRANTS cg
JOIN HQ.MODEL_CRM.SF_ASTRO_ORGS o ON o.METRONOME_ID = cg.METRONOME_ID
JOIN HQ.MODEL_CRM.SF_ACCOUNTS a ON a.ACCT_ID = o.ACCT_ID
WHERE a.ACCT_NAME ILIKE '%acme%'
  AND cg.IS_CONTRACT_CREDIT = TRUE
  AND cg.IS_VOIDED = FALSE
ORDER BY cg.EFFECTIVE_DATE DESC
```

### Pattern 8: Daily usage burn vs contract (Metronome)

```sql
SELECT ud.USAGE_DATE, ud.USAGE_AMT, ud.BILL_AMT,
       ud.PERIOD_USAGE_AMT_CUMULATIVE, ud.PLAN_TYPE
FROM HQ.MODEL_FINANCE.METRONOME_USAGE_DAILY ud
JOIN HQ.MODEL_CRM.SF_ASTRO_ORGS o ON o.METRONOME_ID = ud.METRONOME_ID
JOIN HQ.MODEL_CRM.SF_ACCOUNTS a ON a.ACCT_ID = o.ACCT_ID
WHERE a.ACCT_NAME ILIKE '%acme%'
  AND ud.IS_LATEST = TRUE
  AND ud.IS_CONTRACT = TRUE
ORDER BY ud.USAGE_DATE DESC
LIMIT 90
```

### Pattern 9: MQLs for an account with channel breakdown

```sql
SELECT m.MQL_TS, m.REPORTING_CHANNEL, m.UTM_CAMPAIGN,
       m.ASSIGNED_AE_NAME, m.ASSIGNED_SDR_NAME, m.FIRST_POST_MQL_STATUS
FROM HQ.MODEL_CRM.SF_MQLS m
WHERE m.ACCT_ID = (
    SELECT ACCT_ID FROM HQ.MODEL_CRM.SF_ACCOUNTS
    WHERE ACCT_NAME ILIKE '%acme%' LIMIT 1
)
ORDER BY m.MQL_TS DESC
```

### Pattern 10: Open pipeline for a rep

```sql
SELECT ACCT_NAME, OPP_NAME, OPP_TYPE, CURRENT_STAGE_NAME,
       AMT, CLOSE_DATE, OWNER_FORECAST_CATEGORY, NEXT_STEPS
FROM HQ.MODEL_CRM.SF_OPPS
WHERE OWNER_NAME ILIKE '%kenney%'
  AND IS_OPEN = TRUE
ORDER BY CLOSE_DATE
```

---

## Optimization Rules

1. **Always CTE-filter before joining**: Resolve `ACCT_NAME → ORG_ID` in a CTE, then join. Never join first and filter after on large tables.

2. **Always filter `TIME_GRAIN` on `*_MULTI` tables**: These tables store day/week/month rows for every org. Without `TIME_GRAIN = 'day'`, you'll scan 3× the data.

3. **Always add `DATE` filter on time-series tables**: `ORG_COST_MULTI`, `DEPLOYMENT_COST_MULTI`, `DAG_ACTIVITY_DAILY`, etc. are partitioned by date. A missing date filter = full table scan.

4. **Prefer MART over joining MODEL**: `CURRENT_ASTRO_CUSTS` already joins usage, contract, ARR, and team data. Don't replicate that join.

5. **Never `SELECT *` on wide tables**: `CURRENT_ASTRO_CUSTS` has 120+ columns. Select only what you need.

6. **For optimization recommendations, always check `MODEL_ASTRO.TASK_RUNS` for the actual distribution**: Aggregate tables hide bimodal distributions. Example: `DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` showed ExternalTaskSensor avg 32 min, but `TASK_RUNS` revealed 33% of tasks complete in <30s — a distribution that materially changes the recommendation. Always add `IS_TERMINAL = TRUE` and a date filter. **7.4B rows — always filter by date.**

7. **`*_LATEST` tables are pre-filtered**: `SF_ACCT_FEATURE_STORE_LATEST`, `SF_ACCT_SCORES_LATEST`, etc. — no date filter needed.

8. **Use `SAMPLE` for exploration**: `SELECT * FROM big_table SAMPLE (100 ROWS)` to spot-check data without a full scan.

9. **Result cache**: Snowflake caches identical query results for 24h. Keep expensive base CTEs unchanged when iterating — only modify the outer SELECT.

10. **`MODEL_ASTRO.ORGANIZATIONS` uses `SF_ACCT_ID` (not `ACCT_ID`)**: Every other table in HQ uses `ACCT_ID` as the SF account FK. This table uses `SF_ACCT_ID`. Don't mix them up. Prefer `SF_ASTRO_ORGS` for SF joins (consistent naming).

11. **`ZD_TICKETS.ORG_ID` is Zendesk's ORG_ID (NUMBER), not Astro's ORG_ID (VARCHAR)**: The column names collide but they're completely different keys. Always join via `MAPS.ZD_ORGS.ZD_ORG_ID` to get to `ACCT_ID`. Never join directly on ORG_ID between `ZD_TICKETS` and Astro product tables.

12. **`SF_CUST_CONTRACTS` needs `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE`**: The table contains all historical contract periods. Without these filters you'll get duplicate/expired records.

13. **`SNOWFLAKE_CURRENT_TABLES` is a free schema discovery tool**: Before describing a table or guessing column names, query `HQ.MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES` to get `TABLE_SIZE_GB`, `PRIMARY_KEY`, and `FOREIGN_KEY` — saves a describe_table call and warns you before running a full scan on a 100GB table.

14. **Metronome billing lags 2–3 days behind actual config changes**: Do not use `METRONOME_COMPUTE_EVENTS` to infer current infrastructure state. A worker size appearing in billing doesn't mean that queue is still configured that way. Use `MODEL_ASTRO.WORKER_QUEUES` for current config.

11. **`METRONOME_COMPUTE_EVENTS` has no cost column**: Must join to `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH` and compute `COMPUTE_RUNTIME_SECONDS / 3600 * UNIT_PRICE`. Always scope `RATE_CARD_ITEMS` to the customer's specific `RATE_CARD_ID` first — otherwise you pull prices from other rate cards. Use `ASTRO_ORG_ID` (not `ORGANIZATION_ID`) to filter. `METRONOME_RATE_CARD_ITEMS` has a `PRICING_GROUP_OBJECT_DEFINITION` column — use `LIKE '%small%'` (or the desired scheduler size) to filter to specific rates without JSON parsing. `METRONOME_DEPLOYMENT_EVENTS` has both `EVENT_TS` and `START_TIMESTAMP` date columns — both work for date range filtering. `DEPLOYMENT_COST_MULTI` can be filtered by `METRONOME_ID` in addition to `ORG_ID`.

12. **`DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` requires `TIME_GRAIN = 'day'`**: The table stores day, roll_7d, roll_30d, and week rows for every period. Omitting this filter inflates counts by 40–50x. **Always include `TIME_GRAIN = 'day'` (or the intended grain explicitly).**

---

## CURRENT_ASTRO_CUSTS Column Reference

The gold standard customer table (`HQ.MART_CUST.CURRENT_ASTRO_CUSTS`) — 140+ columns. Key groups:

**Identity**
- `ACCT_ID` — Salesforce account ID (primary SF FK)
- `ORG_ID` — Astro organization ID (product system key)
- `METRONOME_ID` — Billing system ID (bridge to Metronome tables)
- `ACCT_NAME`, `ACCT_TYPE`, `ACCT_STATUS`
- `OWNER_NAME`, `FIELD_ENGINEER`, `CUST_SUCCESS_MANAGER`
- `SALES_TEAM` (Commercial/Enterprise/Strategic), `SALES_REGION`

**Contract & Revenue**
- `TOTAL_ARR_AMT`, `ARR_AMT`, `ARR_PLAN_AMT`
- `CONTRACT_START_DATE`, `CONTRACT_END_DATE`
- `DAYS_TO_RENEWAL`, `ATR_AMT`, `ATR_DATE`
- `IS_ANNUAL`, `IS_M2M`, `IS_PRODUCT_TRANSITION`
- `RENEWAL_OUTCOME` (Renewed/Churned/Downsell/Upsell)

**Usage (real-time)**
- `USAGE_AMT_1D`, `USAGE_AMT_7D`, `USAGE_AMT_30D`
- `CONTRACT_TARGET_USAGE_AMT_30D`, `USAGE_VS_CONTRACT_TARGET_PCT_30D`
- `TASK_SUCCESS_COUNT_7D`, `TASK_SUCCESS_COUNT_30D`
- `DISTINCT_DAG_COUNT_30D`, `DISTINCT_USER_COUNT_30D`

**Credit & Billing**
- `CREDIT_BALANCE` — remaining prepaid credit balance
- `PROJECTED_FULL_CREDIT_USE_DATE_30D` — estimated credit exhaustion date
- `PROJECTED_FULL_CREDIT_USE_DATE_7D`
- `IS_OVERAGE_RISK` — approaching credit limit

**Health & Risk**
- `ACCT_HEALTH` (Green/Yellow/Red), `SMOKE_SCORE`, `FIRE_SCORE`
- `IS_CHURN_RISK`, `IS_DOWNGRADE_RISK`, `IS_EXPANSION_CANDIDATE`
- `P1_TICKET_COUNT`, `P2_TICKET_COUNT`, `P3_TICKET_COUNT`
- `IS_CURRENT_CUST`, `IS_TRIAL`, `IS_POV`
- `ACCT_TAGS` (array) — custom tags e.g. 'High Usage', 'Low Engagement'

**Tech Signals**
- `HG_AIRFLOW`, `HG_DATABRICKS`, `HG_MWAA`, `HG_AZURE_DATA_FACTORY` (boolean — HG Insights flags)
- `IS_REMOTE_EXECUTION_ENABLED`

**Renewal Pipeline**
- `NEXT_RENEWAL_DATE`, `RENEWAL_AMT`
- `DAYS_TO_RENEWAL` — negative = overdue

---

## Enum Quick Reference

Use these to write correct `WHERE` clauses without querying the table first.

**`SF_ACCOUNTS.ACCT_TYPE`** — filter noise: `ACCT_TYPE NOT IN ('Internal', 'Competitor')`
Values: Customer, Prospect, Partner, Internal, Competitor, Other

**`SF_ACCOUNTS.ACCT_STATUS`**
Values: Active, Inactive, Former Customer

**`SF_ACCOUNTS.SALES_TEAM`**
Values: Commercial, Enterprise, Strategic, Growth (PLG), Partner

**`SF_OPPS.OPP_TYPE`**
Values: New Business, Expansion, Renewal, Guided Trial, Churn, Downsell

**`SF_OPPS.CURRENT_STAGE_NAME`** (in order)
1-Discovery → 2-QSO & Demo → 3-EB Meeting → 4-Tech Workshop/POV → 5-Negotiate → 7-Closed Won → 8-Closed Lost

**`SF_OPPS.OWNER_FORECAST_CATEGORY`**
Values: Pipeline, Best Case, Commit, Closed, Omitted

**`SF_MQLS.REPORTING_CHANNEL`**
Values: Webinar, Free Trial, Tradeshow, Paid Social, Paid Search, Field Event, Organic Search, Direct, Partner, Content Syndication, Other

**`METRONOME_CONTRACTS.PLAN_TYPE`**
Values: contract, paygo, trial, pov, internal

**`METRONOME_INVOICES.INV_TYPE`**
Values: usage, plan_arrears, scheduled, credit_purchase

**`METRONOME_INVOICES.INV_STATUS`**
Values: draft, finalized, void — filter `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE` for real revenue

**`ZD_TICKETS.PRIORITY`**
Values: p1, p2, p3, p4 (p1 = critical/outage)

**`ZD_TICKETS.STATUS`**
Values: open, pending, hold, solved, closed

**`ZD_TICKETS.TYPE`**
Values: question, incident, problem, task

**`MODEL_ASTRO.ORGANIZATIONS.PRODUCT_TIER`**
Values: trial, basic_paygo, developer_paygo, team, team_paygo, standard, enterprise, business, pov, inactive, internal

**`MODEL_ASTRO.DEPLOYMENTS.EXECUTOR`**
Values: CeleryExecutor, AstroExecutor, KubernetesExecutor, StellarExecutor

**`MODEL_ASTRO.DEPLOYMENTS.SCHEDULER_SIZE`**
Values: small, medium, large, extra_large (note: SCHEDULER_CPU and SCHEDULER_RAM are identical for small vs medium — cannot use to estimate cost diff)

**`MODEL_ASTRO.DEPLOYMENTS.CLUSTER_TYPE`**
Values: HOSTED, SHARED, BRING_YOUR_OWN_CLOUD, VIRTUAL_RUNTIMES

---

## Email / Contact Lookup Notes

- **Full user emails are not stored in Snowflake** — privacy policy strips them from all models
- `MODEL_ASTRO.USERS` has `EMAIL_DOMAIN` only (e.g. `huli.io`)
- `MODEL_CRM.SF_CONTACTS` has `ASTRO_USER_ID` link + `CONTACT_URL` (Salesforce link where full email lives)
- To get full emails: join `ORG_USER_RELATION → USERS → SF_CONTACTS`, then use the `CONTACT_URL` to open Salesforce, or enrich via Apollo

---

## Auto-Update Instruction

This skill self-updates via two mechanisms:

**1. On query error (immediate):** A PostToolUse hook fires automatically after any failed `mcp__snowflake__execute_query` call and prompts you to log the fix as soon as it's resolved — don't wait until end of session.

**2. End of session (checklist):** The UserPromptSubmit hook reminds you to log new patterns from the session.

**Log an entry when any of the following occur:**
- A query failed due to a wrong column name, schema path, or join — record the error and fix
- An aggregate result was misleading and a different table/grain told a better story
- A new table, column, or join pattern was used successfully for the first time
- A billing/config discrepancy was discovered
- A filter that's always required was discovered (like `IS_LATEST = TRUE`, `TIME_GRAIN = 'day'`)

**After updating, always sync (local CLI only):**
```bash
cp ~/claude-work/gtm-agent-repo/skills/snowflake-query/SKILL.md \
   ~/.claude/skills/snowflake-query/SKILL.md
```

All schema knowledge is embedded in this file — no local file path dependencies. The CURRENT_ASTRO_CUSTS column reference, enum cheat sheet, and join patterns above are the authoritative reference for cloud sessions.

---

## Learned Patterns Log

Each entry captures a query pattern that was used successfully or a correction to a prior approach.

<!-- PATTERNS_LOG_START -->
**2026-03-27** — Initial schema exploration. Key discoveries:
- `CURRENT_ASTRO_CUSTS` is the gold standard account table; always start here
- `ORG_COST_MULTI` uses `ORG_ID` (not `METRONOME_ID`) as the join key — confirmed via actual query
- `IN_ASTRO_DB_PROD.ORG_USER_RELATION.ORGANIZATION_ID` = `ORG_ID` in other tables (different column name)
- `MODEL_ASTRO.USER_ROLES` IS_DELETED filter returns empty for Huli — use `IN_ASTRO_DB_PROD.ORG_USER_RELATION` + `MODEL_ASTRO.USERS` join instead
- `QUERY_HISTORY` requires `SNOWFLAKE.ACCOUNT_USAGE` schema — not accessible under current role
- `INFORMATION_SCHEMA.QUERY_HISTORY()` table function doesn't support named params in this account config
- No clustering keys are set on any tables — Snowflake relies on micro-partition pruning via natural sort order on date columns

**2026-03-30** — Schema correction from refresh run; no new user queries in past 24h:
- `INFORMATION_SCHEMA.QUERY_HISTORY_BY_USER` does NOT have `PARTITIONS_SCANNED` or `PARTITIONS_TOTAL` columns — those only exist in `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` (requires elevated role). Use `BYTES_SCANNED` as the scan-size proxy when using the `INFORMATION_SCHEMA` table function.

**2026-03-30** — Pulumi usage/cost analysis session. Key discoveries:
- `DEPLOYMENT_OPERATOR_ACTIVITY_MULTI` requires `TIME_GRAIN = 'day'` — omitting it caused a 3% undercount (131,584 vs correct 135,092) because `roll_7d`/`roll_30d` rows partially overlapped the date range
- `METRONOME_COMPUTE_EVENTS`: no cost column — must join `METRONOME_RATE_CARD_ITEMS` on `PRICING_GROUP_OBJECT_HASH`; always scope to customer's `RATE_CARD_ID` first; filter uses `ASTRO_ORG_ID` not `ORGANIZATION_ID`
- Metronome billing lags 2–3 days: Pulumi's default queue showed A40 pods in billing 3 days after they'd already switched to A20. Don't use billing data to infer current queue config — use `MODEL_ASTRO.WORKER_QUEUES`
- `MODEL_ASTRO.TASK_RUNS` has individual task durations and is the right table to check before making optimization recommendations. Aggregates mislead: ExternalTaskSensor avg was 32 min but 33% of tasks complete in <30s (upstream already done when sensor fires). Always check distribution, not just average.
- `WORKER_QUEUES` correct column names: `WORKER_QUEUE_NAME`, `POD_SIZE`, `MIN_WORKER_COUNT`, `MAX_WORKER_COUNT`, `IS_DEFAULT`, `IS_DELETED`
- `DEPLOYMENTS` org filter column is `ORG_ID` (not `ORGANIZATION_ID`)

**2026-03-31** — Session covering rate card analysis and Zendesk/Gong table discovery:
- Four new tables confirmed: `MODEL_CRM.SF_ACCOUNTS` (`OWNER_NAME`, `ZD_ORG_ID`), `MODEL_SUPPORT.ZD_ORG`, and `MODEL_CRM_SENSITIVE.GONG_CALL_TRANSCRIPTS`/`GONG_CALLS` (join on `CALL_ID`; always filter `IS_DELETED = FALSE` on GONG_CALLS; filter by `ACCT_NAME` on transcripts)
- `METRONOME_RATE_CARD_ITEMS` has `PRICING_GROUP_OBJECT_DEFINITION` column — use `LIKE '%small%'` (or scheduler type) to filter scheduler-specific rates without parsing `PRICING_GROUP_KEYS` JSON
- `METRONOME_DEPLOYMENT_EVENTS` has both `EVENT_TS` and `START_TIMESTAMP` date columns (confirmed both work for date range filtering); `DEPLOYMENT_COST_MULTI` can also be filtered by `METRONOME_ID` in addition to `ORG_ID`

**2026-04-01** — 48 queries observed (Gong cron runs + ad-hoc cost analysis):
- `GONG_CALL_TRANSCRIPTS` full column set confirmed: `CALL_ID`, `ACCT_NAME`, `CALL_TITLE`, `CALL_URL`, `SCHEDULED_TS`, `OPP_NAME`, `CALL_BRIEF`, `CALL_NEXT_STEPS`, `ATTENDEES`, `FULL_TRANSCRIPT`; `GONG_CALLS` additional columns: `OPP_STAGE_AT_CALL`, `CALL_DURATION`, `PRIMARY_EMPLOYEE`
- `ANALYST_WH` warehouse does not exist — caused "No active warehouse" failures on 2 Gong queries; always connect with `HUMANS` warehouse, never switch via `USE WAREHOUSE`
- Gong count-then-fetch pattern well-established: count check first (~100-700ms), then full transcript fetch only if calls exist; result cache (BYTES=0) kicks in reliably on repeated identical count queries
**2026-04-01** — Full schema mapping session. Major additions:
- Complete column maps for: `SF_ACCOUNTS` (170+ cols incl. tech signals HG_*, smoke/fire scores, churn flags), `SF_OPPS` (stage names confirmed: 1-Discovery through 7-Closed Won/8-Closed Lost; OPP_TYPE enum), `SF_CONTACTS`, `SF_MQLS`, `SF_USERS`, `SF_RENEWALS`, `SF_DISCOVERY_MEETING`, `SF_ASTRO_ORGS`
- `SF_ACCOUNTS` has **no IS_DELETED column** — was confirmed via query error; use `ACCT_TYPE NOT IN ('Internal','Competitor')` instead
- `LF_WEBSITE_VISITS` FK is `SF_ACCT_ID` not `ACCT_ID` — different from all other CRM tables
- Metronome full chain confirmed: `METRONOME_USAGE_DAILY` requires `IS_LATEST = TRUE`; `METRONOME_INVOICES` filter: `IS_FINALIZED = TRUE AND IS_VOIDED = FALSE`; `METRONOME_CREDIT_GRANTS` filter: `IS_CONTRACT_CREDIT = TRUE AND IS_VOIDED = FALSE`
- Metronome → SF join: `METRONOME_ID → HQ.MODEL_CRM.SF_ASTRO_ORGS.METRONOME_ID → ACCT_ID`
- Zendesk tables moved to `HQ.MAPS.ZD_ORGS` and `HQ.MAPS.ZD_ACCTS` (not `MODEL_SUPPORT.ZD_ORG` as previously logged)
- `GONG_CALLS` has `IS_DELETED` column (confirmed); `GONG_CALL_TRANSCRIPTS` does not
- `ORG_ACTIVITY_MULTI` TIME_GRAIN values: day (10.9M rows), roll_30d (11.7M), roll_7d (11.1M), week (1.6M), month (415K) — always filter `TIME_GRAIN = 'day'`
- Hooks added: PreToolUse injects gotchas before every execute_query; PostToolUse detects errors and triggers immediate skill update
**2026-04-01 (full DB sweep)** — Comprehensive schema mapping of all HQ schemas. Key discoveries:
- `MODEL_SUPPORT.ZD_TICKETS`: `ORG_ID` is Zendesk's NUMBER-type ID, NOT Astro ORG_ID — always bridge via `MAPS.ZD_ORGS.ZD_ORG_ID`. Ticket has `PRIORITY` (p1-p4), `TYPE` (question/incident/problem/task), `BUSINESS_IMPACT`, `CUSTOMER_SENTIMENT`, `IS_ESCALATED`, `IS_SECURITY_INCIDENT`. Massive for customer health context.
- `MODEL_ASTRO.ORGANIZATIONS`: FK to SF is `SF_ACCT_ID` (not `ACCT_ID`) — only table in HQ with this inconsistency. Has `PRODUCT_TIER` enum: trial/basic_paygo/developer_paygo/team/team_paygo/standard/enterprise/business/pov/inactive/internal. Filter `IS_DELETED = FALSE AND IS_INTERNAL = FALSE`.
- `MODEL_ASTRO.DEPLOYMENTS`: `EXECUTOR` values: CeleryExecutor/AstroExecutor/KubernetesExecutor/StellarExecutor. `CLUSTER_TYPE`: HOSTED/SHARED/BRING_YOUR_OWN_CLOUD/VIRTUAL_RUNTIMES. Filter `IS_DELETED = FALSE`.
- `MODEL_CONTRACTS.SF_CUST_CONTRACTS`: has actual `BASE_RATE`, `ON_DEMAND_RATE`, `RESERVED_CAPACITY` — more granular than `ACCT_PRODUCT_ARR`. Filter `IS_ACTIVE_CONTRACT = TRUE AND IS_LATEST = TRUE`.
- `MODEL_ECOSYSTEM.SCARF_COMPANY_ARTIFACT_EVENTS`: OSS download signals by company domain — no direct SF join, match via domain → `SF_ACCOUNT_DOMAINS`. Useful for prospecting.
- `MODEL_SNOWFLAKE.SNOWFLAKE_CURRENT_TABLES`: query this before running against unknown tables to get `TABLE_SIZE_GB` and declared `PRIMARY_KEY`/`FOREIGN_KEY` — free schema discovery.
- Largest schemas: `IN_SPLUNK` (2.9TB), `IN_CHRONOSPHERE` (2.4TB) — engineering, not accessible. `MODEL_ASTRO` (743GB) — always date-filter. `SEGMENT_EVENTS_PROD.CLOUD_UI` (439 tables, 14GB) — raw events, use `MODEL_WEB.*` instead.
- Hooks confirmed working: PreToolUse fired on all 5 parallel queries in this session.
<!-- PATTERNS_LOG_END -->
