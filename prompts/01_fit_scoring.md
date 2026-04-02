# Astronomer Fit Scoring

You are evaluating **{COMPANY_NAME}** ({DOMAIN}) for fit with Astronomer (Apache Airflow managed platform).

## Source Tags

Use these tags on every evidence citation:
- `[SF]` — Snowflake first-party CRM data: SF_CONTACTS (who we know, activity, intent visits), SF_OPPS (deal history, loss reasons, discovery notes), SF_ACCOUNTS non-enriched fields (CRM status, owner, region, segment, ICP designation, engagement scores)
- `[SF-LF]` — Snowflake: LF_WEBSITE_VISITS + LF_PAGE_VIEWS (Leadfeeder website visit data — reliable)
- `[GONG]` — Gong call transcripts: tech stack, pain points, objections from discovery (primary truth source)
- `[WEB]` — Web search / WebFetch: job postings, engineering blog, GitHub, news (primary truth source)

> **Primary sources of truth**: Gong `[GONG]`, web search `[WEB]`, and Leadfeeder `[SF-LF]`. First-party SF data `[SF]` (contacts, opps, scores) is reliable. Tech stack, headcount, and company size always come from `[WEB]` or `[GONG]` — never from SF enrichment.

If a source returned no data, note it explicitly and reduce confidence accordingly.

---

## Dimension 1: Orchestration Need (0-4)

**What to evaluate**: Does this company have data pipelines, ETL/ELT workflows, ML training jobs, or other batch/streaming workloads that require orchestration?

**Primary sources**:
- `[WEB]` — Job descriptions mentioning Airflow/orchestration/DAGs (primary), engineering blog posts, GitHub repos, conference talks
- `[GONG]` — Tech stack mentions from call transcripts
- `[SF]` — `SF_OPPS.AIRFLOW_EXPERIENCE`, `CURRENT_AIRFLOW_DEPLOYMENT_MODEL` (what they told us in discovery — reliable)

> **Note**: `HG_AIRFLOW`, `DATAFOX_AIRFLOW`, `EVIDENCE_OF_AIRFLOW`, and `APACHE_AIRFLOW_ROLES` from SF_ACCOUNTS are unreliable and must NOT be used for scoring. Only use `[WEB]` and `[GONG]` to confirm orchestration need.

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Airflow named verbatim in job posting `[WEB]` OR Airflow confirmed in Gong discovery call `[GONG]` OR Airflow confirmed via GitHub/blog/conference `[WEB]` OR `SF_OPPS.AIRFLOW_EXPERIENCE` confirmed `[SF]` |
| 3 | Job postings mention orchestration, DAGs, or a named alternative (dagster, prefect) `[WEB]` OR engineering blog describes batch workflow architecture `[WEB]` |
| 2 | Data-heavy product implies orchestration need (ML platform, analytics product, data marketplace) `[WEB]` OR prior SF_OPPS shows Airflow discussion `[SF]` |
| 1 | Generic "data engineer" hiring without orchestration specifics `[WEB]` |
| 0 | No evidence of data pipeline needs |

---

## Dimension 2: Data Platform Maturity (0-4)

**What to evaluate**: How sophisticated is their data infrastructure? More mature = better Astronomer fit.

**Primary sources**:
- `[WEB]` — Job postings (data engineering team size, modern tooling), engineering blog posts, case studies (primary)
- `[GONG]` — Data team size and sophistication from discovery conversations
- `[SF]` — `SF_OPPS.AIRFLOW_EXPERIENCE`, `CURRENT_AIRFLOW_DEPLOYMENT_MODEL` (reliable — from actual discovery)

> **Note**: `DATA_ENGINEERS`, `DATA_PLATFORM_ENGINEERS`, `DATA_TEAM_SIZE`, `NUMBER_OF_EMPLOYEES`, `ANNUAL_REVENUE` from SF_ACCOUNTS are 3rd-party enrichment and unreliable — use as weak background context only `[UNVERIFIED-HINT-SF]`, not as scoring evidence.

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Dedicated data platform team evident from multiple open JDs or engineering blog `[WEB]`, multiple modern tools confirmed (warehouse + orchestration + BI) `[WEB]` `[GONG]` |
| 3 | Data engineering hiring confirmed (JDs mentioning data eng roles) + modern warehouse confirmed (Snowflake/BigQuery/Databricks/Redshift) `[WEB]` `[GONG]` |
| 2 | Some data infrastructure evident from web (blog, JDs, case studies) OR company size suggests mid-market data maturity `[WEB]` |
| 1 | Early-stage signals — light web presence, no clear data team from JDs `[WEB]` |
| 0 | No evidence of data infrastructure |

