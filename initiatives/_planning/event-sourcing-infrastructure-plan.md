# Initiative Implementation Plan: Event Sourcing Infrastructure Modernization

## Overview

This plan breaks down the comprehensive infrastructure overhaul of the event-sourcing data pipeline into actionable phases and tasks. The initiative modernizes dependency management, implements Infrastructure as Code, migrates from Pub/Sub to Cloud Tasks, enhances observability with Logfire dashboards, and updates core AI dependencies.

**Total Estimated Effort:** 2-4 weeks with 0.5 engineer (~40 hours total)

---

## Dependencies

### Blocking Dependencies
- None (this is foundational infrastructure work)

### Unblocks
- Admin Interface pipeline management tools (can trigger Cloud Tasks directly)
- Future IaC expansion initiatives
- Pipeline reliability improvements

### Coordination Required
- **mystage-admin-interface** - Failed tasks UI and manual task triggering features
- **mystage-databases** - `failed_tasks` collection schema

---

## Phase 1: Foundation & Tooling
**Goal:** Establish modern dependency management and Infrastructure as Code foundation before touching core pipeline logic.

**Duration:** 2-3 weeks

---

### Task 1.1: UV + pyproject.toml Migration for All Services

#### SCOPE OF WORK
Migrate all Python services from `requirements.txt` to `pyproject.toml` with UV for consistent dependency management. This includes configuring UV to use `venv/` directory for Firebase CLI compatibility.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 4

#### EXPECTED OUTPUTS
**Deliverables:**
- `pyproject.toml` file for each service with proper dependencies
- `uv.lock` files committed for reproducible installs
- Updated deployment scripts to use `uv sync --locked`
- Remove old `requirements.txt` files after migration

**Acceptance Criteria:**
- All 10+ services have `pyproject.toml` with `[tool.uv] venv = "venv"` config
- `uv sync --locked` works for all services
- Firebase deploy still works (uses `venv/` directory)
- No dependency resolution conflicts

#### PREREQUISITES
**Dependencies from previous tasks:**
- None (first task)

**Required decisions:**
- Confirm UV version to standardize on
- Confirm Python version requirements per service

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should we standardize Python version across all services (3.12)? Or keep per-service versions?
2. Are there any services with complex native dependencies that might cause issues?

#### IMPLEMENTATION APPROACH
- Research phase: Audit all services for current dependency setup
- Design phase: Create standard `pyproject.toml` template
- Implementation phase:
  - Start with `functions-scheduling` (reference existing `functions-sync-data-stores`)
  - Migrate one service at a time
  - Test Firebase deploy after each service
- Review phase: Verify all services work in local and deployed environments

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] All services have `pyproject.toml` + `uv.lock`
- [ ] `[tool.uv] venv = "venv"` configured in all services
- [ ] Firebase CLI deploys successfully
- [ ] Local development workflow documented
- [ ] Old `requirements.txt` files removed
- [ ] CI/CD uses `uv sync --locked` for installs

#### EFFORT ESTIMATE
- **Size**: M (Medium)
- **Estimated Time**: 1-2 weeks
- **Complexity**: Low (repetitive, clear pattern)
- **Risk**: 🟢 Low

---

### Task 1.2: Terraform Infrastructure Setup

#### SCOPE OF WORK
Set up Terraform with GCS backend for state management. Create initial infrastructure definitions for Cloud Tasks queues and DLQ Pub/Sub topics.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 3

#### EXPECTED OUTPUTS
**Deliverables:**
- `infrastructure/` directory with Terraform configuration
- GCS bucket for Terraform state (manually created or bootstrapped)
- Terraform definitions for Cloud Tasks queues
- Terraform definitions for DLQ Pub/Sub topics
- CI/CD integration script for `terraform apply`

**Acceptance Criteria:**
- `terraform init` succeeds with GCS backend
- `terraform plan` shows expected resources
- `terraform apply` creates queues and topics in GCP
- State is properly stored in GCS bucket
- Can run `terraform apply` multiple times (idempotent)

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 1.1 should be started (can run in parallel, but UV migration establishes patterns)

