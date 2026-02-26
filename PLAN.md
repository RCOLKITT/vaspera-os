# VasperaOS

**The Autonomous Business Operating System**

*One founder. Multiple products. AI agents running everything.*

---

## Vision

Build and operate a portfolio of products (VasperaMemory, WealthSynapse, NutriFitAI, VasperaShield, VasperaTrade, etc.) with minimal human intervention. Each product lives in its own repository, but all share a unified autonomous operating layer.

**Target:** Join the first wave of one-person billion-dollar companies by 2026.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          VASPERA-OS                                  │
│                   Autonomous Business Operating System               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                     COMMAND CENTER                              │ │
│  │              (Claude Code + VasperaMemory + MCP)               │ │
│  │                                                                 │ │
│  │  "Check all products, pause underperforming ads, draft         │ │
│  │   changelog for VasperaMemory release, respond to              │ │
│  │   enterprise inquiry for WealthSynapse"                        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                │                                     │
│                                ▼                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    AGENT ORCHESTRATOR                           │ │
│  │                      (CrewAI / LangGraph)                       │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                │                                     │
│         ┌──────────────────────┼──────────────────────┐             │
│         ▼                      ▼                      ▼             │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐        │
│  │    BUILD    │       │     RUN     │       │   MARKET    │        │
│  │   AGENTS    │       │   AGENTS    │       │   AGENTS    │        │
│  └─────────────┘       └─────────────┘       └─────────────┘        │
│         │                      │                      │             │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐        │
│  │   SUPPORT   │       │    SELL     │       │   FINANCE   │        │
│  │   AGENTS    │       │   AGENTS    │       │   AGENTS    │        │
│  └─────────────┘       └─────────────┘       └─────────────┘        │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                         PRODUCT REPOS                                │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │
│  │ vaspera-  │ │  wealth-  │ │ nutrifit- │ │  vaspera- │  ...      │
│  │  memory   │ │  synapse  │ │    ai     │ │  shield   │           │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Open Source Foundation

We build on proven, battle-tested open source projects. No reinventing wheels.

### Core Infrastructure