---

## Dimension 3: Stack Evidence (0-4)

**What to evaluate**: What specific technologies do they use? Complementary stack = higher fit.

**Primary sources**:
- `[WEB]` — Job descriptions (tools named verbatim), GitHub repos, engineering blog, case studies, StackShare (primary — required for confirmation)
- `[GONG]` — Tools named in call transcripts
- `[SF]` — `SF_OPPS.CLOUD_PROVIDER`, `CURRENT_AIRFLOW_VERSIONS` (from actual discovery calls — reliable)

> **Note**: `HG_AIRFLOW`, `HG_DBT`, `HG_DATABRICKS`, `HG_FIVETRAN`, `CF_*`, `DATAFOX_*` from SF_ACCOUNTS are unreliable signals that must NOT be used for scoring. Only `[WEB]` and `[GONG]` sources confirm stack.

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Airflow confirmed in stack via web (verbatim in JD, GitHub repo, blog post) `[WEB]` OR named in Gong transcript `[GONG]` |
| 3 | Complementary tools confirmed from web (dbt + Snowflake/Databricks in JDs or blog, Fivetran + warehouse) `[WEB]` |
| 2 | Modern cloud stack (AWS/GCP/Azure) with data tools mentioned in JDs or web `[WEB]` |
| 1 | Basic cloud usage, no specific data tooling confirmed |
| 0 | No stack evidence found |

---

## Dimension 4: Scale & Compliance (0-4)

**What to evaluate**: Do they operate at a scale or in an industry where reliability, SLAs, and compliance matter?

**Primary sources**:
- `[WEB]` — Company website (employee count, funding, customer list), LinkedIn, Crunchbase, industry news (primary)
- `[GONG]` — Scale signals from discovery conversations
- `[SF]` — `INDUSTRY`, `SEGMENT_PLANNED`, `BILLING_COUNTRY` (first-party CRM fields — reliable for classification)

> **Note**: `NUMBER_OF_EMPLOYEES`, `ANNUAL_REVENUE`, `APOLLO_COMPANY_SIZE` from SF_ACCOUNTS come from 3rd-party enrichment and are unreliable. Confirm headcount and revenue from web (company website, LinkedIn, Crunchbase, news articles) `[WEB]`.

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | Regulated industry (fintech, healthcare, gov) AND confirmed enterprise scale (1000+ employees from web) `[WEB]` `[GONG]` |
| 3 | Enterprise scale confirmed from web (500+ employees OR revenue > $50M OR named enterprise customers) OR regulated industry `[WEB]` |
| 2 | Mid-market confirmed from web (100-500 employees, Series B+ funding) with data-critical operations `[WEB]` |
| 1 | Growth-stage startup signals from web `[WEB]` |
| 0 | Too early or no scale/compliance indicators |

---

## Dimension 5: Buying Signals (0-4)

**What to evaluate**: Is there active interest in Astronomer or Airflow solutions?

**Primary sources** (ranked by signal strength):
- `[SF]` — `SF_CONTACTS.LAST_VISITED_PRICING_PAGE_DATE` (person-level pricing/demo visit — highest signal)
- `[SF]` — `SF_ACCOUNTS.FIRE_SCORE` (high fire score = active buying motion)
- `[SF]` — `SF_ACCOUNTS.SMOKE_SCORE` (elevated smoke = warming up)
- `[SF-LF]` — `LF_WEBSITE_VISITS` page URLs and recency (IP-level visit data)
- `[SF]` — `APOLLO_INTENT_SCORE`, `APOLLO_INTENT_KEYWORD`, `APOLLO_LAST_PAGE_VIEW_DATE`
- `[SF]` — `LAST_MQL_DATE`, `LAST_COSMOS_DOC_VIEW_DATE`, `LAST_DAG_FACTORY_DOWNLOAD_DATE`
- `[SF]` — Prior open/closed opp in `SF_OPPS` (prior engagement = warmer than cold)