**Required decisions:**
- GCS bucket name and location for Terraform state
- IAM permissions for Terraform service account
- Naming conventions for queues/topics

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. GCS bucket name for state (e.g., `mystage-terraform-state`)?
2. How many Cloud Tasks queues? One per pipeline stage or service type?
3. Service account for Terraform execution?

#### IMPLEMENTATION APPROACH
- Research phase: Review Terraform GCP provider docs
- Design phase:
  - Define queue naming conventions
  - Define retry policies per queue type
  - Define DLQ topic structure
- Implementation phase:
  - Create GCS bucket for state
  - Initialize Terraform project
  - Define queues and topics
  - Test apply/destroy cycle
- Review phase: Verify resources in GCP Console

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] GCS backend configured and working
- [ ] At least one Cloud Tasks queue defined and created
- [ ] DLQ Pub/Sub topic defined and created
- [ ] Terraform state stored securely in GCS
- [ ] `terraform apply` is idempotent
- [ ] Documentation for adding new infrastructure
- [ ] CI/CD integration tested

#### EFFORT ESTIMATE
- **Size**: M (Medium)
- **Estimated Time**: 1 week
- **Complexity**: Medium (new tooling)
- **Risk**: 🟡 Medium (first time using Terraform)

---

### Task 1.3: Logfire Instrumentation Standards

#### SCOPE OF WORK
Define and document consistent Logfire instrumentation standards for the pipeline. Implement core metrics and span patterns that will be used across all services during the Cloud Tasks migration.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 2

#### EXPECTED OUTPUTS
**Deliverables:**
- Instrumentation standards document (what metrics, what spans)
- Shared utility module for common metrics/spans
- Example implementations in 2-3 services
- Metric naming conventions

**Acceptance Criteria:**
- Documented standards for counters, histograms, spans
- Entity found/created metrics defined
- Pipeline stage success/failure metrics defined
- Trace context propagation pattern documented

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 1.1 (UV migration) should be complete for at least some services

**Required decisions:**
- Metric naming conventions (snake_case, namespacing)
- Which metrics are mandatory vs optional per service
- Span naming conventions

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should we create a shared Python module for common metrics, or just document patterns?
2. Any specific metrics beyond what's in the spec (entity found/created, success/failure rates)?

#### IMPLEMENTATION APPROACH
- Research phase: Review existing Logfire usage in codebase
- Design phase:
  - Define metric taxonomy
  - Define span hierarchy patterns
  - Document trace context propagation
- Implementation phase:
  - Create shared utilities or patterns
  - Implement in scheduling service first
  - Validate metrics appear in Logfire dashboard
- Review phase: Ensure consistency and completeness

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Instrumentation standards documented
- [ ] Entity metrics defined (venues/artists/performances found/created)
- [ ] Success/failure rate metrics defined
- [ ] Latency histogram patterns defined
- [ ] Trace context propagation pattern documented
- [ ] Example implementation in at least one service
- [ ] Metrics visible in Logfire

#### EFFORT ESTIMATE
- **Size**: S (Small)
- **Estimated Time**: 3-4 days
- **Complexity**: Low
- **Risk**: 🟢 Low

---

## Phase 2: Cloud Tasks Migration
**Goal:** Gradually migrate pipeline from Pub/Sub to Cloud Tasks, stage by stage, with proper observability.

**Duration:** 3-4 weeks

---

### Task 2.1: Cloud Tasks Client Library Integration

#### SCOPE OF WORK
Create shared Cloud Tasks client utilities that will be used across all services. This includes the core `create_cloud_task()` function with support for delayed execution, context propagation, and proper error handling.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 2

#### EXPECTED OUTPUTS
**Deliverables:**
- Shared Cloud Tasks client module in `mystage-core` package
- `create_cloud_task()` function with delay support
- Authentication and configuration patterns
- Unit tests for client utilities

**Acceptance Criteria:**
- Can create Cloud Tasks programmatically
- Supports optional delay_seconds parameter
- Includes trace context in payload
- Proper error handling and logging
- Works in both local and deployed environments

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 1.2 (Terraform setup) complete - queues exist
- Task 1.3 (Logfire standards) complete - know how to instrument

