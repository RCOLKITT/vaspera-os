# VasperaOS

<p align="center">
  <strong>The Autonomous Business Operating System</strong>
</p>

<p align="center">
  <em>One founder. Multiple products. AI agents running everything.</em>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#agents">Agents</a> •
  <a href="#roadmap">Roadmap</a>
</p>

---

## What is VasperaOS?

VasperaOS is an open-source framework for building **autonomous businesses** — companies that run themselves with minimal human intervention through AI agents.

Inspired by the prediction that the first one-person billion-dollar company will emerge by 2026, VasperaOS provides the infrastructure to:

- **Build** — AI agents that write code, run tests, deploy changes
- **Run** — AI agents that monitor, detect incidents, auto-remediate
- **Market** — AI agents that manage ads, create content, optimize SEO
- **Support** — AI agents that answer questions, triage tickets, prevent churn
- **Sell** — AI agents that handle outreach, onboarding, upsells
- **Finance** — AI agents that track revenue, manage billing, report metrics

## Features

- **Multi-Product Support** — Manage multiple products from a single control plane
- **Agent Orchestration** — Built on CrewAI and LangGraph for robust multi-agent workflows
- **MCP Integration** — Connect to any tool via Model Context Protocol
- **Persistent Memory** — Cross-agent context via VasperaMemory
- **Rules Engine** — Configurable automation rules (3x Kill Rule, 20% Scale Rule, etc.)
- **Self-Hosted** — Run on your infrastructure, own your data

## Quick Start

```bash
# Clone the repo
git clone https://github.com/AgriciDaniel/vaspera-os.git
cd vaspera-os

# Install dependencies
pip install -e .

# Copy and configure secrets
cp config/secrets.example.yaml config/secrets.yaml

# Configure your products
vim config/products.yaml

# Start the orchestrator
python scripts/run_agents.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     VASPERA-OS                          │
├─────────────────────────────────────────────────────────┤
│                  COMMAND CENTER                          │
│           (Claude + VasperaMemory + MCP)                │
├─────────────────────────────────────────────────────────┤
│                AGENT ORCHESTRATOR                        │
│                (CrewAI / LangGraph)                     │
├─────────────────────────────────────────────────────────┤
│  BUILD    │    RUN     │   MARKET   │  SUPPORT  │ SELL │
│  AGENTS   │   AGENTS   │   AGENTS   │  AGENTS   │AGENTS│
├─────────────────────────────────────────────────────────┤
│              MCP SERVERS & INTEGRATIONS                  │
│  GitHub • Stripe • Vercel • Sentry • Ads • Chatwoot    │
├─────────────────────────────────────────────────────────┤
│                   PRODUCT REPOS                          │
│  product-a  │  product-b  │  product-c  │  ...         │
└─────────────────────────────────────────────────────────┘
```

## Agents

| Category | Agent | What It Does |
|----------|-------|--------------|
| **Build** | Code Agent | Implements features, fixes bugs |
| | Test Agent | Runs tests, ensures quality |
| | Deploy Agent | Ships code to production |
| **Run** | Monitor Agent | Watches health metrics |
| | Incident Agent | Auto-remediates issues |
| **Market** | Ads Agent | Manages paid advertising |
| | Content Agent | Creates and distributes content |
| | SEO Agent | Optimizes search rankings |
| **Support** | Chat Agent | Answers customer questions |
| | Ticket Agent | Triages and routes issues |
| **Sell** | Outreach Agent | Generates leads |
| | Churn Agent | Prevents customer churn |
| **Finance** | Revenue Agent | Tracks financial metrics |

## Open Source Stack

VasperaOS builds on proven open-source tools:

| Component | Tool |
|-----------|------|
| Agent Framework | [CrewAI](https://github.com/crewAIInc/crewAI) |
| Workflows | [LangGraph](https://github.com/langchain-ai/langgraph) |
| MCP Protocol | [MCP Servers](https://github.com/modelcontextprotocol/servers) |
| Support | [Chatwoot](https://github.com/chatwoot/chatwoot) |
| Analytics | [PostHog](https://github.com/PostHog/posthog) |
| CMS | [Ghost](https://github.com/TryGhost/Ghost) |
| Monitoring | [Sentry](https://github.com/getsentry/sentry) |

## Roadmap

- [x] Project structure and plan
- [ ] Core orchestration framework
- [ ] Monitor and Deploy agents
- [ ] Ads automation system
- [ ] Support bot integration
- [ ] Content pipeline
- [ ] Revenue tracking
- [ ] Build agents (code/test/review)
- [ ] Full documentation
- [ ] v1.0 release

See [PLAN.md](PLAN.md) for the detailed implementation roadmap.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key areas:
- MCP servers for new platforms
- Agent improvements
- Integrations
- Documentation

## License

MIT License — use it, modify it, build on it.

---

<p align="center">
  Built with quiet brilliance by <a href="https://vasperacapital.com">Vaspera Capital</a>
</p>
