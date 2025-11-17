# Venue Merge - Asana Tasks Reference

**Initiative**: venue-merge
**Created**: 2025-11-17
**Total Tasks**: 25 (backend) + 5 (admin UI) = 30 total

All tasks follow the naming convention: `[Venue-Merge X.Y] [Task Name]`

**To find all tasks:** Search Asana for `[Venue-Merge`

## Tasks by Project

### -MS D Data Pipeline (25 tasks)

| Task | Name | Priority | Est. Hours | Asana URL |
|------|------|----------|------------|-----------|
| 1.1 | Create VenueDuplicate Pydantic Model | High | 1 | https://app.asana.com/0/0/1211913454299742 |
| 1.2 | Add Soft-Delete Fields to Venue Model | High | 1 | https://app.asana.com/0/0/1211913454427239 |
| 1.3 | Create Shared Venue Matching Utility | High | 3 | https://app.asana.com/0/0/1211913191442571 |
| 1.4 | Setup New Service Directory Structure | High | 1 | https://app.asana.com/0/0/1211913535832492 |
| 1.5 | Configure Cloud Tasks Queue and Firebase Integration | High | 2 | https://app.asana.com/0/0/1211913454716015 |
| 2.1 | Add Cloud Tasks Helper Utility | High | 2 | https://app.asana.com/0/0/1211913373009934 |
| 2.2 | Update Entity Writers for Cloud Tasks | High | 3 | https://app.asana.com/0/0/1211913373210283 |
| 2.3 | Update Entity Source Writer to Enqueue Cloud Tasks | High | 2 | https://app.asana.com/0/0/1211913373254978 |
| 3.1 | Implement Validation Service Core Logic | High | 4 | https://app.asana.com/0/0/1211913638878662 |
| 3.2 | Add Data Integrity Check and Swapping Logic | High | 3 | https://app.asana.com/0/0/1211913722094733 |
| 3.3 | Add Admin-Flagged Duplicate Handling | High | 2 | https://app.asana.com/0/0/1211913638401934 |
| 3.4 | Add Cloud Task Enqueuing for High-Confidence Merges | High | 2 | https://app.asana.com/0/0/1211913375443265 |
| 4.1 | Implement Merge Executor Scaffolding | High | 2 | https://app.asana.com/0/0/1211913642413602 |
| 4.2 | Implement Entity Sources Update Logic | High | 4 | https://app.asana.com/0/0/1211913725735417 |
| 4.3 | Implement Extractions Update Logic | High | 4 | https://app.asana.com/0/0/1211913642460517 |
| 4.4 | Implement Soft-Delete and Status Update Logic | High | 3 | https://app.asana.com/0/0/1211913725906967 |
| 4.5 | Add Error Handling and Idempotency | High | 3 | https://app.asana.com/0/0/1211913722230647 |
| 5.1 | Add Soft-Delete Filtering to Entity Resolution | High | 2 | https://app.asana.com/0/0/1211913730531517 |
| 6.1 | Create Integration Tests | Medium | 6 | https://app.asana.com/0/0/1211913647160837 |
| 6.2 | Update Documentation | Medium | 2 | https://app.asana.com/0/0/1211913383297602 |

### -MS D Admin Portal (5 tasks)

| Task | Name | Priority | Est. Hours | Asana URL |
|------|------|----------|------------|-----------|
| 4.1 | Add Swap Button with Confirmation Dialog | High | 2 | https://app.asana.com/0/0/1211913349392911 |
| 4.2 | Add ID Editing with Validation | High | 2 | https://app.asana.com/0/0/1211913351844268 |
| 4.3 | Implement Merge Operation with venueMergeService | High | 3 | https://app.asana.com/0/0/1211913272780386 |
| 4.4 | Integrate VenueMergePanel into VenuesPage | High | 3 | https://app.asana.com/0/0/1211913272851353 |
| 4.5 | Update Documentation Indexes | Medium | 1 | https://app.asana.com/0/0/1211913273251921 |

## Tasks by Repository

**mystage-event-sourcing**: Tasks 1.1-1.5, 2.1-2.3, 3.1-3.4, 4.1-4.5, 5.1, 6.1-6.2
**mystage-admin-interface**: Tasks 4.1-4.5 (Admin UI)

## Effort Summary by Phase

| Phase | Description | Tasks | Est. Hours |
|-------|-------------|-------|------------|
| Phase 1 | Foundation & Models | 5 | 8 |
| Phase 2 | Cloud Tasks Integration | 3 | 7 |
| Phase 3 | Validation Service | 4 | 11 |
| Phase 4 | Merge Executor | 5 | 16 |
| Phase 5 | Entity Resolution Update | 1 | 2 |
| Phase 6 | Testing & Docs | 2 | 8 |
| Admin UI | Admin Interface | 5 | 11 |
| **Total** | | **25** | **63** |

**Total Estimated Hours**: 63 hours (~1.5-2 weeks with 1 engineer)

## Task Dependencies

```
Phase 1: Foundation (can start immediately)
├── 1.1 VenueDuplicate Model (no deps)
├── 1.2 Soft-Delete Fields (no deps)
├── 1.3 Venue Matching Utility (no deps)
├── 1.4 Service Directory Structure (no deps)
└── 1.5 Cloud Tasks Queue Config (after 1.4)

Phase 2: Cloud Tasks Integration (after Phase 1)
├── 2.1 Cloud Tasks Helper (after 1.5)
├── 2.2 Entity Writers Update (after 2.1)
└── 2.3 Entity Source Writer Update (after 2.1)

Phase 3: Validation Service (after Phase 1)
├── 3.1 Validation Core Logic (after 1.1, 1.3)
├── 3.2 Data Integrity Check (after 3.1)
├── 3.3 Admin-Flagged Handling (after 3.1)
└── 3.4 Cloud Task Enqueuing (after 3.1, 2.1)

Phase 4: Merge Executor (after Phase 2, 3)
├── 4.1 Merge Executor Scaffolding (after 3.4)
├── 4.2 Entity Sources Update (after 4.1)
├── 4.3 Extractions Update (after 4.1)
├── 4.4 Soft-Delete & Status Update (after 4.1, 1.2)
└── 4.5 Error Handling & Idempotency (after 4.2, 4.3, 4.4)

Phase 5: Entity Resolution (after Phase 4)
└── 5.1 Soft-Delete Filtering (after 1.2)

Phase 6: Testing & Docs (after Phase 5)
├── 6.1 Integration Tests (after 4.5, 5.1)
└── 6.2 Documentation (after 6.1)

Admin UI (parallel with backend, after Phase 3)
├── 4.1 Swap Button (after 3.1)
├── 4.2 ID Editing (after 4.1)
├── 4.3 Merge Operation (after 4.2)
├── 4.4 VenueMergePanel Integration (after 4.3)
└── 4.5 Documentation (after 4.4)
```
