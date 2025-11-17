# Event Sourcing Infrastructure Modernization - Asana Tasks Reference

**Initiative**: event-sourcing-infrastructure
**Created**: 2025-11-17
**Total Tasks**: 13

All tasks follow the naming convention: `[event-sourcing-infrastructure X.Y] [Task Name]`

**To find all tasks:** Search Asana for `[event-sourcing-infrastructure`

## Tasks by Project

### -MS D Data Pipeline (12 tasks)

| Task | Name | Priority | Est. Hours | Asana URL |
|------|------|----------|------------|-----------|
| 1.1 | UV + pyproject.toml Migration for All Services | High | 4 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969692934742 |
| 1.2 | Terraform Infrastructure Setup | High | 3 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969693075946 |
| 1.3 | Logfire Instrumentation Standards | High | 2 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969693206012 |
| 2.1 | Cloud Tasks Client Library Integration | High | 2 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969783999326 |
| 2.2 | Migrate Scheduling → Sourcing (First Stage) | High | 4 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969784413672 |
| 2.3 | Migrate Doc Processing → Extraction | High | 5 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969909020455 |
| 2.4 | Migrate Entity Resolution → Writers | High | 4 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969784630915 |
| 2.5 | Dead Letter Queue + Failed Tasks Collection | High | 3 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969699403462 |
| 3.1 | Logfire Custom Dashboard Creation | Medium | 2 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969789813766 |
| 3.2 | Alert Configuration | Medium | 1.5 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969704351793 |
| 4.1 | Pydantic-AI Version Update | Medium | 4 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969914846511 |
| 4.2 | Cleanup and Documentation | Medium | 3 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969914980164 |
| 5.1 | Testing Infrastructure Improvements | Low | 5 | https://app.asana.com/1/426521350405896/project/1209042780967623/task/1211969791432790 |

### -MS D Admin Portal (1 task)

| Task | Name | Priority | Est. Hours | Asana URL |
|------|------|----------|------------|-----------|
| 4.3 | Admin UI Failed Tasks Integration (Coordination) | Medium | 2 | https://app.asana.com/1/426521350405896/project/1208833533751404/task/1211969915071952 |

## Tasks by Repository

**mystage-event-sourcing**: Tasks 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 2.5, 4.1, 4.2, 5.1
**mystage-databases**: Task 2.5 (schema for failed_tasks)
**mystage-platform**: Task 4.2 (documentation updates)
**mystage-admin-interface**: Task 4.3
**N/A (Logfire UI)**: Tasks 3.1, 3.2

## Manual Setup Required

Due to MCP integration limitations, manually set these custom fields in Asana:

| Task | Priority | Est. Hours |
|------|----------|------------|
| [event-sourcing-infrastructure 1.1] UV + pyproject.toml Migration | High | 4 |
| [event-sourcing-infrastructure 1.2] Terraform Infrastructure Setup | High | 3 |
| [event-sourcing-infrastructure 1.3] Logfire Instrumentation Standards | High | 2 |
| [event-sourcing-infrastructure 2.1] Cloud Tasks Client Library Integration | High | 2 |
| [event-sourcing-infrastructure 2.2] Migrate Scheduling → Sourcing | High | 4 |
| [event-sourcing-infrastructure 2.3] Migrate Doc Processing → Extraction | High | 5 |
| [event-sourcing-infrastructure 2.4] Migrate Entity Resolution → Writers | High | 4 |
| [event-sourcing-infrastructure 2.5] Dead Letter Queue + Failed Tasks | High | 3 |
| [event-sourcing-infrastructure 3.1] Logfire Custom Dashboard Creation | Medium | 2 |
| [event-sourcing-infrastructure 3.2] Alert Configuration | Medium | 1.5 |
| [event-sourcing-infrastructure 4.1] Pydantic-AI Version Update | Medium | 4 |
| [event-sourcing-infrastructure 4.2] Cleanup and Documentation | Medium | 3 |
| [event-sourcing-infrastructure 4.3] Admin UI Failed Tasks Integration | Medium | 2 |
| [event-sourcing-infrastructure 5.1] Testing Infrastructure Improvements | Low | 5 |

**Total Estimated Hours**: 44.5 hours (~40 hours + buffer)

Values are also documented in each task's description field.

## Task Dependencies

```
Phase 1: Foundation (can start immediately)
├── 1.1 UV Migration (no deps)
├── 1.2 Terraform Setup (parallel with 1.1)
└── 1.3 Logfire Standards (after 1.1 partial)

Phase 2: Cloud Tasks Migration
├── 2.1 Client Library (after 1.2, 1.3)
├── 2.2 Scheduling → Sourcing (after 2.1)
├── 2.3 Doc Processing → Extraction (after 2.2)
├── 2.4 Entity Resolution → Writers (after 2.3)
└── 2.5 DLQ + Failed Tasks (after 1.2, parallel with 2.2-2.4)

Phase 3: Observability
├── 3.1 Dashboards (after 1.3, 2.2-2.4 partial)
└── 3.2 Alerts (after 3.1)

Phase 4: Dependencies & Polish
├── 4.1 Pydantic-AI Update (after 1.1, 2.2-2.4)
├── 4.2 Cleanup & Docs (after 2.1-2.5, 3.1-3.2)
└── 4.3 Admin UI Coordination (after 2.5)

Phase 5: Testing (Nice to Have)
└── 5.1 Testing Infrastructure (after 4.1)
```
