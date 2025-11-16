# Event Sourcing Infrastructure Modernization

## Status
🟡 Planning - Technical Architecture Complete

## Description

Major infrastructure overhaul of the event-sourcing data pipeline to improve reliability, scalability, maintainability, and observability. This initiative modernizes the entire pipeline from dependency management through task orchestration to monitoring.

## Business Context

### Problem Statement
Current pipeline infrastructure has reliability gaps, inconsistent tooling, and limited observability making it difficult to ensure data flows correctly through all stages and to diagnose issues when they occur.

### Success Metrics
- Pipeline completion rate visibility (% of scrapes that become entities)
- Error detection within minutes (not hours/days)
- Ability to retry failed tasks from admin UI
- Consistent dependency management across all services
- Reproducible deployments with Infrastructure as Code

## Scope

### In Scope (Critical)
1. **UV + pyproject.toml Migration** - Modernize Python dependency management
2. **Terraform Setup** - Infrastructure as Code foundation
3. **Pub/Sub → Cloud Tasks Migration** - All pipeline stages
4. **Firestore Triggers → Explicit Task Creation** - Writer controls next stage
5. **Dead Letter Queue + Failed Tasks Collection** - Universal error observability
6. **Logfire Dashboard** - Metrics, spans, alerts, funnel views
7. **Pydantic-AI Update** - Upgrade to latest stable version

### Nice to Have
8. **Testing Infrastructure** - Improve pydantic/deep evals (after Pydantic-AI update)

### Out of Scope (Separate Initiatives)
- Admin Directory → Cloud Functions
- BigQuery IaC setup
- VM/Docker deployment for Facebook scraper
- Full platform-wide IaC adoption

## Affected Repositories

- **mystage-event-sourcing** (primary) - All pipeline services
- **mystage-admin-interface** (secondary) - Failed tasks UI, manual task triggering
- **mystage-databases** (minor) - `failed_tasks` collection schema

---

## Technical Architecture

**Added**: Technical Brainstorming Phase

### Implementation Sequence

1. UV + pyproject.toml migration (all services)
2. Terraform setup (GCS backend, queues, topics)
3. Logfire instrumentation improvements
4. Cloud Tasks migration (stage by stage, in pipeline order)
5. Pydantic-AI update
6. Testing infrastructure (nice to have)

---

### Component 1: UV + pyproject.toml Migration

**Current State:**
- Most services use `requirements.txt`
- Each service has own `venv/` directory
- `functions-sync-data-stores` already uses UV + pyproject.toml

**Target State:**
- All services use `pyproject.toml` + `uv.lock`
- Consistent dependency management
- Reproducible installs with `uv sync --locked`

**Technical Consideration - Firebase CLI Compatibility:**

Firebase CLI expects `venv/` directory (not `.venv/`). Configure UV:

```toml
# pyproject.toml
[tool.uv]
venv = "venv"
```

**Services to Migrate:**
- functions-scheduling
- functions-sourcing
- functions-scrapestorm
- functions-doc-processors
- functions-extraction-adapters
- functions-extraction-agents
- functions-entity-resolution
- functions-entity-source-mgmt
- functions-entity-writers
- functions-img-processing
- (any others not yet using UV)

---

### Component 2: Terraform Infrastructure as Code

**Purpose:** Provision and manage GCP resources (Cloud Tasks queues, Pub/Sub topics) declaratively.

**Setup:**

1. **GCS Backend for State** (proper state management)
```hcl
terraform {
  backend "gcs" {
    bucket = "mystage-terraform-state"
    prefix = "event-sourcing"
  }
}

provider "google" {
  project = "mystage-project-id"
  region  = "us-central1"
}
```

2. **Cloud Tasks Queues** (one per pipeline stage or service type)
```hcl
resource "google_cloud_tasks_queue" "sourcing_queue" {
  name     = "sourcing-queue"
  location = "us-central1"

  retry_config {
    max_attempts       = 5
    min_backoff        = "10s"
    max_backoff        = "300s"
    max_doublings      = 3
  }

  rate_limits {
    max_concurrent_dispatches = 10
    max_dispatches_per_second = 5
  }
}
```

3. **Dead Letter Queue Topics**
```hcl
resource "google_pubsub_topic" "failed_tasks_dlq" {
  name = "failed-tasks-dlq"
}

resource "google_pubsub_subscription" "failed_tasks_sub" {
  name  = "failed-tasks-subscription"
  topic = google_pubsub_topic.failed_tasks_dlq.name
}
```

**CI/CD Integration:**
```bash
cd infrastructure
terraform init
terraform apply -auto-approve
```

---

### Component 3: Pub/Sub → Cloud Tasks Migration

