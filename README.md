<p align="center">
  <img src="./assets/banner.svg" alt="Sahil Kanungo — Systems & Agentic AI Engineer" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/sahil0017/Systera"><img src="https://img.shields.io/badge/Flagship-Systera-0EA5E9?style=flat-square" alt="Systera" /></a>
  <a href="https://dusmzcwbbwktl.cloudfront.net"><img src="https://img.shields.io/badge/Live-CareerPilot%20AI-6366F1?style=flat-square" alt="CareerPilot AI Live" /></a>
  <a href="https://frontend-production-22b1.up.railway.app"><img src="https://img.shields.io/badge/Live-AttributionIQ-10B981?style=flat-square" alt="AttributionIQ Live" /></a>
  <a href="https://github.com/sahil0017/SYNTRIX/releases"><img src="https://img.shields.io/badge/macOS-SYNTRIX%20DMG-1E293B?style=flat-square&logo=apple&logoColor=white" alt="SYNTRIX Release" /></a>
</p>

I design and build **distributed control planes**, **durable multi-agent runtimes**, and **edge-to-cloud AI platforms** — focusing on correctness, transactional guarantees, observability, and native/web product craft.

---

## Flagship Systems & AI Architecture

### Autonomous Engineering & Career Intelligence

| Project | What It Does | Core Architecture & Stack | Links |
| :--- | :--- | :--- | :--- |
| **[Systera](https://github.com/sahil0017/Systera)** | Autonomous engineering intelligence platform that investigates products, designs HLD/LLD graphs, simulates behavior, adversarially reviews designs, and compiles artifacts. | **Go** control plane & durable DAG worker runtime · **PostgreSQL** (forced RLS, transactional outbox, `pgvector`) · **NATS JetStream** · **React/TypeScript** Architecture Studio · **Chrome MV3** Engineering Lens · **Helm / AWS** | [Repo](https://github.com/sahil0017/Systera) |
| **[JobIntelligenceAgent](https://github.com/sahil0017/JobIntelligenceAgent)** *(CareerPilot AI)* | Agentic job-intelligence & autonomous career command center with evidence-backed matching and human-in-the-loop application sagas. | **Go** modular monolith · **Python FastAPI / LangGraph** Cortex · **React 19** console · **AWS Always-Free Tier** (DynamoDB, Step Functions, Bedrock, SNS, CloudFront) | [Repo](https://github.com/sahil0017/JobIntelligenceAgent) · [Live](https://dusmzcwbbwktl.cloudfront.net) |

### Edge, Desktop & Personal Intelligence Platforms

| Project | What It Does | Core Architecture & Stack | Links |
| :--- | :--- | :--- | :--- |
| **[Nexora](https://github.com/sahil0017/Nexora)** | Privacy-first personal intelligence OS unifying urban mobility, wealth, health & sleep clearance, and cross-domain copilot. | **Go (Chi)** control plane · **PostgreSQL + PostGIS** · **Redis** · **Python FastAPI + PyTorch** ML platform · Transactional Outbox → **AWS SNS/SQS** · **SSE** · **Expo React Native** | [Repo](https://github.com/sahil0017/Nexora) |
| **[SYNTRIX](https://github.com/sahil0017/SYNTRIX)** | Native macOS desktop intelligence system with real-time telemetry, local persistence, and an autonomous guardian agent. | **C17** Mach system engine · **Go** local daemon (`syntrixd`) + **WAL SQLite** · **Python** ML forecasting & RL Guardian · **SwiftUI** dark-first HUD | [Repo](https://github.com/sahil0017/SYNTRIX) · [macOS DMG](https://github.com/sahil0017/SYNTRIX/releases) |
| **[HealthAgentApp](https://github.com/sahil0017/HealthAgentApp)** *(Sehat / CORTEX)* | Personal health records & biomarker intelligence platform with evidence-backed, citation-grounded AI Q&A for families. | **Go** API · **Python FastAPI** AI service · **Flutter** cross-platform app · **PostgreSQL + `pgvector`** · PDF care-plan export | [Repo](https://github.com/sahil0017/HealthAgentApp) |
| **[LIFEOS](https://github.com/sahil0017/LIFEOS)** | Local-first personal intelligence platform bridging on-device storage with edge inference and multimodal orchestration. | **Expo / React Native** + on-device **SQLite** · **Cloudflare Workers AI** (Gemma 4 + BGE-M3) · **Python** intelligence engine | [Repo](https://github.com/sahil0017/LIFEOS) |

### Data Pipelines & Engineering Knowledge

| Project | What It Does | Core Architecture & Stack | Links |
| :--- | :--- | :--- | :--- |
| **[AttributionIQ](https://github.com/sahil0017/AttributionIQ)** | First-party marketing attribution pipeline transforming website events, order webhooks & ad spend into channel revenue and ROAS. | **Java 21** · **Spring Boot 4** · **PostgreSQL 17** + **Flyway** · **Streamlit** analytics dashboard · **Railway** | [Repo](https://github.com/sahil0017/AttributionIQ) · [Live](https://frontend-production-22b1.up.railway.app) |
| **[SystemDesign](https://github.com/sahil0017/SystemDesign)** | Staff-level system design library (HLD, LLD, DB, API, Distributed Systems, Java) with an automated GitHub Actions ML dedup PR agent. | **Python** · **GitHub Actions** automation · ML classifier + git-wiki ledger · **Streamlit** | [Repo](https://github.com/sahil0017/SystemDesign) |

---

## Engineering Focus

- **Durable Control Planes:** Transactional outbox patterns, idempotent APIs, PostgreSQL Row-Level Security (RLS), lease-based DAG schedulers, and SSE/JetStream event relays.
- **Evidence-Backed Agentic AI:** Multi-agent orchestration (LangGraph, custom Go/Python runtimes), strict capability & tool gateways, human-in-the-loop approval sagas, and citation-grounded retrieval (`pgvector`, BGE-M3).
- **Native & Full-Stack Surfaces:** From C17 Mach APIs and SwiftUI HUDs on macOS to React/TypeScript studios, Chrome MV3 extensions, and local-first Expo/Flutter mobile apps.
- **Pragmatic Cloud Architecture:** Designing production-grade topologies on AWS (DynamoDB, Step Functions, Bedrock, SNS/SQS, CloudFront), Cloudflare Workers AI, Docker, and Kubernetes/Helm.

---

## Core Technical Stack

| Layer | Technologies |
| :--- | :--- |
| **Languages** | `Go` · `Python` · `TypeScript` · `Java` · `Swift` · `C17` · `SQL` |
| **Backend & Distributed** | `Chi` · `FastAPI` · `Spring Boot` · `NATS JetStream` · `PostgreSQL` (`pgvector`, `PostGIS`, `RLS`) · `Redis` · `SQLite (WAL)` |
| **AI & Agentic Systems** | `LangGraph` · `PyTorch` · `AWS Bedrock` · `Cloudflare Workers AI` · `Ollama` · `RAG / Vector Search` · `Reinforcement Learning` |
| **Frontend & Native** | `React 19` · `Vite` · `Expo / React Native` · `Flutter` · `SwiftUI` · `Chrome Extensions (MV3)` · `Streamlit` |
| **Cloud & Infrastructure** | `AWS` (DynamoDB, Step Functions, SNS/SQS, CloudFront) · `Docker` · `Kubernetes / Helm` · `GitHub Actions` · `Cloudflare` · `Railway` |

---

## Foundations & Practice

- **[LowLevelDesign](https://github.com/sahil0017/LowLevelDesign)** — Object-oriented design patterns and concurrency implementations in Java & Spring Boot
- **[SplitwiseRepo](https://github.com/sahil0017/SplitwiseRepo)** — Expense-sharing & group ledger backend in Java, Spring Boot & Docker Compose
- **[neetcode-submissions](https://github.com/sahil0017/neetcode-submissions)** — Curated algorithmic solutions in Java organized by pattern
- **[DataX](https://github.com/sahil0017/DataX)** — TypeScript + Vite data-driven web workspace