**Required decisions:**
- Queue naming conventions (how to determine which queue)
- Authentication method (service account, default credentials)

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should Cloud Tasks client be part of `mystage-core` package?
2. How should functions discover their HTTP endpoints (environment variables)?

#### IMPLEMENTATION APPROACH
- Research phase: Review Google Cloud Tasks Python client docs
- Design phase:
  - Define function signature and parameters
  - Plan configuration management
  - Design error handling strategy
- Implementation phase:
  - Add `google-cloud-tasks` to dependencies
  - Implement core utility functions
  - Write unit tests
  - Test in local environment
- Review phase: Code review and integration testing

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] `google-cloud-tasks` added to relevant service dependencies
- [ ] `create_cloud_task()` function implemented
- [ ] Delay scheduling works correctly
- [ ] Context propagation included
- [ ] Unit tests passing
- [ ] Can successfully create tasks in test queue

#### EFFORT ESTIMATE
- **Size**: S (Small)
- **Estimated Time**: 3-4 days
- **Complexity**: Medium
- **Risk**: 🟢 Low

---

### Task 2.2: Migrate Scheduling → Sourcing (First Stage)

#### SCOPE OF WORK
Migrate the first pipeline stage: scheduler functions that trigger sourcing functions. Replace `pubsub.publish_datas()` with `create_cloud_task()`. This is the first real migration and establishes patterns for subsequent stages.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 4

#### EXPECTED OUTPUTS
**Deliverables:**
- Updated `task_scheduler.py` using Cloud Tasks instead of Pub/Sub
- Updated `url_scrape_scheduler.py` using Cloud Tasks
- Staggered execution implementation (spacing out tasks)
- Updated Logfire instrumentation with new metrics
- Sourcing functions updated to accept HTTP requests (not just Pub/Sub)

**Acceptance Criteria:**
- Scheduler creates Cloud Tasks instead of publishing to Pub/Sub
- Tasks are staggered (not all executed at once)
- Sourcing functions receive and process HTTP requests
- Trace context propagates from scheduler to sourcing
- Metrics tracked for tasks scheduled

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 2.1 (Cloud Tasks client) complete
- Sourcing functions need to be converted to HTTP endpoints (if not already)

**Required decisions:**
- Stagger timing (how many seconds between tasks)
- Which queue to use for sourcing tasks
- How to handle existing Pub/Sub subscriptions during transition

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Can we run both Pub/Sub and Cloud Tasks paths simultaneously during testing?
2. What's the stagger interval (30 seconds? 60 seconds?)?
3. Should sourcing functions be HTTP-triggered Cloud Functions or Cloud Run?

#### IMPLEMENTATION APPROACH
- Research phase: Review current scheduler and sourcing code
- Design phase:
  - Map Pub/Sub topics to Cloud Task queues
  - Plan gradual cutover strategy
  - Design HTTP endpoint structure
- Implementation phase:
  - Update scheduler to use Cloud Tasks
  - Update sourcing functions to handle HTTP
  - Add Logfire instrumentation
  - Test end-to-end flow
- Review phase: Validate in staging environment

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Schedulers create Cloud Tasks (not Pub/Sub)
- [ ] Staggered execution working (configurable delay)
- [ ] Sourcing functions accept HTTP requests
- [ ] Trace context propagates through
- [ ] Metrics visible in Logfire
- [ ] No data loss during migration
- [ ] Can fallback to Pub/Sub if needed

#### EFFORT ESTIMATE
- **Size**: L (Large)
- **Estimated Time**: 1 week
- **Complexity**: High (first migration, establishes patterns)
- **Risk**: 🟡 Medium

---

### Task 2.3: Migrate Doc Processing → Extraction

#### SCOPE OF WORK
Replace Firestore document triggers with explicit Cloud Task creation. When scrapes/extractions are written, the writer explicitly creates the Cloud Task for the next stage instead of relying on automatic triggers.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 5