**Migration Strategy:** Gradual, stage-by-stage migration. Pub/Sub and Cloud Tasks coexist during transition.

**Migration Order** (following pipeline flow):
1. Scheduling → Sourcing
2. Sourcing → Doc Processing (via Firestore write)
3. Doc Processing → Extraction
4. Extraction → Entity Resolution
5. Entity Resolution → Entity Source Management
6. Entity Source Management → Entity Writers
7. Entity Writers → Sync Data Stores

**Code Pattern - Before (Pub/Sub):**
```python
from mystage_core import pubsub

# Current: publish to Pub/Sub topic
pubsub.publish_datas("scraper_topic", {
    "url_id": url_id,
    "url_data": url_data
})
```

**Code Pattern - After (Cloud Tasks):**
```python
from google.cloud import tasks_v2
from datetime import timedelta

def create_cloud_task(queue_name: str, url: str, payload: dict, delay_seconds: int = 0):
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT_ID, LOCATION, queue_name)

    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(payload).encode(),
        }
    }

    if delay_seconds > 0:
        task["schedule_time"] = timestamp_pb2.Timestamp(
            seconds=int(time.time()) + delay_seconds
        )

    return client.create_task(request={"parent": parent, "task": task})

# New: create Cloud Task with optional delay
create_cloud_task(
    queue_name="sourcing-queue",
    url=f"https://{REGION}-{PROJECT_ID}.cloudfunctions.net/dpl_source_bit_listings",
    payload={"url_id": url_id, "url_data": url_data, "ctx": logfire.get_context()},
    delay_seconds=60  # stagger execution
)
```

**Staggered Execution Example** (scheduler):
```python
# Grab 5 tasks, space them out
delay = 0
for task in tasks:
    create_cloud_task(
        queue_name="pipeline-queue",
        url=task["function_url"],
        payload=task["payload"],
        delay_seconds=delay
    )
    delay += 60  # 1 minute apart
```

---

### Component 4: Firestore Triggers → Explicit Task Creation

**Current State:**
- Firestore triggers fire on document writes
- Some writes should trigger next stage, some shouldn't (status updates)
- Wasted function invocations

**Target State:**
- Writer explicitly creates Cloud Task for next stage
- No automatic triggers
- Admin UI can manually create tasks for any document

**Code Pattern - Before (Firestore Trigger):**
```python
@on_document_created("scrapes/{scrapeId}")
def dpl_on_scrapes_written(event):
    # Triggers on ALL writes, even status updates
    scrape_data = event.data.to_dict()
    # Route to extraction...
```

**Code Pattern - After (Explicit Task):**
```python
def write_scrape_and_trigger_extraction(scrape_data: dict):
    # Write document
    doc_ref = db.collection("scrapes").add(scrape_data)
    scrape_id = doc_ref.id

    # Explicitly trigger next stage
    create_cloud_task(
        queue_name="extraction-queue",
        url=f"https://{REGION}-{PROJECT_ID}.cloudfunctions.net/dpl_extraction_agent",
        payload={
            "scrape_id": scrape_id,
            "ctx": logfire.get_context()
        }
    )
```

**Benefits:**
- No wasted invocations on status updates
- Writer controls flow
- Admin UI can trigger any stage manually by creating Cloud Task

---

### Component 5: Dead Letter Queue + Failed Tasks Collection

**Architecture:**

1. **Cloud Tasks exhaust retries** → publish to DLQ Pub/Sub topic
2. **Cloud Function on DLQ topic** → writes to `failed_tasks` Firestore collection
3. **Admin UI** → displays failed tasks, allows retry

**Failed Tasks Collection Schema:**
```typescript
// failed_tasks document
{
  id: string,                    // auto-generated

  // What failed
  function_name: string,         // "dpl_extraction_agent"
  function_url: string,          // full URL for retry
  payload: object,               // original task payload

  // Failure context
  error_message: string,         // from DLQ metadata
  retry_count: number,           // attempts before failure
  first_failed_at: Timestamp,
  last_failed_at: Timestamp,

  // For filtering/grouping
  pipeline_stage: string,        // "sourcing", "extraction", "entity_resolution", etc.
  task_type: string,             // more specific: "bit_event_extraction"

  // Status
  status: "failed" | "retrying" | "resolved",
  resolved_at?: Timestamp,
  resolved_by?: string           // admin user who retried
}
```

