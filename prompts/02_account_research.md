# Account Research Summary

You are generating an AE brief for **{COMPANY_NAME}** ({DOMAIN}) as a prospective Astronomer (Apache Airflow) customer.

## Instructions

Using all data provided, generate a structured account research summary. Every bullet point MUST be tagged with its verification status:

- `(VERIFIED-SF)` — Confirmed by first-party Salesforce CRM: SF_CONTACTS (activity, intent visits), SF_OPPS (deal history, discovery notes), SF_ACCOUNTS non-enriched fields (CRM status, owner, region, ICP designation, engagement scores)
- `(VERIFIED-SF-LF)` — Confirmed by Leadfeeder data in Snowflake: LF_WEBSITE_VISITS / LF_PAGE_VIEWS
- `(VERIFIED-GONG)` — Confirmed by Gong call transcripts (primary truth source)
- `(VERIFIED-WEB)` — Confirmed by web search / WebFetch: job postings, news, engineering blog, GitHub (primary truth source)
- `(GENERATED)` — Inferred or synthesized from available data (not directly confirmed)

> **Source hierarchy**: Gong and web search are primary. Leadfeeder and first-party SF (contacts, opps, scores) are reliable. Tech stack, headcount, and hiring signals always come from web or Gong — not from SF.

If a data source returned no results, explicitly note "No data available from [source]" in the relevant section.

---

## Output Format