#### EXPECTED OUTPUTS
**Deliverables:**
- Remove `dpl_on_scrapes_written` Firestore trigger
- Remove `dpl_on_extractions_written` Firestore trigger
- Update sourcing functions to create extraction tasks after writing scrapes
- Update extraction functions to create resolution tasks after writing extractions
- Logfire instrumentation for all transitions

**Acceptance Criteria:**
- No Firestore triggers remain for pipeline flow
- Writers explicitly create next-stage tasks
- Status-only updates don't create spurious tasks
- All transitions instrumented and traceable
- Admin can manually trigger any stage via API

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 2.2 (Scheduling → Sourcing) complete
- Pattern established for Cloud Tasks creation

**Required decisions:**
- Which writes should trigger next stage vs which are status-only
- Error handling when task creation fails after document write

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should document write and task creation be in a transaction (all or nothing)?
2. What happens if write succeeds but task creation fails?
3. Are there any status-update-only writes we need to identify?

#### IMPLEMENTATION APPROACH
- Research phase: Identify all Firestore triggers and their behavior
- Design phase:
  - Map document writes to next-stage triggers
  - Identify status-only updates
  - Plan transaction handling
- Implementation phase:
  - Update each writer to create Cloud Task
  - Remove Firestore trigger functions
  - Add comprehensive logging
  - Test each pathway
- Review phase: Verify no data gets stuck

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] All Firestore triggers removed from pipeline flow
- [ ] Scrape writes → extraction task created
- [ ] Extraction writes → resolution task created
- [ ] Status updates don't trigger unnecessary tasks
- [ ] All transitions logged and traceable
- [ ] No documents stuck without next-stage processing

#### EFFORT ESTIMATE
- **Size**: L (Large)
- **Estimated Time**: 1-1.5 weeks
- **Complexity**: High (many touchpoints)
- **Risk**: 🟡 Medium

---

### Task 2.4: Migrate Entity Resolution → Writers

#### SCOPE OF WORK
Continue Cloud Tasks migration through entity resolution, source management, and entity writers. Each stage creates Cloud Tasks for the next stage.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: High

**Estimated Hours**: 4

#### EXPECTED OUTPUTS
**Deliverables:**
- Entity resolution creates source management tasks
- Source management creates entity writer tasks
- Entity writers create sync tasks
- All Pub/Sub publishing removed from these stages
- Complete trace through entire pipeline

**Acceptance Criteria:**
- End-to-end pipeline works with Cloud Tasks only
- No Pub/Sub topics used (except DLQ)
- Consistent instrumentation across all stages
- Can trace single URL from scrape to final entity

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 2.3 (Doc Processing → Extraction) complete
- All stages downstream should be HTTP-capable

**Required decisions:**
- Queue assignments for each stage
- Retry policies per stage (different complexity levels)

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should entity writers have different retry policies than extraction?
2. Any specific rate limiting needs for different stages?

#### IMPLEMENTATION APPROACH
- Research phase: Map remaining Pub/Sub usage
- Design phase:
  - Assign queues per stage
  - Configure retry policies
  - Plan migration order
- Implementation phase:
  - Entity resolution updates
  - Source management updates
  - Entity writer updates
  - Sync updates
  - End-to-end testing
- Review phase: Full pipeline trace validation

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] All pipeline stages use Cloud Tasks
- [ ] No Pub/Sub topics used (except DLQ)
- [ ] Complete trace visible in Logfire
- [ ] Entity found/created metrics tracked
- [ ] Pipeline throughput maintained or improved
- [ ] Error rates stable or improved

#### EFFORT ESTIMATE
- **Size**: L (Large)
- **Estimated Time**: 1 week
- **Complexity**: Medium (pattern established)
- **Risk**: 🟡 Medium

---

### Task 2.5: Dead Letter Queue + Failed Tasks Collection

#### SCOPE OF WORK
Implement DLQ handling: when Cloud Tasks exhaust retries, they publish to DLQ Pub/Sub topic. A handler function writes to `failed_tasks` Firestore collection for admin visibility and retry capability.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing (handler function), mystage-databases (schema)

**Priority**: High

**Estimated Hours**: 3