| Component | Open Source Tool | Purpose | Stars |
|-----------|------------------|---------|-------|
| Agent Orchestration | [CrewAI](https://github.com/crewAIInc/crewAI) | Multi-agent coordination | 25k+ |
| Graph Workflows | [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful agent workflows | 8k+ |
| MCP Protocol | [MCP Servers](https://github.com/modelcontextprotocol/servers) | Tool integrations | 15k+ |
| Memory Layer | VasperaMemory (ours) | Cross-agent context | — |

### MCP Servers (Ready to Use)

| Server | Source | What It Does |
|--------|--------|--------------|
| [GitHub MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/github) | Official | Issues, PRs, repos |
| [Google Ads MCP](https://github.com/google-marketing-solutions/google_ads_mcp) | Google | Ad management |
| [Stripe MCP](https://github.com/stripe/stripe-mcp) | Stripe | Payments, billing |
| [Slack MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/slack) | Official | Team notifications |
| [Linear MCP](https://github.com/jerhadf/linear-mcp-server) | Community | Issue tracking |
| [Sentry MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/sentry) | Official | Error monitoring |
| [Filesystem MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | Official | File operations |
| [PostgreSQL MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) | Official | Database queries |
| Vercel MCP | Integrated | Deployments (already in Claude Code) |

### MCP Servers (To Build)

| Server | Priority | Purpose |
|--------|----------|---------|
| Meta Ads MCP | P1 | Facebook/Instagram ad management |
| LinkedIn Ads MCP | P2 | B2B advertising |
| TikTok Ads MCP | P2 | TikTok ad management |
| Reddit Ads MCP | P3 | Developer community ads |
| Chatwoot MCP | P1 | Customer support integration |
| PostHog MCP | P2 | Product analytics |
| Ghost MCP | P2 | Content publishing |
| Mercury MCP | P3 | Banking/finance |

### Support & Operations

| Component | Open Source Tool | Purpose |
|-----------|------------------|---------|
| Customer Support | [Chatwoot](https://github.com/chatwoot/chatwoot) | Intercom alternative |
| Issue Tracking | [Plane](https://github.com/makeplane/plane) | Linear alternative |
| Analytics | [PostHog](https://github.com/PostHog/posthog) | Product analytics |
| CMS | [Ghost](https://github.com/TryGhost/Ghost) | Blog/newsletter |
| Marketing Automation | [Mautic](https://github.com/mautic/mautic) | Email sequences |
| Monitoring | [Sentry](https://github.com/getsentry/sentry) | Error tracking |
| Uptime | [Upptime](https://github.com/upptime/upptime) | Status page |

---

## Multi-Product Architecture

Each Vaspera product is an independent repository with its own:
- Codebase
- CI/CD pipeline
- Deployment
- Billing (Stripe)
- Support queue (Chatwoot)

VasperaOS connects to all of them via MCP and provides unified:
- Monitoring across all products
- Ad management across all products
- Support escalation across all products
- Financial reporting across all products
- Content/marketing for all products

### Product Registry

```yaml
# config/products.yaml
products:
  vaspera-memory:
    repo: "AgriciDaniel/vaspera-memory"
    domain: "vasperamemory.com"
    type: "open-source-saas"
    stripe_account: "acct_xxx"
    chatwoot_inbox: 1
    ad_platforms: ["google", "linkedin", "reddit"]

  wealth-synapse:
    repo: "AgriciDaniel/wealth-synapse"
    domain: "wealthsynapse.com"
    type: "saas"
    stripe_account: "acct_yyy"
    chatwoot_inbox: 2
    ad_platforms: ["google", "meta", "linkedin"]

  nutrifit-ai:
    repo: "AgriciDaniel/nutrifit-ai"
    domain: "nutrifitai.com"
    type: "consumer-app"
    stripe_account: "acct_zzz"
    chatwoot_inbox: 3
    ad_platforms: ["meta", "tiktok", "google"]

  vaspera-shield:
    repo: "AgriciDaniel/vaspera-shield"
    domain: "vasperashield.com"
    type: "saas"
    stripe_account: "acct_aaa"
    chatwoot_inbox: 4
    ad_platforms: ["google", "linkedin"]

  vaspera-trade:
    repo: "AgriciDaniel/vaspera-trade"
    domain: "vasperatrade.com"
    type: "fintech"
    stripe_account: "acct_bbb"
    chatwoot_inbox: 5
    ad_platforms: ["google", "meta"]
```

---

## Agent Definitions

### BUILD AGENTS

#### Code Agent
```yaml
name: code_agent
role: "Senior Software Engineer"
goal: "Implement features and fix bugs across all Vaspera products"
backstory: |
  Expert in TypeScript, Python, and React. Deep knowledge of all
  Vaspera codebases via VasperaMemory context. Can access any repo
  via GitHub MCP.
tools:
  - github_mcp
  - filesystem_mcp
  - vaspera_memory
triggers:
  - github_issue_created
  - slack_message_contains: "bug"
  - error_rate_spike
```

#### Test Agent
```yaml
name: test_agent
role: "QA Engineer"
goal: "Ensure code quality through automated testing"
backstory: |
  Runs test suites, generates new tests for uncovered code,
  reports failures with context.
tools:
  - github_mcp
  - bash_executor
triggers:
  - pull_request_opened
  - code_agent_completed
```

#### Deploy Agent
```yaml
name: deploy_agent
role: "DevOps Engineer"
goal: "Ship code to production safely"
backstory: |
  Manages deployments across Vercel, monitors rollouts,
  triggers rollbacks if errors spike.
tools:
  - vercel_mcp
  - github_mcp
  - sentry_mcp
triggers:
  - pull_request_merged
  - manual_deploy_request
```

### RUN AGENTS

#### Monitor Agent
```yaml
name: monitor_agent
role: "Site Reliability Engineer"
goal: "Keep all products healthy and performant"
backstory: |
  Watches error rates, response times, and uptime across all
  products. Escalates issues or triggers auto-remediation.
tools:
  - sentry_mcp
  - vercel_mcp
  - posthog_mcp
  - slack_mcp
triggers:
  - every_5_minutes
  - error_threshold_exceeded
```

#### Incident Agent
```yaml
name: incident_agent
role: "Incident Commander"
goal: "Resolve incidents with minimal human intervention"
backstory: |
  Analyzes incidents, attempts automated fixes (restart, rollback,
  scale), escalates to human only when necessary.
tools:
  - sentry_mcp
  - vercel_mcp
  - github_mcp
  - slack_mcp
triggers:
  - monitor_agent_alert
  - pagerduty_incident
```

### MARKET AGENTS

#### Ads Agent
```yaml
name: ads_agent
role: "Performance Marketing Manager"
goal: "Maximize ROAS across all ad platforms for all products"
backstory: |
  Manages Google, Meta, LinkedIn, TikTok, Reddit ads. Applies
  3x Kill Rule, 20% Scale Rule. Generates weekly reports.
tools:
  - google_ads_mcp
  - meta_ads_mcp
  - linkedin_ads_mcp
  - tiktok_ads_mcp
  - reddit_ads_mcp
triggers:
  - daily_morning
  - spend_threshold_exceeded
  - cpa_threshold_exceeded
rules:
  - if spend > 3x target_cpa and conversions == 0: pause
  - if cpa < 0.8x target_cpa and conversions >= 10: scale_20pct
  - if frequency > 4: alert_creative_fatigue
```

#### Content Agent
```yaml
name: content_agent
role: "Content Marketing Manager"
goal: "Create and distribute content for all products"
backstory: |
  Drafts blog posts, changelogs, social posts, newsletters.
  Submits for human approval before publishing.
tools:
  - ghost_mcp
  - github_mcp  # for changelogs
  - twitter_api
  - linkedin_api
triggers:
  - weekly_content_calendar
  - product_release
  - manual_request
```

#### SEO Agent
```yaml
name: seo_agent
role: "SEO Specialist"
goal: "Improve organic search rankings for all products"
backstory: |
  Analyzes search console data, suggests optimizations,
  generates meta descriptions, finds keyword opportunities.
tools:
  - search_console_api
  - posthog_mcp
  - ghost_mcp
triggers:
  - weekly_seo_audit
  - new_content_published
```

### SUPPORT AGENTS

#### Chat Agent
```yaml
name: chat_agent
role: "Customer Support Representative"
goal: "Answer customer questions accurately and quickly"
backstory: |
  Has full context of all products via VasperaMemory. Answers
  common questions, escalates complex issues to humans.
tools:
  - chatwoot_mcp
  - vaspera_memory
  - docs_search
triggers:
  - new_chat_message
  - support_ticket_created
```

#### Ticket Agent
```yaml
name: ticket_agent
role: "Support Escalation Manager"
goal: "Triage and route support tickets efficiently"
backstory: |
  Categorizes tickets, assigns priority, routes to appropriate
  channel (bug → Code Agent, billing → human, feature → backlog).
tools:
  - chatwoot_mcp
  - linear_mcp
  - github_mcp
  - slack_mcp
triggers:
  - chat_agent_escalation
  - email_received
```

### SELL AGENTS

#### Outreach Agent
```yaml
name: outreach_agent
role: "Business Development Representative"
goal: "Generate qualified leads through personalized outreach"
backstory: |
  Identifies prospects, personalizes outreach, follows up,
  books meetings for high-intent leads.
tools:
  - apollo_api
  - email_api
  - calendar_api
triggers:
  - new_signup_enterprise_signal
  - weekly_outreach_batch
```

#### Churn Agent
```yaml
name: churn_agent
role: "Customer Success Manager"
goal: "Prevent churn by identifying and engaging at-risk users"
backstory: |
  Monitors usage patterns, identifies drop-off signals,
  triggers intervention sequences.
tools:
  - posthog_mcp
  - stripe_mcp
  - chatwoot_mcp
  - email_api
triggers:
  - usage_drop_detected
  - subscription_cancellation_initiated
```

### FINANCE AGENTS

#### Revenue Agent
```yaml
name: revenue_agent
role: "Financial Analyst"
goal: "Track and report revenue across all products"
backstory: |
  Aggregates Stripe data across all products, calculates MRR,
  churn, LTV, generates financial reports.
tools:
  - stripe_mcp
  - postgres_mcp
  - slack_mcp
triggers:
  - daily_revenue_report
  - weekly_financial_summary
  - monthly_close
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)

#### Week 1: Core Setup
- [ ] Initialize vaspera-os repository
- [ ] Set up project structure
- [ ] Install CrewAI + LangGraph
- [ ] Configure MCP server connections
- [ ] Set up product registry (config/products.yaml)
- [ ] Integrate VasperaMemory for cross-agent context

#### Week 2: First Agents
- [ ] Implement Monitor Agent (Sentry + Vercel)
- [ ] Implement basic Chat Agent (Chatwoot)
- [ ] Implement Deploy Agent (Vercel + GitHub)
- [ ] Set up Slack notifications
- [ ] Create agent testing framework

### Phase 2: Marketing Automation (Weeks 3-4)

#### Week 3: Ads Infrastructure
- [ ] Build Google Ads integration (MCP exists)
- [ ] Build Meta Ads MCP server
- [ ] Implement Ads Agent core logic
- [ ] Implement 3x Kill Rule automation
- [ ] Implement 20% Scale Rule automation

#### Week 4: Content & Analytics
- [ ] Set up Ghost CMS
- [ ] Build Ghost MCP server
- [ ] Implement Content Agent
- [ ] Set up PostHog
- [ ] Build PostHog MCP server
- [ ] Create unified analytics dashboard

### Phase 3: Support & Sales (Weeks 5-6)

#### Week 5: Support Stack
- [ ] Deploy Chatwoot (self-hosted)
- [ ] Build Chatwoot MCP server
- [ ] Implement Chat Agent with AI responses
- [ ] Implement Ticket Agent routing
- [ ] Create escalation workflows

#### Week 6: Revenue Operations
- [ ] Implement Outreach Agent
- [ ] Implement Churn Agent
- [ ] Implement Revenue Agent
- [ ] Build unified revenue dashboard
- [ ] Set up automated financial reporting

### Phase 4: Full Automation (Weeks 7-8)

#### Week 7: Build Agents
- [ ] Implement Code Agent (issue → PR)
- [ ] Implement Test Agent (automated testing)
- [ ] Implement Review Agent (PR review)
- [ ] Create end-to-end automation tests

#### Week 8: Integration & Polish
- [ ] Implement Incident Agent (auto-remediation)
- [ ] Build command center dashboard
- [ ] Create runbooks for all agents
- [ ] Load test agent orchestration
- [ ] Documentation and open source prep

---

## Directory Structure

```
vaspera-os/
├── README.md
├── PLAN.md                      # This file
├── LICENSE                      # MIT
├── pyproject.toml               # Python dependencies
│
├── config/
│   ├── products.yaml            # Product registry
│   ├── agents.yaml              # Agent definitions
│   ├── rules.yaml               # Automation rules
│   └── secrets.example.yaml     # Secret template
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── orchestrator.py      # Agent orchestration (CrewAI)
│   │   ├── memory.py            # VasperaMemory integration
│   │   ├── scheduler.py         # Cron job management
│   │   └── events.py            # Event bus
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py              # Base agent class
│   │   │
│   │   ├── build/
│   │   │   ├── code_agent.py
│   │   │   ├── test_agent.py
│   │   │   └── deploy_agent.py
│   │   │
│   │   ├── run/
│   │   │   ├── monitor_agent.py
│   │   │   └── incident_agent.py
│   │   │
│   │   ├── market/
│   │   │   ├── ads_agent.py
│   │   │   ├── content_agent.py
│   │   │   └── seo_agent.py
│   │   │
│   │   ├── support/
│   │   │   ├── chat_agent.py
│   │   │   └── ticket_agent.py
│   │   │
│   │   ├── sell/
│   │   │   ├── outreach_agent.py
│   │   │   └── churn_agent.py
│   │   │
│   │   └── finance/
│   │       └── revenue_agent.py
│   │
│   ├── mcp_servers/
│   │   ├── __init__.py
│   │   ├── meta_ads/            # Meta Ads MCP (build)
│   │   ├── linkedin_ads/        # LinkedIn Ads MCP (build)
│   │   ├── tiktok_ads/          # TikTok Ads MCP (build)
│   │   ├── chatwoot/            # Chatwoot MCP (build)
│   │   ├── posthog/             # PostHog MCP (build)
│   │   └── ghost/               # Ghost MCP (build)
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── stripe.py
│   │   ├── github.py
│   │   ├── slack.py
│   │   └── email.py
│   │
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── engine.py            # Rules engine
│   │   ├── ads_rules.py         # 3x Kill, 20% Scale
│   │   ├── support_rules.py     # Escalation rules
│   │   └── incident_rules.py    # Auto-remediation rules
│   │
│   └── dashboard/
│       ├── __init__.py
│       └── app.py               # Streamlit dashboard
│
├── tests/
│   ├── __init__.py
│   ├── test_agents/
│   ├── test_rules/
│   └── test_integrations/
│
├── scripts/
│   ├── setup.sh                 # Initial setup
│   ├── run_agents.py            # Start agent orchestrator
│   └── seed_data.py             # Seed test data
│
└── docs/
    ├── agents.md                # Agent documentation
    ├── mcp-servers.md           # MCP server guide
    ├── rules.md                 # Rules documentation
    └── deployment.md            # Deployment guide
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Language | Python 3.12 | CrewAI, LangGraph, most MCP servers |
| Agent Framework | CrewAI | Fastest to production, role-based |
| Workflows | LangGraph | Complex stateful flows |
| MCP Runtime | MCP Python SDK | Official SDK |
| Memory | VasperaMemory | Our product, dog-fooding |
| Database | PostgreSQL | Reliable, MCP server exists |
| Cache | Redis | Fast, simple |
| Queue | Redis (RQ) | Lightweight job queue |
| Dashboard | Streamlit | Fast to build, Python-native |
| Hosting | Railway / Fly.io | Simple, scalable |
| CI/CD | GitHub Actions | Already using GitHub |

---

## Success Metrics

### Operational Efficiency

| Metric | Current (Manual) | Target (Automated) |
|--------|------------------|-------------------|
| Time spent on ops/week | 40+ hours | <5 hours |
| Incident response time | Hours | Minutes |
| Ad optimization frequency | Weekly | Continuous |
| Content output | 1-2 posts/week | 5-10 posts/week |
| Support response time | Hours | <1 minute (AI) |

### Business Metrics

| Metric | 3 Months | 6 Months | 12 Months |
|--------|----------|----------|-----------|
| Products automated | 2 | 4 | All |
| MRR (total) | $10k | $50k | $200k+ |
| Support tickets auto-resolved | 50% | 70% | 85% |
| Ad ROAS improvement | +20% | +40% | +60% |
| Code PRs from agents | 10% | 30% | 50% |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Agent makes bad decision | Human approval gates for high-impact actions |
| API rate limits | Queuing, backoff, caching |
| Cost overrun (AI tokens) | Budget limits, model tiering (Haiku for simple tasks) |
| Data breach | Self-host sensitive systems, encryption |
| Single point of failure | Redundancy, graceful degradation |
| Agent hallucination | Grounding with VasperaMemory, verification steps |

---

## Open Source Strategy

1. **Core VasperaOS** — MIT licensed, open source
2. **MCP Servers we build** — MIT licensed, contribute back
3. **Agent definitions** — Open source (community can contribute)
4. **Hosted version** — Paid tier for those who don't want to self-host
5. **Enterprise features** — Team management, audit logs, SSO

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/AgriciDaniel/vaspera-os.git
cd vaspera-os

# Install dependencies
pip install -e .

# Copy config template
cp config/secrets.example.yaml config/secrets.yaml
# Edit with your API keys

# Set up product registry
# Edit config/products.yaml with your products

# Run the orchestrator
python scripts/run_agents.py

# Or run specific agent
python -m src.agents.market.ads_agent
```

---

## Contributing

We welcome contributions! Areas where help is needed:

1. **MCP Servers** — Meta Ads, LinkedIn Ads, TikTok Ads, etc.
2. **Agent improvements** — Better prompts, more capabilities
3. **Integrations** — New tools and services
4. **Documentation** — Guides, tutorials, examples
5. **Testing** — Unit tests, integration tests, load tests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License — use it, modify it, build on it.

---

*Built with quiet brilliance by [Vaspera Capital](https://vasperacapital.com)*