**DLQ Handler Function:**
```python
@pubsub_fn.on_message_published(topic="failed-tasks-dlq")
def handle_failed_task(event):
    message = event.data.message

    # Extract task info from DLQ message
    task_payload = json.loads(base64.b64decode(message.data))
    attributes = message.attributes

    # Write to failed_tasks collection
    db.collection("failed_tasks").add({
        "function_name": attributes.get("function_name"),
        "function_url": attributes.get("function_url"),
        "payload": task_payload,
        "error_message": attributes.get("error_message", "Unknown"),
        "retry_count": int(attributes.get("retry_count", 0)),
        "first_failed_at": firestore.SERVER_TIMESTAMP,
        "last_failed_at": firestore.SERVER_TIMESTAMP,
        "pipeline_stage": attributes.get("pipeline_stage"),
        "task_type": attributes.get("task_type"),
        "status": "failed"
    })

    # Alert to Slack/Logfire
    logfire.error("Task failed permanently",
                  function=attributes.get("function_name"),
                  task_type=attributes.get("task_type"))
```

**Admin UI Features:**
- View all failed tasks
- Filter by: stage, function, task type, date range, error type
- Bulk retry selected tasks
- One-click retry (creates new Cloud Task with stored payload)
- Mark as resolved

---

### Component 6: Logfire Dashboard & Observability

**Goals:**
- Detect items failing to complete pipeline
- Detect service errors
- Funnel view: scrapes → extractions → entities
- Baseline visibility for "normal" vs "something's wrong"
- Root cause analysis via trace correlation

#### 6.1 Consistent Metrics Across Pipeline

**Entity Tracking:**
```python
# In entity resolution/writers
venues_found = logfire.metric_counter("venues_found")      # matched existing
venues_created = logfire.metric_counter("venues_created")  # new entity
artists_found = logfire.metric_counter("artists_found")
artists_created = logfire.metric_counter("artists_created")
performances_found = logfire.metric_counter("performances_found")
performances_created = logfire.metric_counter("performances_created")
```

**Pipeline Stage Metrics:**
```python
# In each service
scrapes_created = logfire.metric_counter("scrapes_created")
extractions_created = logfire.metric_counter("extractions_created")
entities_resolved = logfire.metric_counter("entities_resolved")

# Success/failure rates
task_succeeded = logfire.metric_counter("task_succeeded", attributes={"service": SERVICE_NAME})
task_failed = logfire.metric_counter("task_failed", attributes={"service": SERVICE_NAME})
```

**Latency Tracking:**
```python
processing_duration = logfire.metric_histogram(
    "processing_duration_ms",
    unit="ms",
    description="Time to process task"
)

with logfire.span("process_scrape") as span:
    start = time.time()
    # ... processing ...
    processing_duration.record((time.time() - start) * 1000)
```

#### 6.2 Trace Correlation

Context propagates through entire pipeline (already partially implemented):

```python
# In Cloud Task payload
payload = {
    "scrape_id": scrape_id,
    "ctx": logfire.get_context()  # trace context
}

# In receiving function
def handle_task(request):
    data = request.get_json()

    with logfire.attach_context(data["ctx"]):
        with logfire.span("extraction_agent"):
            # All work here shares same trace_id
            # Can track single item through entire pipeline
```

#### 6.3 Custom Dashboards (SQL Queries)

**Funnel View:**
```sql
SELECT
    time_bucket($resolution, start_timestamp) AS x,
    sum(CASE WHEN service_name = 'sourcing' THEN 1 ELSE 0 END) as scrapes,
    sum(CASE WHEN service_name = 'extraction' THEN 1 ELSE 0 END) as extractions,
    sum(CASE WHEN service_name = 'entity-resolution' THEN 1 ELSE 0 END) as resolutions
FROM records
WHERE start_timestamp >= now() - interval '24 hours'
GROUP BY x
ORDER BY x
```

**Entity Creation Rates:**
```sql
SELECT
    time_bucket($resolution, start_timestamp) AS x,
    sum(venues_created) as new_venues,
    sum(venues_found) as existing_venues,
    sum(artists_created) as new_artists,
    sum(artists_found) as existing_artists
FROM records
GROUP BY x
```

**Failure Rates by Service:**
```sql
SELECT
    service_name,
    sum(task_failed) as failures,
    sum(task_succeeded) as successes,
    (sum(task_failed)::float / (sum(task_failed) + sum(task_succeeded))) * 100 as failure_rate
FROM records
WHERE start_timestamp >= now() - interval '1 hour'
GROUP BY service_name
```

#### 6.4 Alerting

**Alert Configurations:**

1. **High Error Rate**
   - Query: Error count > 10 in 5 minutes for any service
   - Webhook: Slack notification

2. **Pipeline Stall**
   - Query: No new extractions in 30 minutes (during expected hours)
   - Webhook: Slack notification

3. **DLQ Spike**
   - Query: More than 5 tasks hit DLQ in 15 minutes
   - Webhook: Slack notification

---