#### EXPECTED OUTPUTS
**Deliverables:**
- DLQ handler Cloud Function
- `failed_tasks` collection schema in Firestore
- Logging and alerting on DLQ events
- Documentation for retry process
- Firestore indexes for filtering

**Acceptance Criteria:**
- Failed tasks are captured in Firestore
- All required metadata preserved (function, payload, error)
- Can filter by stage, type, date range
- Alert sent to Slack on DLQ events
- Admin can query failed tasks

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 1.2 (Terraform setup) - DLQ topics created
- Task 2.2-2.4 (Cloud Tasks migration) - at least partially complete to test

**Required decisions:**
- Firestore indexes for `failed_tasks` queries
- Alert thresholds (how many failures trigger alert)

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should we auto-retry failed tasks after N hours, or only manual retry?
2. How long to keep failed tasks in collection (retention policy)?
3. Who should receive Slack alerts?

#### IMPLEMENTATION APPROACH
- Research phase: Review Cloud Tasks DLQ configuration
- Design phase:
  - Define failed_tasks schema
  - Plan Slack integration
  - Design retry workflow
- Implementation phase:
  - Configure Cloud Tasks DLQ in Terraform
  - Create DLQ handler function
  - Set up Slack webhook
  - Create Firestore indexes
  - Test failure scenarios
- Review phase: Verify complete failure capture

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Cloud Tasks configured with DLQ
- [ ] DLQ handler writes to `failed_tasks`
- [ ] All failure metadata captured
- [ ] Slack alert on DLQ events
- [ ] Firestore indexes allow efficient querying
- [ ] Can manually create retry task from failed_tasks doc

#### EFFORT ESTIMATE
- **Size**: M (Medium)
- **Estimated Time**: 3-4 days
- **Complexity**: Medium
- **Risk**: 🟢 Low

---

## Phase 3: Observability & Monitoring
**Goal:** Build comprehensive dashboard and alerting for pipeline health visibility.

**Duration:** 1-2 weeks

---

### Task 3.1: Logfire Custom Dashboard Creation

#### SCOPE OF WORK
Create custom Logfire dashboards with SQL queries for pipeline funnel views, entity creation rates, failure rates, and latency tracking.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: N/A (Logfire web UI configuration)

**Priority**: Medium

**Estimated Hours**: 2

#### EXPECTED OUTPUTS
**Deliverables:**
- Pipeline funnel dashboard (scrapes → extractions → entities)
- Entity creation rates dashboard (found vs created)
- Failure rates by service dashboard
- Latency tracking dashboard
- SQL queries documented for each panel

**Acceptance Criteria:**
- Can see pipeline throughput at a glance
- Can identify bottlenecks or failures quickly
- Historical trends visible
- Conversion rates calculated (scrapes to entities)
- Dashboards accessible to team

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 1.3 (Logfire instrumentation standards) complete
- Task 2.2-2.4 (Cloud Tasks migration) generating consistent metrics

**Required decisions:**
- Dashboard organization (one dashboard vs multiple)
- Time ranges and resolutions
- Team access permissions

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should dashboards be shared across team or individual?
2. Any specific KPIs beyond funnel/entities/failures?
3. Preferred time ranges (last hour, 24h, 7d)?

#### IMPLEMENTATION APPROACH
- Research phase: Review Logfire dashboard SQL syntax
- Design phase:
  - Sketch dashboard layouts
  - Write SQL queries
  - Define panel types (time series, bar charts, tables)
- Implementation phase:
  - Create dashboards in Logfire UI
  - Configure panels with SQL queries
  - Set up variables ($resolution, etc.)
  - Share with team
- Review phase: Get feedback and refine

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Funnel view showing scrapes → extractions → resolutions
- [ ] Entity creation metrics (found vs created per type)
- [ ] Failure rate trends visible
- [ ] Processing latency tracked
- [ ] Dashboards shared with team
- [ ] SQL queries documented

#### EFFORT ESTIMATE
- **Size**: S (Small)
- **Estimated Time**: 3-4 days
- **Complexity**: Medium
- **Risk**: 🟢 Low

---

### Task 3.2: Alert Configuration