**Scoring guide**:
| Score | Evidence Required |
|-------|-------------------|
| 4 | SF_CONTACTS pricing page visit in last 30 days `[SF]` OR high FIRE_SCORE `[SF]` OR pricing/demo page in LF_WEBSITE_VISITS last 30 days `[SF-LF]` |
| 3 | SF_CONTACTS pricing/Airflow debug visit in last 90 days `[SF]` OR multiple astronomer.io LF visits last 90 days `[SF-LF]` OR elevated SMOKE_SCORE + APOLLO_INTENT_SCORE `[SF]` |
| 2 | Single LF visit to astronomer.io `[SF-LF]` OR APOLLO_LAST_PAGE_VIEW_DATE within 6 months `[SF]` OR DAG factory download `[SF]` OR Cosmos doc view `[SF]` |
| 1 | Open or recently closed opp in SF_OPPS `[SF]` OR hiring for Airflow-related roles `[WEB]` (indirect signal) |
| 0 | No buying signals detected from any source |

---

---

## Airflow Mission Critical Assessment

Evaluate how operationally critical Airflow is to this company's business. This is separate from fit scoring — it determines **how hard to push and what message to use**, not whether to pursue.

**Primary evidence sources** (in order):
- `[GONG]` — Discovery call notes about pipeline criticality, customer-facing use, SLAs
- `[WEB]` — Job descriptions (what Airflow orchestrates), engineering blog posts, product descriptions
- `[SF]` — SF_OPPS.AIRFLOW_EXPERIENCE, CURRENT_AIRFLOW_DEPLOYMENT_MODEL (from discovery)

### Grading Scale

| Grade | Name | What it means |
|-------|------|---------------|
| **A** | Real-Time Critical | Airflow downtime = immediate customer-facing outage; sub-minute latency; revenue tied to uptime |
| **B** | Mission-Critical | Airflow downtime delays operations, misses SLAs; core batch workflows (ETL, ML training, reporting) |
| **C** | Operational Tool | Airflow used but not mission-critical; internal/nice-to-have; replaceable without major disruption |
| **D** | No Evidence | No confirmed Airflow usage |

**Diagnostic questions:**
1. Is Airflow confirmed? (CONFIRMED / LIKELY / NOT FOUND)
2. What does it orchestrate? (ETL, ML training, reporting, real-time feeds)
3. Customer impact window if Airflow goes down? (seconds → minutes → hours → days)
4. Batch or streaming? (Scheduled DAGs vs continuous)
5. Grade logic: customers impacted immediately → A | missed SLAs / delayed deliverables → B | internal inconvenience only → C | no evidence → D

### Output Format

```markdown
## Airflow Mission Critical Assessment

**Grade**: [A / B / C / D] — [Grade Name]
**Criticality**: [High / Medium / Low / None]

**The Why**:
[2-4 paragraphs: confirmed usage evidence, business model context (batch vs real-time), customer impact window, complementary stack, conclusion about Airflow's role]

**Evidence**:
1. **[Evidence type]**: [specific finding + verbatim quote] ([source tag])
2. **[Evidence type]**: [specific finding] ([source tag])

**Conclusion**: Airflow [is / is not] mission-critical. Pipeline failures would [immediately impact customers / delay deliverables / inconvenience internal teams], [with / without] direct revenue impact.
```

---

## Output Format

```markdown
## Fit Score: {COMPANY_NAME}

**Total Score**: X/20
**Grade**: [A (16-20) | B (11-15) | C (6-10) | D (0-5)]
**Confidence**: [HIGH | MEDIUM | LOW]

> Confidence is HIGH when 3+ trusted sources returned data, MEDIUM when 2, LOW when 1.
> Trusted sources: Gong transcripts, Web Search, Leadfeeder (LF_WEBSITE_VISITS), SF first-party data (SF_CONTACTS, SF_OPPS). SF 3rd-party enrichment fields alone do not count toward confidence.

### Dimension Scores

| Dimension | Score | Key Evidence |
|-----------|-------|-------------|
| Orchestration Need | X/4 | [one-line summary with source tag] |
| Data Platform Maturity | X/4 | [one-line summary with source tag] |
| Stack Evidence | X/4 | [one-line summary with source tag] |
| Scale & Compliance | X/4 | [one-line summary with source tag] |
| Buying Signals | X/4 | [one-line summary with source tag] |

### Scoring Rationale
[2-3 sentences explaining the overall score, highlighting the strongest and weakest dimensions, and noting any data gaps that affect confidence. Call out specifically if Airflow was confirmed via web (JD verbatim, GitHub, blog) or Gong — that's the single most important fact. HG_AIRFLOW/DATAFOX_AIRFLOW are unreliable hints and must not be cited as confirmation.]
```