### Component 7: Pydantic-AI Update

**Current:** Pre-v1 (beta/pre-release version)
**Target:** Latest stable (1.18.0 as of planning, use latest at implementation)

**Scope:**
- Update dependency in all services using pydantic-ai
- Fix any breaking API changes
- Monitor for reduction in AI integration errors
- Update related dependencies if needed

**Expected Benefits:**
- Fewer persistent AI integration errors
- Better performance/reliability
- Access to new features
- Active support and bug fixes

---

### Component 8: Testing Infrastructure (Nice to Have)

**Prerequisites:** Complete after Pydantic-AI update

**Scope:**
- Finish pydantic/deep evals setup
- Get all evals working fully
- Improve test coverage for AI extraction agents

**Note:** Separate work item, not blocking other components.

---

## Technical Dependencies

### Initiative Dependencies
- **Blocks:** Admin Interface pipeline management tools (can trigger Cloud Tasks)
- **Blocked by:** None (foundational work)
- **Coordination:** Admin Interface for failed_tasks UI

### Technology Dependencies
- **New GCP Services:** Cloud Tasks (queues), Terraform state bucket
- **New Libraries:**
  - `google-cloud-tasks` (Python client)
  - `terraform` (CLI tool)
  - Latest `pydantic-ai`
- **Infrastructure:** GCS bucket for Terraform state

---

## Technical Risks

### Medium Risk
- **Risk:** Cloud Tasks migration complexity
  - **Impact:** Longer timeline, potential bugs during transition
  - **Likelihood:** Medium
  - **Mitigation:** Gradual migration, one stage at a time, both systems coexist
  - **Contingency:** Roll back individual service if issues arise

- **Risk:** Pydantic-AI breaking changes
  - **Impact:** Time spent fixing API changes
  - **Likelihood:** Medium (jumping from pre-v1 to v1.x)
  - **Mitigation:** Comprehensive testing, phased rollout
  - **Contingency:** Pin to specific version, address issues incrementally

### Low Risk
- **Risk:** Terraform learning curve
  - **Impact:** Slower initial setup
  - **Likelihood:** Low (limited scope, good documentation)
  - **Mitigation:** Start with minimal resources, expand later

---

## Deployment Strategy

### Order of Deployment
1. **UV Migration:** Service by service, deploy after each
2. **Terraform:** One-time setup, then integrated into CI/CD
3. **Logfire Instrumentation:** Can deploy incrementally with each service
4. **Cloud Tasks Migration:** One pipeline stage at a time
5. **Pydantic-AI:** Single deployment after thorough testing

### Rollback Plan
- Gradual migration means both Pub/Sub and Cloud Tasks work simultaneously
- Can revert individual services without affecting others
- Terraform state allows infrastructure rollback if needed

### Feature Flags
- Not required - using gradual migration instead
- Old and new paths coexist during transition

---

## Success Criteria

- [ ] All services using UV + pyproject.toml with `venv/` directories
- [ ] Terraform managing Cloud Tasks queues and DLQ topics
- [ ] All Pub/Sub triggers converted to Cloud Tasks
- [ ] All Firestore triggers removed (explicit task creation)
- [ ] Failed tasks visible in admin UI with retry capability
- [ ] Logfire dashboard showing pipeline funnel metrics
- [ ] Alerts configured for error rates and pipeline stalls
- [ ] Entity found/created metrics being tracked
- [ ] Pydantic-AI updated to latest stable
- [ ] All tests passing

---

## Open Technical Questions

- [ ] Exact number of Cloud Tasks queues needed (one per stage? per service type?)
- [ ] Terraform state bucket naming and access controls
- [ ] Specific Slack webhook configuration for alerts
- [ ] Admin UI design for failed tasks (separate initiative or part of this?)

---

## Estimated Effort

**Total:** 2-4 weeks with 0.5 engineer (~40 hours total)

**Breakdown:**
- UV migration: 4 hours
- Terraform setup: 3 hours
- Logfire instrumentation: 2 hours
- Cloud Tasks client: 2 hours
- Cloud Tasks migration: 16 hours (largest piece, stage by stage)
- DLQ + Failed Tasks: 3 hours
- Dashboard & Alerts: 3.5 hours
- Pydantic-AI update: 4 hours
- Cleanup & docs: 3 hours

**Note:** Estimates assume half-time engineer. Testing infrastructure improvements (5 hours) optional/nice to have.

---

## Next Steps

- [ ] Implementation planning (break down into detailed tasks)
- [ ] Effort estimation refinement
- [ ] Approval & prioritization
- [ ] Create issues in mystage-event-sourcing repository

---

**Document History:**
- Initial planning document created
- Technical architecture added based on brainstorming session