#### SCOPE OF WORK
Configure Logfire alerts for critical pipeline conditions: high error rates, pipeline stalls, DLQ spikes. Set up Slack webhook notifications.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: N/A (Logfire web UI configuration)

**Priority**: Medium

**Estimated Hours**: 1.5

#### EXPECTED OUTPUTS
**Deliverables:**
- High error rate alert
- Pipeline stall detection alert
- DLQ spike alert
- Slack webhook integration
- Alert documentation (what each alert means, how to respond)

**Acceptance Criteria:**
- Alerts trigger on defined conditions
- Slack notifications received promptly
- Alert messages contain useful context
- Can enable/disable alerts as needed
- No alert fatigue (thresholds tuned properly)

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 3.1 (Dashboard creation) complete
- Metrics being consistently generated

**Required decisions:**
- Alert thresholds (what's "high" error rate)
- Time windows (5 min? 15 min?)
- Slack channel for alerts

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. What Slack channel should receive alerts?
2. What's acceptable error rate threshold (1%? 5%? 10%)?
3. What hours should pipeline stall detection be active?

#### IMPLEMENTATION APPROACH
- Research phase: Review Logfire alerting docs
- Design phase:
  - Define alert conditions with SQL
  - Set appropriate thresholds
  - Design alert messages
- Implementation phase:
  - Configure Slack webhook in Logfire
  - Create each alert with SQL condition
  - Test alert triggering
  - Tune thresholds based on baseline
- Review phase: Monitor for false positives/negatives

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] High error rate alert configured and tested
- [ ] Pipeline stall alert configured and tested
- [ ] DLQ spike alert configured and tested
- [ ] Slack notifications working
- [ ] Alert thresholds tuned to avoid noise
- [ ] Runbook for each alert type documented

#### EFFORT ESTIMATE
- **Size**: S (Small)
- **Estimated Time**: 2-3 days
- **Complexity**: Low
- **Risk**: 🟢 Low

---

## Phase 4: Dependency Updates & Polish
**Goal:** Update core AI dependencies and finalize any remaining work.

**Duration:** 2-3 weeks

---

### Task 4.1: Pydantic-AI Version Update

#### SCOPE OF WORK
Upgrade Pydantic-AI from pre-v1 to latest stable version (1.18.0+). Fix any breaking API changes and monitor for reduction in persistent AI integration errors.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing (all services using pydantic-ai)

**Priority**: Medium

**Estimated Hours**: 4

#### EXPECTED OUTPUTS
**Deliverables:**
- Updated `pyproject.toml` with latest pydantic-ai version
- Fixed any breaking API changes
- Updated related dependencies
- Test coverage for AI extraction functions
- Documentation of changes made

**Acceptance Criteria:**
- All services using latest pydantic-ai
- No regressions in extraction functionality
- AI integration errors reduced (monitored in Logfire)
- All tests passing
- Performance maintained or improved

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 1.1 (UV migration) complete
- Task 2.2-2.4 (Cloud Tasks migration) complete (stable baseline)

**Required decisions:**
- Exact version to target (latest stable at implementation time)
- Testing strategy (unit tests, integration tests, manual testing)

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Should we update all AI-using services simultaneously or one at a time?
2. What specific AI integration errors are we hoping to resolve?
3. Any features in newer pydantic-ai we want to adopt?

#### IMPLEMENTATION APPROACH
- Research phase:
  - Review pydantic-ai changelog (v1 breaking changes)
  - Audit current pydantic-ai usage patterns
- Design phase:
  - Plan migration path
  - Identify breaking changes that affect our code
- Implementation phase:
  - Update dependency version
  - Fix compile/import errors
  - Fix runtime errors
  - Update tests
  - Monitor error rates
- Review phase: Compare error rates before/after

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Latest stable pydantic-ai in all relevant services
- [ ] All breaking changes resolved
- [ ] Tests passing
- [ ] AI extraction agents functional
- [ ] Error rates monitored (expecting improvement)
- [ ] No regressions in functionality
- [ ] Changes documented

#### EFFORT ESTIMATE
- **Size**: M (Medium)
- **Estimated Time**: 1-1.5 weeks
- **Complexity**: Medium (potential breaking changes)
- **Risk**: 🟡 Medium