```markdown
## Account Research: {COMPANY_NAME}

### Airflow Mission Critical Assessment

> **Grade tells the rep HOW to sell. A/B = lead with reliability/SLA urgency. C = lead with efficiency/DevEx. D = educate first.**

**Grade**: [A / B / C / D] — [Real-Time Critical / Mission-Critical / Operational Tool / No Evidence]
**Criticality**: [High / Medium / Low / None]

**The Why**:
[2-4 paragraphs: confirmed Airflow usage evidence, business model context (batch vs real-time), customer impact window if Airflow goes down, complementary stack, conclusion about Airflow's role in their operations]

**Evidence**:
1. **[Evidence type]**: [specific finding + verbatim quote where available] ([source tag])
2. **[Evidence type]**: [specific finding] ([source tag])

**Conclusion**: Airflow [is / is not] mission-critical to {COMPANY_NAME}. Pipeline failures would [immediately impact customers / delay deliverables and miss SLAs / inconvenience internal teams only], [with / without] direct revenue impact.

---

### Email Brief

> **This is the #1 section for AI email generation.** It distills the entire report into the most actionable outreach inputs.

- **Outreach Type**: [WARM — prior Gong calls or opp history | FOLLOW-UP — emails sent but no reply | COLD — no prior conversations] (VERIFIED-GONG / VERIFIED-SF / GENERATED)
- **Urgency**: [HOT — reach out this week | WARM — reach out this month | COOL — add to nurture sequence] (GENERATED)
- **Urgency Rationale**: [1 sentence — e.g., "SF_CONTACTS shows pricing page visit 8 days ago + HG_AIRFLOW=true" or "No buying signals, general fit only"] (GENERATED)

**Top 3 Personalization Hooks** (ranked by impact):
1. [Most compelling — e.g., a SF_CONTACTS pricing page visit, a Gong call to follow up on, a specific HG stack signal, a job posting phrase] (source tag)
2. [Second hook — e.g., a recent product launch, SF_OPPS Airflow experience from prior discovery, engineering blog post] (source tag)
3. [Third hook — e.g., hiring signal, funding round, community question] (source tag)

**If prior Gong calls or SF_OPPS history exists**:
- **Last Call / Opp**: [date] with [participants/titles] (VERIFIED-GONG / VERIFIED-SF)
- **Outcome**: [1 sentence — what was discussed, where it left off, any follow-ups promised, loss reason if closed-lost] (VERIFIED-GONG / VERIFIED-SF)
- **Email Angle**: [1 sentence — how to reference the prior conversation naturally] (GENERATED)

**If no prior calls or opps**:
- **Cold Outreach Angle**: [1 sentence — the single strongest reason to reach out, grounded in the data] (GENERATED)

### Company Overview
- **Description**: [1-2 sentence description] (VERIFIED-WEB)
- **Founded**: [year] (VERIFIED-WEB)
- **Headquarters**: [location] (VERIFIED-SF / VERIFIED-WEB)
- **Employees**: [count from web — company website, LinkedIn, Crunchbase] (VERIFIED-WEB)
- **Industry**: [industry / sub-industry] (VERIFIED-SF)
- **Funding / Revenue**: [total raised, last round, or revenue estimate] (VERIFIED-WEB)
- **CRM Status**: [Prospect / Customer since {date} / Churned / Closed-lost] (VERIFIED-SF)
- **Astronomer Account Owner**: [{OWNER_NAME}, {SALES_REGION}] (VERIFIED-SF)

### Tech Stack
- **Cloud Provider**: [AWS/GCP/Azure/multi-cloud — from JD or web] (VERIFIED-WEB / VERIFIED-GONG)
- **Airflow / Orchestration**: [Confirmed from web: verbatim JD / GitHub / blog — or "Not confirmed via web" | If SF_OPPS discovery data exists: {CURRENT_AIRFLOW_DEPLOYMENT_MODEL}] (VERIFIED-WEB / VERIFIED-GONG)
- **Current Airflow Deployment**: [{CURRENT_AIRFLOW_DEPLOYMENT_MODEL} | Versions: {CURRENT_AIRFLOW_VERSIONS} | Envs: {CURRENT_AIRFLOW_ENVIRONMENTS_COUNT}] (VERIFIED-SF — from discovery call)
- **Data Warehouse**: [Confirmed from web — or "Not confirmed"] (VERIFIED-WEB / VERIFIED-GONG)
- **Other Confirmed Tools**: [Tools confirmed by web or Gong only — with source and verbatim evidence] (VERIFIED-WEB / VERIFIED-GONG)
- **Competition**: [{SF_OPPS.COMPETITION} from prior opp — if present] (VERIFIED-SF)

### Hiring Signals
- **Active Job Postings**: [titles found + links] (VERIFIED-WEB)
- **Key Requirements from JDs**: [specific tools, verbatim language — especially Airflow/orchestration mentions] (VERIFIED-WEB)
- **Hiring Velocity**: [growing/stable/shrinking — from web] (VERIFIED-WEB)

### Data Challenges & Pain Points
- [Confirmed challenges from SF_OPPS discovery notes or Gong transcripts] (VERIFIED-SF / VERIFIED-GONG)
- [Inferred from stack, scale, and industry] (GENERATED)
- [From job posting language — verbatim: "reliability", "observability", "on-call"] (VERIFIED-WEB)
- [From engineering blog posts about infrastructure challenges] (VERIFIED-WEB)

### Astronomer Alignment
**Why Astronomer fits**:
- [Bullet 1 — tied to Gong discovery finding, web-confirmed stack signal, or Leadfeeder visit] (source tag)
- [Bullet 2 — tied to their scale/industry] (source tag)
- [Bullet 3 — tied to buying signals or prior opp] (source tag)

**Potential objections**:
- [Why they might not buy — loss reason from prior opp if available, otherwise inferred] (VERIFIED-SF / GENERATED)

#### Website Engagement (astronomer.io visits)

> Combine Salesforce-matched Leadfeeder data (SF: LF_WEBSITE_VISITS) and person-level contact visits (SF: SF_CONTACTS).

**IP-level visits (LF_WEBSITE_VISITS — company matched via Salesforce):**
- **Total visits (last 6mo)**: [count] (VERIFIED-SF-LF)
- **Most recent**: [date] (VERIFIED-SF-LF)
- **Top pages visited** (ranked by recency/frequency):

| Page | Date | Duration | Signal |
|------|------|----------|--------|
| [URL or page name] | [date] | [sec] | [HIGH=/pricing,/demo,/trial | MED=/docs,/astro | LOW=/blog,homepage] |

**Person-level visits (SF_CONTACTS — named individuals):**
| Contact Title | Pricing Page | Airflow Debug Page | DAG Debug Page | MQL Date |
|---|---|---|---|---|
| [title] | [date or —] | [date or —] | [date or —] | [date or —] |

> Flag any contact with a pricing page visit in the last 30 days as **HIGH urgency**.

> If no LF or contact visit data: "No astronomer.io visit data found — cold outreach."

**Visit Summary for Outreach**: [1-2 sentences synthesizing visit data into an actionable insight. Example: "Two contacts visited Airflow debugging docs last month and one hit the pricing page — looks like active evaluation."] (GENERATED)

#### Key Contacts (Salesforce)

> From SF_CONTACTS — prioritized by title relevance then recency.

| Title | Lead Score | Last Activity | Pricing Visit | Opted Out | SF URL |
|-------|-----------|---------------|---------------|-----------|--------|
| [title] | [grade] | [date] | [date or —] | [yes/no] | [link] |

> Tier contacts: HIGH = VP/Director Eng, Head/Director of Data, Data Platform Lead, Staff/Principal Data Eng. MED = Data Eng, Analytics Eng, Data Scientist. LOW = non-technical roles.
> If no SF_CONTACTS: "No contacts found in Salesforce for this account."

#### Prior Conversations (Gong + SF_OPPS)

**Opportunity History (SF_OPPS)**:

| Opp Name | Stage | Won/Lost | ACV | Created | Close | Loss Reason |
|---|---|---|---|---|---|---|
| [name] | [stage] | [W/L/Open] | [$] | [date] | [date] | [reason] |

- **Airflow Experience (from discovery)**: [{AIRFLOW_EXPERIENCE}] (VERIFIED-SF)
- **Airflow Deployment Model**: [{CURRENT_AIRFLOW_DEPLOYMENT_MODEL}] (VERIFIED-SF)
- **Competition in deal**: [{COMPETITION}] (VERIFIED-SF)
- **Cloud provider confirmed**: [{CLOUD_PROVIDER}] (VERIFIED-SF)

**Gong Calls**:

| Date | Their Participants | Astronomer | Summary |
|------|-------------------|------------|---------|
| [date] | [names + titles] | [names] | [2-3 sentences: topics, pain points, outcome] |

- **Relationship Status**: [Active opp / Stalled / Closed-lost / Churned / Never engaged] (VERIFIED-GONG / VERIFIED-SF)
- **Key Pain Points from Calls**: [exact quotes where possible] (VERIFIED-GONG)
- **Objections Raised**: [what they pushed back on] (VERIFIED-GONG)
- **Decision Makers Identified**: [names + titles] (VERIFIED-GONG / VERIFIED-SF)
- **Open Follow-Ups**: [commitments or next steps promised] (VERIFIED-GONG)
- **Tech Stack from Calls**: [tools mentioned — tag with call date] (VERIFIED-GONG)

> If no Gong calls and no SF_OPPS: "No prior Astronomer conversations found. Cold outreach."

#### Prior Email Replies (Apollo)

**Replies**:
- **[Contact name]** ([title]) replied on [date]: "[full reply text]" (VERIFIED-SF)

> If no replies: "No replies received from {COMPANY_NAME} contacts in Apollo."

### Intent & Engagement Signals (Snowflake)
- **Acct Score**: {ACCT_SCORE} | Drivers: {ACCT_SCORE_POSITIVE_DRIVERS} / {ACCT_SCORE_NEGATIVE_DRIVERS} (VERIFIED-SF)
- **Smoke Score**: {SMOKE_SCORE} | **Fire Score**: {FIRE_SCORE} (VERIFIED-SF)
- **Last MQL**: {LAST_MQL_DATE} | **Cosmos doc**: {LAST_COSMOS_DOC_VIEW_DATE} | **DAG factory**: {LAST_DAG_FACTORY_DOWNLOAD_DATE} (VERIFIED-SF)

### Recent News & Events
- [Date] — [Event/news item] (VERIFIED-WEB)

### Competitive Landscape
- **Current Orchestration**: [Airflow self-hosted / MWAA / Prefect / Dagster / none identified — source] (VERIFIED-SF / VERIFIED-GONG / VERIFIED-WEB)
- **Prior Competitive Loss**: [{COMPETITION} from SF_OPPS — if present] (VERIFIED-SF)
- **Competitive Risk**: [are they evaluating alternatives?] (VERIFIED-GONG / GENERATED)

### Outreach Context

#### Engineering Blog & Tech Stack Insights
- **[Blog Post Title]** ([date], [URL]) (VERIFIED-WEB)
  - Key excerpt: "[relevant quote about their stack or challenges]"
  - Tools mentioned: [specific technologies]

> If none: "No engineering blog content found."

#### Job Posting Details
- **[Job Title]** ([URL]) (VERIFIED-WEB)
  - Key requirements: [tools, responsibilities]
  - Notable language: "[verbatim pain point language]"

> If none: "No relevant data/platform job postings found."

#### Company Self-Description
- **Mission/tagline**: "[their own words]" (VERIFIED-WEB)
- **Key products/services**: [what they sell] (VERIFIED-WEB)
- **Target customers**: [who they serve] (VERIFIED-WEB)

### Persona Talking Points (GENERATED)

> Only generate for personas where we have supporting evidence from SF_CONTACTS titles, Gong participants, or confirmed stack signals. Skip personas with no evidence.

**For Engineering / Data Platform Leadership** (VP Eng, Head of Data, Data Platform Lead):
- [Talking point: team velocity, reliability SLAs, build-vs-buy — tied to their specific stack or opp history] (GENERATED)
- [Talking point connecting Astronomer to their business goals or stack signal] (GENERATED)

**For Individual Contributors** (Senior Data Engineer, Staff Platform Engineer):
- [Talking point: developer experience, DAG authoring, CI/CD for pipelines — reference their confirmed tools] (GENERATED)

### How Astronomer Can Help (GENERATED)

Based on confirmed signals from Snowflake and web research, generate 2-4 specific use cases where Astronomer delivers value. Each use case must:
- Be tied to a real signal (HG_AIRFLOW, EVIDENCE_OF_AIRFLOW, a confirmed tool, a job posting phrase, opp history)
- Explain what the Airflow DAG would actually do — reference their specific tools by name
- Explain what pain it removes, tied to their business context

Format:
1. **[Use Case Name]**: [2-3 sentences — specific workflow, why it matters, what pain it removes]
2. **[Use Case Name]**: [same format]

- **Astronomer differentiator**: [1-2 sentences — why managed Airflow is better than self-hosting or their current tool, based on their specific situation]
- **Conversation starter**: [One compelling question grounded in a specific signal — a stack confirmation, job posting phrase, pricing page visit, or prior opp finding]

### Summary & Recommended Next Steps
[2-3 sentences for the AE: who the company is, why they're a fit (or not), what the entry point is, what to do first. If SF_CONTACTS shows a pricing page visit or there's an open opp, lead with that.]
```
