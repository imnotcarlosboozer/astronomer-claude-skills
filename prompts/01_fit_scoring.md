# Astronomer Fit Scoring

You are evaluating **{COMPANY_NAME}** ({DOMAIN}) for fit with Astronomer (Apache Airflow managed platform).

## Scoring Instructions

Using the RAW INTELLIGENCE block provided above, score this company on a 0-20 scale across 5 dimensions (0-4 points each). Every score MUST cite evidence with source tags: `[EXA]`, `[LF]`, `[CR]`.

If a source returned no data, note it explicitly and reduce confidence accordingly.

---

## Dimension 1: Orchestration Need (0-4)

**What to evaluate**: Does this company have data pipelines, ETL/ELT workflows, ML training jobs, or other batch/streaming workloads that require orchestration?

**Primary sources**:
- `[EXA]` — Tech stack searches, engineering blog posts, job descriptions mentioning Airflow/orchestration/DAGs/pipelines
- `[EXA]` — Company research for product descriptions involving data processing

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Confirmed Airflow user OR explicit orchestration tool in use (Prefect, Dagster, Luigi, Step Functions) `[EXA]` |
| 3 | Job postings mention orchestration/pipelines/DAGs OR engineering blog describes batch workflows `[EXA]` |
| 2 | Data-heavy product implies orchestration need (ML platform, analytics product, data marketplace) `[EXA]` |
| 1 | Generic "data engineer" hiring without orchestration specifics `[EXA]` |
| 0 | No evidence of data pipeline needs |

---

## Dimension 2: Data Platform Maturity (0-4)

**What to evaluate**: How sophisticated is their data infrastructure? More mature = better Astronomer fit (they understand the pain).

**Primary sources**:
- `[EXA]` — Company research: product descriptions, tech blog posts
- `[CR]` — Organization profile: company size, revenue, employee count (larger companies = more mature data platforms)

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Dedicated data platform team, multiple data tools in stack (warehouse + orchestration + BI), 500+ employees `[EXA]` `[CR]` |
| 3 | Data engineering team exists, modern warehouse (Snowflake/BigQuery/Databricks/Redshift) confirmed `[EXA]` |
| 2 | Some data infrastructure evident, 100-500 employees, Series B+ `[EXA]` `[CR]` |
| 1 | Early-stage data efforts, <100 employees or pre-Series B `[EXA]` `[CR]` |
| 0 | No evidence of data infrastructure |

---

## Dimension 3: Stack Evidence (0-4)

**What to evaluate**: What specific technologies do they use? Complementary stack = higher fit.

**Primary sources**:
- `[EXA]` — Code context searches (GitHub repos, Stack Overflow, tech blogs)
- `[CR]` — Community activity: GitHub contributions, Slack/forum posts about Airflow or data tools, open-source engagement

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Active Airflow contributor/user in community `[CR]` OR Airflow in confirmed tech stack `[EXA]` |
| 3 | Uses complementary tools (dbt, Spark, Kafka, cloud-native services) with evidence from 2+ sources `[EXA]` `[CR]` |
| 2 | Modern cloud stack (AWS/GCP/Azure) with data tools mentioned `[EXA]` |
| 1 | Basic cloud usage, no specific data tooling evidence |
| 0 | No stack evidence found |

---

## Dimension 4: Scale & Compliance (0-4)

**What to evaluate**: Do they operate at a scale or in an industry where reliability, SLAs, and compliance matter?

**Primary sources**:
- `[EXA]` — Company research: industry, customer base, regulatory environment
- `[CR]` — Organization profile: revenue, employee count, industry classification

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Regulated industry (fintech, healthcare, gov) AND 1000+ employees `[EXA]` `[CR]` |
| 3 | Enterprise scale (500+ employees, $50M+ revenue) OR regulated industry `[EXA]` `[CR]` |
| 2 | Mid-market (100-500 employees) with data-critical operations `[EXA]` `[CR]` |
| 1 | Growth-stage startup with scaling data needs `[EXA]` `[CR]` |
| 0 | Too early or no scale/compliance indicators |

---

## Dimension 5: Buying Signals (0-4)

**What to evaluate**: Is there active interest in Astronomer or Airflow solutions?

**Primary sources**:
- `[LF]` — Leadfeeder page visits: which pages, how often, how recently (pricing page = strong signal)
- `[CR]` — Website visits, community questions about Airflow, engagement with Astronomer content

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Visited astronomer.io pricing/demo page in last 30 days `[LF]` OR asked about Astronomer in community `[CR]` |
| 3 | Multiple astronomer.io visits in last 90 days `[LF]` OR Airflow-related community questions `[CR]` |
| 2 | Single astronomer.io visit `[LF]` OR general Airflow community activity `[CR]` |
| 1 | Hiring for Airflow-related roles `[EXA]` (indirect buying signal) |
| 0 | No buying signals detected |

---

## Output Format

```markdown
## Fit Score: {COMPANY_NAME}

**Total Score**: X/20
**Grade**: [A (16-20) | B (11-15) | C (6-10) | D (0-5)]
**Confidence**: [HIGH | MEDIUM | LOW]

> Confidence is HIGH when 3+ sources returned data, MEDIUM when 2, LOW when 1. Sources: Exa AI, Leadfeeder, Common Room, Gong, Apollo.

### Dimension Scores

| Dimension | Score | Key Evidence |
|-----------|-------|-------------|
| Orchestration Need | X/4 | [one-line summary with source tag] |
| Data Platform Maturity | X/4 | [one-line summary with source tag] |
| Stack Evidence | X/4 | [one-line summary with source tag] |
| Scale & Compliance | X/4 | [one-line summary with source tag] |
| Buying Signals | X/4 | [one-line summary with source tag] |

### Scoring Rationale
[2-3 sentences explaining the overall score, highlighting the strongest and weakest dimensions, and noting any data gaps that affect confidence.]
```