---

### Task 4.2: Cleanup and Documentation

#### SCOPE OF WORK
Remove deprecated Pub/Sub infrastructure, update all documentation, clean up unused code, and ensure knowledge transfer.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing, mystage-platform (docs)

**Priority**: Medium

**Estimated Hours**: 3

#### EXPECTED OUTPUTS
**Deliverables:**
- Removed old Pub/Sub topic subscriptions
- Updated architecture diagrams
- Updated `pipeline.md` documentation
- README updates for new deployment process
- Knowledge transfer documentation

**Acceptance Criteria:**
- No orphaned Pub/Sub resources
- All documentation reflects current state
- Deployment process fully documented
- Team understands new architecture
- No deprecated code remaining

#### PREREQUISITES
**Dependencies from previous tasks:**
- All migration tasks complete (2.1-2.5)
- All monitoring tasks complete (3.1-3.2)

**Required decisions:**
- Retention period for old infrastructure (how long to keep as fallback)
- Documentation format and location

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. How long should we keep old Pub/Sub infrastructure before deletion?
2. Should we update the pipeline.md mermaid diagrams?
3. Any specific knowledge transfer sessions needed?

#### IMPLEMENTATION APPROACH
- Research phase: Audit all deprecated resources
- Design phase: Plan cleanup order
- Implementation phase:
  - Remove Pub/Sub subscriptions (after confidence period)
  - Update architecture documentation
  - Update deployment guides
  - Create knowledge transfer docs
- Review phase: Final team review

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Old Pub/Sub infrastructure removed (after grace period)
- [ ] `pipeline.md` updated with Cloud Tasks architecture
- [ ] README and deployment docs current
- [ ] Architecture diagrams reflect new state
- [ ] Knowledge transfer completed
- [ ] No deprecated code in codebase

#### EFFORT ESTIMATE
- **Size**: M (Medium)
- **Estimated Time**: 3-4 days
- **Complexity**: Low
- **Risk**: 🟢 Low

---

### Task 4.3: Admin UI Failed Tasks Integration (Coordination)

#### SCOPE OF WORK
Coordinate with Admin Interface team to implement failed tasks UI. This task tracks the coordination, not the implementation (which happens in mystage-admin-interface).

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Admin Portal

**Repository**: mystage-admin-interface

**Priority**: Medium

**Estimated Hours**: 2 (coordination and spec review)

#### EXPECTED OUTPUTS
**Deliverables:**
- Failed tasks UI requirements spec
- API contract for failed_tasks queries
- Retry functionality specification
- Coordination meetings completed

**Acceptance Criteria:**
- Admin UI can query failed_tasks collection
- Admin can filter by stage, type, date range
- Admin can retry individual or bulk tasks
- Admin can mark tasks as resolved
- UI is intuitive and useful

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 2.5 (DLQ + Failed Tasks) complete
- `failed_tasks` schema finalized

**Required decisions:**
- Admin UI framework/approach
- Permissions model (who can retry tasks)

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. Is failed tasks UI part of this initiative or separate?
2. Who owns the admin-interface implementation?
3. Any specific UI/UX requirements?

#### IMPLEMENTATION APPROACH
- Research phase: Review failed_tasks schema
- Design phase: Spec out UI requirements and API
- Implementation phase: (In admin-interface repo)
- Review phase: Validate integration works

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] Requirements clearly specified
- [ ] API contract defined
- [ ] Admin interface team understands requirements
- [ ] Integration tested end-to-end
- [ ] Documentation complete

#### EFFORT ESTIMATE
- **Size**: S (Small) for coordination
- **Estimated Time**: 2-3 days coordination
- **Complexity**: Low (coordination, not implementation)
- **Risk**: 🟢 Low

---

## Phase 5: Validation & Testing (Nice to Have)
**Goal:** Improve testing infrastructure, especially for AI extraction agents.

**Duration:** 1-2 weeks (if time permits)

---

### Task 5.1: Testing Infrastructure Improvements

#### SCOPE OF WORK
Finish pydantic/deep evals setup, get all evaluations working fully, improve test coverage for AI extraction agents.

