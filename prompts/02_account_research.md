# Account Research Summary

You are generating an AE brief for **{COMPANY_NAME}** ({DOMAIN}) as a prospective Astronomer (Apache Airflow) customer.

## Instructions

Using the RAW INTELLIGENCE block provided above, generate a structured account research summary. Every bullet point MUST be tagged with its verification status:

- `(VERIFIED-EXA)` — Confirmed by Exa web research
- `(VERIFIED-LF)` — Confirmed by Leadfeeder website visit data
- `(VERIFIED-CR)` — Confirmed by Common Room community/contact data
- `(VERIFIED-GONG)` — Confirmed by Gong call transcript data
- `(VERIFIED-APOLLO)` — Confirmed by Apollo CRM email/contact data
- `(GENERATED)` — Inferred or synthesized from available data (not directly confirmed)

If a data source returned no results, explicitly note "No data available from [source]" in the relevant section.

---

## Output Format

```markdown
## Account Research: {COMPANY_NAME}

### Email Brief

> **This is the #1 section for AI email generation.** It distills the entire report into the most actionable outreach inputs. The email writer should start here, then reference other sections for supporting detail.

- **Outreach Type**: [WARM — prior Gong calls or Apollo replies exist | FOLLOW-UP — emails sent but no reply yet | COLD — no prior conversations or outreach] (VERIFIED-GONG / VERIFIED-APOLLO / GENERATED)
- **Urgency**: [HOT — reach out this week | WARM — reach out this month | COOL — add to nurture sequence] (GENERATED)
- **Urgency Rationale**: [1 sentence explaining why — e.g., "Visited pricing page 3x in last 2 weeks + just raised Series B" or "No buying signals, general fit only"] (GENERATED)

**Top 3 Personalization Hooks** (ranked by impact for email outreach):
1. [Most compelling hook — e.g., a specific Gong conversation to follow up on, a pricing page visit, a case study quote, a job posting phrase] (source tag)
2. [Second hook — e.g., a recent product launch that creates pipeline needs, an engineering blog post about their stack] (source tag)
3. [Third hook — e.g., a new funding round, a hiring signal, a community question about Airflow] (source tag)

**If prior Gong calls exist**:
- **Last Call**: [date] with [their participant names/titles] and [Astronomer participant] (VERIFIED-GONG)
- **Call Outcome**: [1 sentence — what was discussed, where it left off, any follow-ups promised] (VERIFIED-GONG)
- **Email Angle**: [1 sentence — how to reference the prior conversation naturally] (GENERATED)

**If no prior calls**:
- **Cold Outreach Angle**: [1 sentence — the single strongest reason to reach out, framed as a question or observation] (GENERATED)

### Company Overview
- **Description**: [1-2 sentence company description] (VERIFIED-EXA)
- **Founded**: [year] (VERIFIED-EXA)
- **Headquarters**: [location] (VERIFIED-EXA)
- **Employees**: [count or range] (VERIFIED-EXA) / (VERIFIED-CR)
- **Industry**: [industry] (VERIFIED-EXA)
- **Funding**: [total raised, last round, valuation if known] (VERIFIED-EXA)
- **Revenue**: [estimate if available] (VERIFIED-EXA) / (VERIFIED-CR)

### Tech Stack
- **Cloud Provider**: [AWS/GCP/Azure/multi-cloud] (source tag)
- **Data Warehouse**: [Snowflake/BigQuery/Redshift/Databricks/etc.] (source tag)
- **Orchestration**: [Current tool if known — Airflow, Prefect, Dagster, Step Functions, none identified] (source tag)
- **Other Data Tools**: [dbt, Spark, Kafka, Fivetran, etc.] (source tag)
- **CI/CD / DevOps**: [relevant tools] (source tag)
- **Community Stack Signals**: [Any tools mentioned in GitHub repos, forum posts, or community activity] (VERIFIED-CR)

### Hiring Signals
- **Data Engineering Roles**: [active postings mentioning pipelines, orchestration, Airflow, data platform] (VERIFIED-EXA)
- **Platform Engineering Roles**: [active postings for infra/platform roles] (VERIFIED-EXA)
- **Key Job Requirements**: [specific technologies or skills mentioned in postings] (VERIFIED-EXA)
- **Hiring Velocity**: [growing/stable/shrinking based on available data] (VERIFIED-EXA)

### Data Challenges & Pain Points
- [Inferred or confirmed challenges based on their stack, scale, and industry] (source tag)
- [Community activity sentiment — are they asking questions about migration, scaling, reliability?] (VERIFIED-CR)
- [Any public post-mortems, blog posts about data infrastructure challenges] (VERIFIED-EXA)

### Astronomer Alignment
**Why Astronomer fits**:
- [Bullet 1 — specific reason tied to their stack/needs] (source tag)
- [Bullet 2 — specific reason tied to their scale/industry] (source tag)
- [Bullet 3 — specific reason tied to buying signals] (source tag)

**Potential objections**:
- [Bullet 1 — why they might not buy] (source tag)

#### Website Engagement

Combine visit data from both Leadfeeder and Common Room into a single view. This section is high-value for outreach — knowing what pages they looked at tells us what they care about.

**Leadfeeder (astronomer.io visits)**:
- **Total Visits**: [count in last 6 months] (VERIFIED-LF)
- **Most Recent Visit**: [date] (VERIFIED-LF)
- **Visit Frequency**: [pattern — weekly/monthly/one-time] (VERIFIED-LF)
- **Top Pages Visited** (ranked by visit count, most visited first):

| Page | Visits | Most Recent | Signal Strength |
|------|--------|-------------|-----------------|
| [URL or page name, e.g., /pricing, /docs/astro, /blog/migrate-airflow] | [count] | [date] | [HIGH/MEDIUM/LOW — pricing/demo=HIGH, docs=MEDIUM, blog/homepage=LOW] |

> Classify each page: pricing, demo request, or trial pages = **HIGH** signal (active buying intent). Documentation, guides, or migration pages = **MEDIUM** signal (evaluating/learning). Blog posts, homepage, or about pages = **LOW** signal (awareness only).
> If no Leadfeeder data: "No Leadfeeder visit data found for {COMPANY_NAME} in the last 6 months."

**Common Room (community web visits)**:
- **Total Visits**: [count in last 90 days] (VERIFIED-CR)
- **Top Pages Visited** (ranked by visit count, most visited first):

| Page | Visits | Most Recent |
|------|--------|-------------|
| [URL] | [count] | [date] |

> If no Common Room data: "No Common Room visit data found for {COMPANY_NAME}."

**Visit Summary for Outreach**: [1-2 sentences synthesizing the visit data into an actionable insight for an SDR/AE. Example: "They've visited the pricing page 3 times in the last month and read 2 migration guides — this looks like active evaluation, not just browsing." Or: "Single homepage visit only — awareness-level interest." If no visit data from either source: "No website engagement detected — cold outreach required."] (GENERATED)

#### Key Contacts (Common Room)
| Name | Title | Email | Engagement |
|------|-------|-------|------------|
| [name] | [title] | [email] | [recent activity summary] |

> List up to 5 contacts from Common Room, prioritized by: (1) title relevance (VP Eng, Head of Data, Data Platform Lead), (2) engagement recency, (3) has email address.
> If no Common Room data: "No community contacts found for {COMPANY_NAME}."

#### Prior Conversations (Gong)

> If calls found, list each call. If not, note it's cold outreach.

| Date | Their Participants | Astronomer Participants | Summary |
|------|-------------------|------------------------|---------|
| [date] | [names + titles] | [names] | [2-3 sentence summary: topics, pain points, objections, outcome] |

- **Relationship Status**: [Active opportunity / Stalled / Closed-lost / Churned / Never engaged] (VERIFIED-GONG)
- **Key Pain Points from Calls**: [bullet list of specific pain points they mentioned] (VERIFIED-GONG)
- **Objections Raised**: [any concerns or pushback they expressed] (VERIFIED-GONG)
- **Tech Stack from Calls**: [specific tools, platforms, cloud providers, data warehouses, orchestration tools mentioned — tag each with the call date] (VERIFIED-GONG)
- **Decision Makers Identified**: [names + titles of people with buying authority from the calls] (VERIFIED-GONG)
- **Open Follow-Ups**: [any commitments or next steps that were promised but may not have happened] (VERIFIED-GONG)

> If no Gong calls: "No prior Astronomer conversations found for {COMPANY_NAME}. This is a cold outreach."

#### Prior Email Replies (Apollo)

> **CRITICAL FOR EMAIL GENERATION**: If someone at this company has replied to Astronomer outreach, the email writer MUST know what they said. Ignoring a prior reply is a dealbreaker.

**Replies**:
- **[Contact name]** ([title]) replied on [date]: "[full reply text]" (VERIFIED-APOLLO)

**Reply Assessment**:
- [1-2 sentences: Was the reply positive (interested, asking for more info), negative (not interested, wrong timing), or neutral (OOO, redirect to someone else)? Is there an open thread to continue?] (GENERATED)

> If no replies found: "No replies received from {COMPANY_NAME} contacts in Apollo."

### Recent News & Events
- [Date] — [Event/news item] (VERIFIED-EXA)
- [Date] — [Event/news item] (VERIFIED-EXA)

### Competitive Landscape
- **Current Orchestration**: [what they use today, if known] (source tag)
- **Competitive Risk**: [are they evaluating alternatives? Any signals from community activity?] (source tag)

### Outreach Context

> **NOTE FOR AI EMAIL GENERATION**: This section provides *supplementary* detail for personalization. It does NOT replace the rest of the report. The email writer should reference the ENTIRE report — including Company Overview, Tech Stack, Hiring Signals, Data Challenges, Astronomer Alignment, Website Engagement, Key Contacts, News, Competitive Landscape, and How Astronomer Can Help — as source material for crafting emails. This section simply adds raw excerpts and quotes that are harder to find elsewhere.

This section captures raw detail from public sources that an AI email writer can reference for personalization. Include only items that are relevant to data infrastructure, orchestration, or Astronomer's value prop.

#### Engineering Blog & Tech Stack Insights
> Extract key quotes or findings from the company's own engineering blog posts about their data infrastructure, pipeline challenges, architecture decisions, or tool choices. Include the blog post title, date, and URL for each. If nothing found, note "No engineering blog content found."

- **[Blog Post Title]** ([date], [URL]) (VERIFIED-EXA)
  - Key excerpt: "[relevant quote about their stack, challenges, or decisions]"
  - Stack/tools mentioned: [specific technologies referenced]

#### Product Announcements & Launches
> Recent product announcements that imply new or growing data pipeline needs (e.g., new ML features, real-time capabilities, expanding into new verticals, scaling to new markets).

- **[Announcement]** ([date]) (VERIFIED-EXA)
  - Data implication: [1 sentence on why this creates orchestration/pipeline needs]

#### Case Studies & Vendor References
> Case studies by other vendors (Snowflake, Databricks, dbt Labs, AWS, etc.) featuring this company, or third-party blog posts that describe their tech stack in detail. These are high-value because vendors typically get stack details verified before publishing.

- **[Case Study/Article Title]** by [vendor/author] ([URL]) (VERIFIED-EXA)
  - Stack details revealed: [specific tools, architecture, data volumes, team size, etc.]
  - Key quote: "[relevant excerpt]"

> If no case studies found: "No vendor case studies or third-party stack references found for {COMPANY_NAME}."

#### Job Posting Details
> Specific requirements and language from their data engineering / platform engineering job postings. Include exact phrases that reveal pain points or priorities — an email writer can mirror this language.

- **[Job Title]** ([URL]) (VERIFIED-EXA)
  - Key requirements: [specific tools, experience, responsibilities listed]
  - Notable language: "[exact phrases that reveal pain points, e.g., 'reduce pipeline failure rates', 'manage complex DAG dependencies', 'scale training data ingestion']"

> If no relevant postings found: "No relevant data/platform job postings found for {COMPANY_NAME}."

#### Company Self-Description
> How the company describes itself and its mission from their website. Useful for connecting Astronomer's value to their own language and goals.

- **Mission/tagline**: "[their own words]" (VERIFIED-EXA)
- **Key products/services**: [what they sell, in their language] (VERIFIED-EXA)
- **Target customers**: [who they serve] (VERIFIED-EXA)

### Persona Talking Points (GENERATED)

> Generate tailored talking points for the most likely outreach targets. Use titles from Common Room contacts, Gong call participants, or infer from the company's likely org structure. Only generate for personas where we have enough context to be specific — don't force generic points.

**For Engineering Leadership** (VP Eng, CTO, Head of Engineering):
- [Talking point focused on: team velocity, reducing operational burden, reliability SLAs, build-vs-buy decisions] (GENERATED)
- [Talking point connecting Astronomer to their business goals or recent strategic moves] (GENERATED)

**For Data/Platform Leadership** (Head of Data, Director of Data Platform, ML Platform Lead):
- [Talking point focused on: pipeline reliability, scaling infrastructure, reducing maintenance toil, observability] (GENERATED)
- [Talking point referencing their specific stack or a pain point from their job postings/blog] (GENERATED)

**For Individual Contributors** (Senior Data Engineer, Staff Platform Engineer, MTS):
- [Talking point focused on: developer experience, DAG authoring, testing, CI/CD for pipelines, open-source Airflow community] (GENERATED)
- [Talking point referencing specific tools they use or technical challenges from job descriptions] (GENERATED)

> Only include persona sections where relevant contacts or titles have been identified. Skip personas with no supporting evidence.

### How Astronomer Can Help (GENERATED)

Based on what we know about {COMPANY_NAME}'s business, tech stack, and growth trajectory, generate 2-4 specific, concrete use cases where Astronomer (managed Apache Airflow) would deliver value. Each use case should:
- Be tied to a real business goal, pain point, or initiative identified in the research above
- Explain what the Airflow pipeline/DAG would actually do (not just "orchestrate data")
- Reference their specific tools (e.g., "orchestrate dbt transformations loading into their Snowflake warehouse" rather than generic "manage data pipelines")
- Be written in a way that an AE or SDR could directly reference in outreach

Format:
1. **[Use Case Name]**: [2-3 sentences describing the specific workflow Astronomer would orchestrate, why it matters for their business, and what pain it removes. Reference their actual stack and business context.]
2. **[Use Case Name]**: [same format]

Also include:
- **Astronomer differentiator**: [1-2 sentences on why managed Airflow via Astronomer is better for them than self-hosting Airflow or using an alternative, based on their specific situation — e.g., team size, scale, cloud provider, compliance needs]
- **Conversation starter**: [A single compelling question or observation an SDR could use to open a conversation, grounded in something specific from the research — a job posting, a tech choice, a recent announcement]

### Summary & Recommended Next Steps
[2-3 sentence summary for the AE: who the company is, why they're a fit, what the entry point is, and what action to take first.]
```