#### PROJECT/REPOSITORY
**Primary Project**: -MS D Data Pipeline

**Repository**: mystage-event-sourcing

**Priority**: Low

**Estimated Hours**: 5

#### EXPECTED OUTPUTS
**Deliverables:**
- Working eval framework for AI agents
- Comprehensive test coverage for extraction agents
- CI/CD integration for evals
- Baseline performance metrics

**Acceptance Criteria:**
- All evals run successfully
- Can track extraction quality over time
- Tests catch regressions
- Coverage metrics improved

#### PREREQUISITES
**Dependencies from previous tasks:**
- Task 4.1 (Pydantic-AI update) complete
- Stable pipeline infrastructure

**Required decisions:**
- Eval framework to use
- Test data sources
- Quality thresholds

#### CLARIFICATION NEEDED
Before proceeding with this task, please confirm:
1. What specific evals are currently failing?
2. What's the target test coverage percentage?
3. Should this run on every PR or scheduled?

#### IMPLEMENTATION APPROACH
- Research phase: Audit current test infrastructure
- Design phase: Plan eval framework
- Implementation phase:
  - Fix existing evals
  - Add new test cases
  - Integrate with CI
  - Establish baselines
- Review phase: Validate coverage

#### ACCEPTANCE CRITERIA
This task is complete when:
- [ ] All evals passing
- [ ] Extraction agent coverage improved
- [ ] CI integration working
- [ ] Performance baselines established
- [ ] Documentation updated

#### EFFORT ESTIMATE
- **Size**: L (Large)
- **Estimated Time**: 1-2 weeks
- **Complexity**: High
- **Risk**: 🟡 Medium

---

## Risk Mitigation

### Primary Risks and Mitigations

1. **Cloud Tasks Migration Complexity**
   - **Mitigation:** Gradual migration, one stage at a time
   - **Contingency:** Both Pub/Sub and Cloud Tasks coexist during transition
   - **Monitoring:** Logfire dashboards track success rates

2. **Pydantic-AI Breaking Changes**
   - **Mitigation:** Thorough review of changelog, comprehensive testing
   - **Contingency:** Pin to specific version, incremental fixes
   - **Monitoring:** AI error rates tracked pre/post update

3. **Data Loss During Migration**
   - **Mitigation:** DLQ captures all failures, no data lost
   - **Contingency:** Manual retry from failed_tasks collection
   - **Monitoring:** Pipeline completion rates tracked

4. **Performance Regression**
   - **Mitigation:** Latency metrics tracked throughout
   - **Contingency:** Cloud Tasks queue rate limiting adjustable
   - **Monitoring:** Processing duration histograms

---

## Success Metrics

### Quantitative Metrics
- **Pipeline completion rate:** % of scrapes that become entities (target: >95%)
- **Error detection time:** Time from failure to alert (target: <5 minutes)
- **Failed task visibility:** 100% of failures captured and queryable
- **Deployment reproducibility:** All services use uv.lock (target: 100%)
- **Infrastructure as Code:** All queues/topics managed by Terraform

### Qualitative Metrics
- Team confidence in pipeline reliability improved
- Debugging and root cause analysis faster
- New service deployment simpler with established patterns
- Clear visibility into pipeline health at any time

---

## Summary Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| Phase 1: Foundation | 2-3 weeks | UV migration, Terraform, Logfire standards |
| Phase 2: Cloud Tasks | 3-4 weeks | Full Pub/Sub migration, DLQ setup |
| Phase 3: Observability | 1-2 weeks | Dashboards, alerts |
| Phase 4: Dependencies | 2-3 weeks | Pydantic-AI update, cleanup, docs |
| Phase 5: Testing (optional) | 1-2 weeks | Eval improvements |

**Total: 8-12 weeks** (with Phase 5 optional based on time)

---

## Next Steps After Plan Approval

1. Get stakeholder review and approval
2. Merge initiative PR to main
3. Run `/initiative-create-tasks` to generate Asana tasks
4. Begin Phase 1 implementation
5. Track progress in Asana with initiative tag
