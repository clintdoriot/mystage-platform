# Initiative Implementation Plan: Comprehensive Notification System

## Overview

The Comprehensive Notification System brings real-time engagement alerts to MyStage users through an in-app notification center and push notifications. This initiative implements an account-centric fan-out architecture where notifications are created for each account managing a profile, ensuring independent read status and badge counts while maintaining cross-device sync through Firestore real-time listeners.

**Total Effort**: 103 hours (~2.6 weeks for 1 engineer)
**Timeline**: 2-3 weeks with parallelization (backend + frontend work can overlap)
**Team Size**: 1-2 engineers (backend + frontend work)
**Repositories Affected**: mystage-databases, mystage-app-backend, mystage-app
**Risk Level**: 🟡 Medium - New feature with push notification complexity and external API security

## Dependencies

### Blocking Dependencies
**None** - This initiative builds on existing Firebase infrastructure and social features

### Unblocks
- **Chat System Notifications** (Phase 2) - DM notification foundation enables future chat enhancements
- **Admin Notification Tools** (Phase 2) - System/account notifications for admin-initiated actions
- **Content Moderation Alerts** (Phase 2+) - Notification infrastructure for moderation workflows

### Coordination Required
- **Database Schema & Tooling Initiative**: Coordinate on schema documentation format and CI/CD integration
- **FlutterFlow App Updates**: Ensure notification center UI follows established FlutterFlow patterns

## Phase 1: Foundation & Schema (Weeks 1-2)

### Task 1.1: Design Firestore Schema & Indexes

#### SCOPE OF WORK
Create the complete Firestore schema definition for the `notifications/` collection including all fields, data types, indexes, and security rules. This is the foundation that enables all notification functionality.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-databases
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `databases/main/collections/notifications.md` - Complete schema documentation
- Firestore indexes definition (in Firestore console or JSON config)
- Security rules for `notifications/` collection
- Index configuration for common queries (receiverAccount + createdAt, etc.)

**Acceptance Criteria:**
- Schema includes all 22 fields defined in initiative spec (receiverAccount, receiverProfile, type, etc.)
- Composite indexes defined for: `receiverAccount + createdAt DESC`, `receiverAccount + read + createdAt`
- Security rules prevent frontend creation, allow account-based read/update
- Schema documentation follows mystage-databases conventions

#### PREREQUISITES

**Dependencies from previous tasks:**
- None (this is the first task)

**Required decisions:**
- Schema documentation format (if Database Schema & Tooling initiative hasn't defined it yet)
- Firestore index deployment process (manual via console or automated via JSON)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Should indexes be deployed manually via Firebase console or automated via `firestore.indexes.json`?
2. What schema documentation format should be used? (Markdown, JSON Schema, Pydantic models?)
3. Should this schema follow the pattern from Database Schema & Tooling initiative or establish its own pattern?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing Firestore collections in mystage-databases for schema documentation patterns
- Check Database Schema & Tooling initiative for schema format standards
- Review Firebase documentation for composite index best practices

**Design phase:**
- Document complete `notifications/` schema with all 22 fields
- Design composite indexes for badge count and notification list queries
- Write security rules for account-centric read/update permissions

**Implementation phase:**
- Create schema documentation file
- Configure indexes (console or JSON)
- Add security rules to firestore.rules file
- Test index deployment in development environment

**Review phase:**
- Backend engineer reviews schema completeness
- Verify indexes support all planned queries
- Test security rules with mock data

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Schema documentation created with all 22 fields and data types
- [ ] Composite indexes configured for badge count and list queries
- [ ] Security rules implemented with account-based permissions
- [ ] Schema documentation reviewed and approved
- [ ] Indexes deployed to development Firestore
- [ ] Security rules deployed to development Firestore

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Low
- **Risk**: 🟢 Low - Well-understood schema design

---

### Task 1.2: Create Notification Configuration File

#### SCOPE OF WORK
Create a centralized configuration file (`notification_config.py`) that defines all notification types, their properties (push-enabled, deep link pages, message templates), and provides helper functions for notification creation and type-checking.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/notification_config.py` - Notification type configuration
- Type definitions for all 6 Phase 1 notification types (like, comment, reply, mention, follow, DM)
- Helper functions for notification creation (create_notification, get_notification_config, etc.)
- Deep link page constants (PostDetailPage, ProfilePage, ChatPage, etc.)

**Acceptance Criteria:**
- Configuration includes all 6 Phase 1 notification types with correct push-enabled flags
- Deep link page constants match FlutterFlow page names
- Message template functions generate user-friendly notification text
- Type-safe configuration (TypedDict or dataclass)
- Unit tests for helper functions

#### PREREQUISITES

**Dependencies from previous tasks:**
- None (can proceed in parallel with schema design)

**Required decisions:**
- Deep link page names in FlutterFlow (must match exact page names for routing)
- Message template format (simple strings vs. parameterized templates)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What are the exact FlutterFlow page names for deep linking? (PostDetailPage, ProfilePage, ChatPage?)
2. Should deep link pages be constants in notification_config.py or a separate constants file?
3. Are message templates simple strings or should they support rich formatting?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing FlutterFlow pages in mystage-app for exact page names
- Check existing backend configuration patterns (if any)
- Review Python best practices for configuration files

**Design phase:**
- Design notification type enum or constants
- Design configuration structure (dict, dataclass, or TypedDict)
- Design message template functions (parameterized strings)

**Implementation phase:**
- Create notification_config.py with type definitions
- Implement helper functions (create_notification, get_notification_config)
- Add deep link page constants
- Write unit tests for configuration access

**Review phase:**
- Backend engineer reviews configuration structure
- Verify all Phase 1 types are included
- Test helper functions with mock data

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] notification_config.py created with all 6 Phase 1 types
- [ ] Helper functions implemented and tested
- [ ] Deep link page constants defined (verified against FlutterFlow)
- [ ] Message template functions generate user-friendly text
- [ ] Unit tests pass with 100% coverage
- [ ] Code reviewed and approved

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 2 hours
- **Complexity**: Low
- **Risk**: 🟢 Low - Straightforward configuration file

---

### Task 1.3: Deploy Schema to Development Firestore

#### SCOPE OF WORK
Deploy the notifications schema, indexes, and security rules to the development Firestore database. Verify deployment success and test security rules with manual operations.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-databases
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- Deployed schema documentation (if using automated tooling)
- Deployed indexes in development Firestore (verified in Firebase console)
- Deployed security rules in development Firestore
- Verification test results (manual document creation, query testing)

**Acceptance Criteria:**
- `notifications/` collection exists in development Firestore
- Composite indexes deployed and showing "Enabled" status in console
- Security rules deployed and prevent unauthorized access
- Manual tests confirm: admin SDK can create, users can read their own, users cannot create directly

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 1.1: Schema and indexes designed

**Required decisions:**
- Development Firestore database URL/project
- Deployment method (manual console, Firebase CLI, CI/CD)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What is the development Firestore project ID?
2. Should deployment be manual (Firebase console) or automated (Firebase CLI, CI/CD)?
3. Who has permission to deploy to development Firestore?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review mystage-databases deployment documentation
- Check Firebase CLI installation and authentication
- Identify development Firestore project

**Design phase:**
- Plan deployment steps (indexes first, then security rules)
- Design verification test cases
- Document rollback procedure if needed

**Implementation phase:**
- Deploy indexes via Firebase console or `firebase deploy --only firestore:indexes`
- Deploy security rules via Firebase console or `firebase deploy --only firestore:rules`
- Run verification tests (create notification with admin SDK, query as user)

**Review phase:**
- Verify indexes in Firebase console (check "Enabled" status)
- Verify security rules in Firebase console
- Backend engineer confirms deployment success

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Indexes deployed and showing "Enabled" in Firebase console
- [ ] Security rules deployed successfully
- [ ] Admin SDK can create notifications (tested)
- [ ] Users can query their own notifications (tested)
- [ ] Users cannot create notifications directly (tested)
- [ ] Deployment documented in mystage-databases repo

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 1 hour
- **Complexity**: Low
- **Risk**: 🟢 Low - Standard Firestore deployment

---

## Phase 2: Backend Notification Triggers (Weeks 3-5)

### Task 2.1: Implement Core Notification Creation Function

#### SCOPE OF WORK
Create a reusable `create_notification_for_accounts()` function that handles fan-out logic (reading profile.managers, creating one notification per account), deduplication (preventing duplicate notifications per account within 1 hour), and push job creation (writing to FlutterFlow's push notification collection).

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/notifications/create_notification.py` - Core notification creation function
- Fan-out logic implementation (read profile.managers, create N notifications)
- Deduplication logic (check for duplicate within 1 hour using composite key)
- Push job creation (write to ff_user_push_notifications/)
- Comprehensive unit tests for all code paths

**Acceptance Criteria:**
- Function handles single-manager profiles (1 notification created)
- Function handles multi-manager profiles (N notifications created, one per manager)
- Deduplication prevents duplicate notifications for same account within 1 hour
- Push jobs created only for push-enabled notification types
- Unit tests cover: single manager, multiple managers, deduplication, push job creation
- Error handling for missing profiles, invalid accounts, Firestore errors

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 1.2: Notification configuration file (defines notification types and push-enabled flags)
- Task 1.3: Schema deployed to development Firestore

**Required decisions:**
- Deduplication window (confirmed: 1 hour)
- Push job structure (must match FlutterFlow's ff_user_push_notifications schema)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What is the exact schema for ff_user_push_notifications/ collection? (FlutterFlow-managed)
2. Should we log errors when push job creation fails or fail the entire notification?
3. How should we handle profiles with 0 managers (orphaned profiles)?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing backend functions for Firestore read patterns
- Investigate FlutterFlow's ff_user_push_notifications schema (check existing records)
- Review Python Firebase Admin SDK documentation for batch writes

**Design phase:**
- Design function signature: create_notification_for_accounts(profile_ref, notification_type, actor_profile, metadata)
- Design deduplication key structure: f"{account_id}-{notification_type}-{content_id}-{hour}"
- Design error handling strategy (log and continue vs. fail fast)

**Implementation phase:**
- Read profile document to get managers array
- For each account in managers:
  - Check deduplication (query for existing notification with same key within 1 hour)
  - If not duplicate: create notification document in notifications/
  - If push-enabled: create push job document in ff_user_push_notifications/
- Implement batch writes for efficiency (Firestore batch limit: 500 operations)
- Add comprehensive error logging

**Review phase:**
- Unit tests with Firebase Emulator
- Code review focusing on fan-out logic and deduplication
- Performance review (batch size, query efficiency)

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Core function implemented with fan-out logic
- [ ] Deduplication logic prevents duplicates within 1 hour
- [ ] Push jobs created for push-enabled notification types only
- [ ] Unit tests achieve >90% code coverage
- [ ] Error handling covers all edge cases (missing profile, invalid account, Firestore errors)
- [ ] Performance tested with 10+ managers (worst case scenario)
- [ ] Code reviewed and approved

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Medium-High - Complex fan-out and deduplication logic
- **Risk**: 🟡 Medium - Core function that all triggers depend on

---

### Task 2.2: Implement Notification Creation Microservice Wrappers

#### SCOPE OF WORK
Create two Firebase Cloud Functions that wrap the core notification creation logic as separate microservices. (1) HTTP-callable function for authenticated users (FlutterFlow only), (2) Cloud Tasks-triggered function for backend services (admin, event-sourcing) that can specify the push collection type. Both are proper microservices wrapping the shared utility function.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: mystage-app (FlutterFlow may call this), mystage-admin-interface (admin tools may call this)

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/app_create_profile_notification.py` - HTTP-callable function for FlutterFlow
- `functions/src/app_backend_create_notification.py` - Cloud Tasks-triggered function for backend services
- Two separate microservices:
  1. `app_create_profile_notification` - HTTP-callable for authenticated users (FlutterFlow only), creates ff_user_push_notifications
  2. `app_backend_create_notification` - Cloud Tasks HTTP function for backend services, accepts push_collection parameter
- Authentication middleware (verify Firebase Auth token for app endpoint)
- Request validation (validate required fields, notification type, profile references)
- Cloud Tasks client helper for backend services to enqueue notification requests
- Comprehensive unit tests for both functions

**Acceptance Criteria:**
- `app_create_profile_notification` endpoint callable via HTTPS with Firebase Auth token
- `app_backend_create_notification` triggered via Cloud Tasks (HTTP endpoint but not public)
- Both functions call the shared `create_notification_for_accounts()` utility function
- App endpoint ALWAYS creates `ff_user_push_notifications/` documents
- Backend function accepts `push_collection` parameter ('ff_user_push_notifications' or 'ff_push_notifications')
- Request validation prevents invalid inputs (missing fields, invalid notification types)
- Authentication prevents unauthorized access to app endpoint (401 for missing/invalid token)
- Backend function is NOT publicly accessible (only Cloud Tasks can invoke)
- Cloud Tasks client helper makes it easy for backend services to enqueue requests
- Error responses include clear error messages and status codes
- Unit tests cover: successful calls, auth failures, validation errors, Cloud Tasks invocation

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 2.1: Core notification creation function implemented

**Required decisions:**
- Should backend function verify Cloud Tasks headers for security?
- Should we implement rate limiting for app endpoint?
- What's the schema for ff_push_notifications (broadcast notifications)?
- What Cloud Tasks queue should be used (create new or use existing)?

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Should we create a new Cloud Tasks queue or use an existing one?
2. What's the schema for ff_push_notifications? (broadcast to all users vs. targeted users?)
3. Should we implement rate limiting for app endpoint? If so, what limits? (e.g., 100 calls/minute per user)
4. Should FlutterFlow call this for all notifications or only specific use cases?
5. Should backend function verify Cloud Tasks headers (X-CloudTasks-TaskName, etc.) for security?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review Firebase Callable Functions documentation (for app endpoint)
- Review Cloud Tasks documentation (creating tasks, HTTP targets, authentication)
- Compare ff_user_push_notifications vs ff_push_notifications schemas
- Check existing Cloud Tasks usage in mystage repos (queue names, patterns)
- Review Cloud Tasks header validation for security

**Design phase:**
- Design request/response schemas for both functions
- Design authentication flow for app endpoint (Firebase Auth token)
- Design Cloud Tasks payload structure for backend function
- Design Cloud Tasks client helper API for backend services
- Design error handling and response codes
- Design security validation for backend function (Cloud Tasks headers)

**Implementation phase:**

**Function 1: FlutterFlow-Accessible HTTP Callable**

```python
# functions/src/app_create_profile_notification.py

from firebase_functions import https_fn
from firebase_admin import firestore
from notifications.create_notification import create_notification_for_accounts

@https_fn.on_call()
def app_create_profile_notification(req: https_fn.CallableRequest) -> dict:
    """
    Create notification for authenticated user.
    Creates ff_user_push_notifications for user-initiated actions.

    Request:
      - profile_ref: Profile to notify (path string)
      - notification_type: Type of notification
      - actor_profile: Profile triggering notification (optional)
      - metadata: Additional context

    Returns:
      - success: bool
      - notifications_created: int
    """
    # 1. Verify authentication (handled by on_call decorator)
    if not req.auth:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="Must be authenticated to create notifications"
        )

    # 2. Extract and validate request data
    data = req.data
    if not data.get('profile_ref') or not data.get('notification_type'):
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INVALID_ARGUMENT,
            message="Missing required fields: profile_ref, notification_type"
        )

    # 3. Call core function
    try:
        result = create_notification_for_accounts(
            profile_ref=firestore.document(data['profile_ref']),
            notification_type=data['notification_type'],
            actor_profile=firestore.document(data.get('actor_profile')) if data.get('actor_profile') else None,
            metadata=data.get('metadata', {}),
            push_collection='ff_user_push_notifications'  # User-initiated
        )

        return {
            'success': True,
            'notifications_created': result['count']
        }
    except Exception as e:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.INTERNAL,
            message=f"Failed to create notifications: {str(e)}"
        )


```

**Function 2: Backend Cloud Tasks HTTP Function**

```python
# functions/src/app_backend_create_notification.py

from flask import Request
from firebase_functions import https_fn
from firebase_admin import firestore
from notifications.create_notification import create_notification_for_accounts
import json

@https_fn.on_request()
def app_backend_create_notification(req: Request):
    """
    Cloud Tasks-triggered notification creation.
    NOT publicly accessible - only invokable by Cloud Tasks.

    Security: Verifies Cloud Tasks headers to ensure request came from Cloud Tasks.

    Request body (JSON):
        - profile_ref: Profile to notify (path string)
        - notification_type: Type of notification
        - actor_profile: Profile triggering notification (optional)
        - metadata: Additional context
        - push_collection: 'ff_user_push_notifications' or 'ff_push_notifications'

    Returns: 200 OK with JSON response
    """
    # 1. Verify this is a Cloud Tasks request (security)
    task_name = req.headers.get('X-CloudTasks-TaskName')
    queue_name = req.headers.get('X-CloudTasks-QueueName')

    if not task_name or not queue_name:
        return {'error': 'Unauthorized - not a Cloud Tasks request'}, 401

    # 2. Parse request body
    try:
        data = req.get_json()
    except Exception:
        return {'error': 'Invalid JSON'}, 400

    # 3. Validate required fields
    if not data.get('profile_ref') or not data.get('notification_type'):
        return {'error': 'Missing required fields: profile_ref, notification_type'}, 400

    push_collection = data.get('push_collection', 'ff_user_push_notifications')
    if push_collection not in ['ff_user_push_notifications', 'ff_push_notifications']:
        return {'error': f'Invalid push_collection: {push_collection}'}, 400

    # 4. Call core function
    try:
        result = create_notification_for_accounts(
            profile_ref=firestore.document(data['profile_ref']),
            notification_type=data['notification_type'],
            actor_profile=firestore.document(data.get('actor_profile')) if data.get('actor_profile') else None,
            metadata=data.get('metadata', {}),
            push_collection=push_collection
        )

        return {
            'success': True,
            'notifications_created': result['count']
        }, 200
    except Exception as e:
        return {'error': f'Failed to create notifications: {str(e)}'}, 500


# Helper function for backend services to enqueue Cloud Tasks
from google.cloud import tasks_v2

def enqueue_notification_task(
    profile_ref: str,
    notification_type: str,
    actor_profile: str = None,
    metadata: dict = None,
    push_collection: str = 'ff_user_push_notifications'
):
    """
    Helper function for backend services to enqueue notification creation.

    Usage (from mystage-admin-interface or mystage-event-sourcing):
        from backend_create_notification import enqueue_notification_task

        enqueue_notification_task(
            profile_ref='profiles/abc123',
            notification_type='system_alert',
            metadata={'message': 'Account verified'},
            push_collection='ff_push_notifications'
        )
    """
    client = tasks_v2.CloudTasksClient()

    # Configure for your project
    project = 'your-project-id'
    location = 'us-central1'
    queue = 'notifications'  # Or whatever queue name you choose

    parent = client.queue_path(project, location, queue)

    # Create task
    task = {
        'http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'url': f'https://{location}-{project}.cloudfunctions.net/app_backend_create_notification',
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'profile_ref': profile_ref,
                'notification_type': notification_type,
                'actor_profile': actor_profile,
                'metadata': metadata,
                'push_collection': push_collection
            }).encode()
        }
    }

    response = client.create_task(request={'parent': parent, 'task': task})
    return response.name
```

**Update core function to accept push_collection parameter:**

```python
# functions/src/notifications/create_notification.py

def create_notification_for_accounts(
    profile_ref,
    notification_type,
    actor_profile=None,
    metadata=None,
    push_collection='ff_user_push_notifications'  # NEW parameter
):
    """
    Core notification creation with fan-out.

    Args:
        push_collection: Which collection to use for push jobs
            - 'ff_user_push_notifications' for user-initiated notifications
            - 'ff_push_notifications' for admin/system notifications
    """
    # ... existing logic ...

    # When creating push job:
    if notification_config[notification_type].push_enabled:
        firestore.collection(push_collection).add({
            # ... push job data ...
        })
```

**FlutterFlow Usage (App Endpoint):**

```dart
// In FlutterFlow Custom Action
Future<void> createProfileNotification({
  required String profilePath,
  required String notificationType,
  String? actorProfilePath,
  Map<String, dynamic>? metadata,
}) async {
  final callable = FirebaseFunctions.instance.httpsCallable('app_create_profile_notification');

  try {
    final result = await callable.call({
      'profile_ref': profilePath,
      'notification_type': notificationType,
      'actor_profile': actorProfilePath,
      'metadata': metadata,
    });

    print('Created ${result.data['notifications_created']} notifications');
  } catch (e) {
    print('Error creating notification: $e');
  }
}
```

**Backend Service Usage (Cloud Tasks):**

```python
# In mystage-admin-interface or mystage-event-sourcing

from app_backend_create_notification import enqueue_notification_task

def send_system_notification(profile_id: str, notification_type: str, message: str):
    """Send system notification to a profile (e.g., account verification, policy updates)"""

    # Enqueue Cloud Task - notification creation happens asynchronously
    task_name = enqueue_notification_task(
        profile_ref=f'profiles/{profile_id}',
        notification_type=notification_type,
        metadata={
            'message': message,
            'system_generated': True
        },
        push_collection='ff_push_notifications'  # Broadcast to all devices
    )

    print(f'Enqueued notification task: {task_name}')
    return task_name


def send_targeted_notification(profile_id: str, notification_type: str, actor_id: str):
    """Send targeted notification to specific profile managers"""

    task_name = enqueue_notification_task(
        profile_ref=f'profiles/{profile_id}',
        notification_type=notification_type,
        actor_profile=f'profiles/{actor_id}',
        push_collection='ff_user_push_notifications'  # Targeted
    )

    return task_name
```

**Review phase:**
- Test app endpoint with Firebase Emulator (auth, validation)
- Test backend function with Cloud Tasks emulator
- Test request validation (missing fields, invalid types, invalid push_collection)
- Test Cloud Tasks header validation (security)
- Test FlutterFlow integration (can FlutterFlow call successfully?)
- Test cross-repo usage (can admin-interface enqueue tasks?)
- Code review focusing on security (auth for app endpoint, Cloud Tasks headers for backend)

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] App endpoint (app_create_profile_notification) deployed as HTTP-callable Cloud Function
- [ ] Backend function (app_backend_create_notification) deployed as Cloud Tasks HTTP target
- [ ] Cloud Tasks helper (enqueue_notification_task) available for backend services
- [ ] App endpoint requires Firebase Auth token (401 without token)
- [ ] App endpoint ALWAYS uses ff_user_push_notifications
- [ ] Backend function accepts push_collection parameter ('ff_user_push_notifications' or 'ff_push_notifications')
- [ ] Both functions are separate microservices wrapping shared create_notification_for_accounts() utility
- [ ] Backend function validates Cloud Tasks headers (X-CloudTasks-TaskName, X-CloudTasks-QueueName)
- [ ] Backend function validates push_collection parameter
- [ ] Request validation prevents invalid inputs (missing fields, invalid notification types)
- [ ] Error responses include clear messages and proper status codes
- [ ] Unit tests achieve >90% code coverage
- [ ] Integration tests verify end-to-end (HTTP call → notifications created, Cloud Task → notifications created)
- [ ] FlutterFlow can successfully call app endpoint (tested in dev)
- [ ] Admin interface can successfully enqueue Cloud Tasks (tested)
- [ ] Documentation includes usage examples for FlutterFlow and backend services

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Medium - HTTP functions, auth, validation
- **Risk**: 🟡 Medium - Security-critical (authentication, authorization)

---

### Task 2.3: Implement Social Interaction Triggers (Likes, Comments, Follows)

#### SCOPE OF WORK
Implement Firestore onCreate triggers for social interactions: likes (reactions/), comments (comments/), and follows (profile_relationships/). Each trigger calls the core notification creation function with the appropriate notification type and metadata.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/reactions.py` - Updated with notification trigger for likes
- `functions/src/comments.py` - New onCreate trigger for comments
- `functions/src/profile_relationships.py` - Updated with notification trigger for follows
- Integration with core notification creation function
- Unit tests for each trigger (onCreate event → notification created)

**Acceptance Criteria:**
- onReactionCreated trigger: creates "like" notification for post author's account(s)
- onCommentCreated trigger: creates "comment" notification for post author's account(s)
- onCommentCreated trigger: creates "reply" notification for parent comment author's account(s) (if reply)
- onProfileRelationshipCreated trigger: creates "follow" notification for followed profile's account(s)
- All triggers call create_notification_for_accounts() with correct parameters
- Unit tests verify notification creation with Firebase Emulator
- Error handling prevents trigger failures from breaking social actions

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 2.1: Core notification creation function implemented

**Required decisions:**
- Should reply notifications go to both post author AND parent comment author? (likely: only parent comment author)
- Should we create notifications for self-interactions? (e.g., user likes their own post)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Do reply notifications go to post author, parent comment author, or both?
2. Should self-interactions (user likes own post) create notifications?
3. Are there any rate limits per user (max notifications per hour)?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing onCreate triggers in mystage-app-backend (reactions.py, profile_relationships.py)
- Understand how to extract profile reference from reaction/comment/relationship documents
- Check existing comments collection schema for parent_id field

**Design phase:**
- Design trigger function signatures (follow existing patterns)
- Design metadata extraction (actor profile, content reference, timestamps)
- Design error handling (log and continue to avoid breaking social actions)

**Implementation phase:**
- **reactions.py**: Add notification creation to existing appReactionsProcessor
  - Extract: post reference, actor profile (from reaction document)
  - Call: create_notification_for_accounts(post.author_profile, "like", actor_profile, {post_ref})
- **comments.py**: Create new onCommentCreated trigger
  - Extract: post reference (root_id), parent comment reference (parent_id), actor profile
  - If reply: call create_notification_for_accounts(parent_comment.author_profile, "reply", ...)
  - If not reply: call create_notification_for_accounts(post.author_profile, "comment", ...)
- **profile_relationships.py**: Add notification creation to existing appProfileRelationshipsProcessor
  - Extract: target_profile, actor profile
  - Call: create_notification_for_accounts(target_profile, "follow", actor_profile)
- Add unit tests for each trigger with Firebase Emulator

**Review phase:**
- Test each trigger in development Firestore (create like → verify notification)
- Code review focusing on correct parameter extraction
- Error handling review (what happens if profile missing?)

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Like trigger creates notification for post author
- [ ] Comment trigger creates notification for post author
- [ ] Reply trigger creates notification for parent comment author
- [ ] Follow trigger creates notification for followed profile
- [ ] Self-interactions handled correctly (no notification or notification based on decision)
- [ ] Unit tests pass for all triggers
- [ ] Integration tests verify end-to-end flow (action → notification in Firestore)
- [ ] Error handling prevents trigger failures

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Medium - Multiple triggers, correct metadata extraction
- **Risk**: 🟡 Medium - Critical user-facing functionality

---

### Task 2.4: Implement Content Triggers (Mentions in Posts)

#### SCOPE OF WORK
Implement onCreate trigger for posts (posts/) that detects @mentions in post text and creates "mention" notifications for each mentioned profile's account(s). Uses fan-out architecture to notify all accounts managing mentioned profiles.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/posts.py` - New onCreate trigger for posts
- Mention detection logic (parse post text for @mentions)
- Profile lookup logic (resolve @username to profile reference)
- Notification creation for each mentioned profile (fan-out)
- Unit tests for mention detection and notification creation

**Acceptance Criteria:**
- onPostCreated trigger detects @mentions in post.text field
- Mention parser extracts profile references or usernames
- Profile lookup resolves usernames to profile documents
- One notification created per mentioned profile (with fan-out to accounts)
- Unit tests cover: single mention, multiple mentions, invalid mentions, self-mentions
- Error handling for missing profiles, invalid mentions

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 2.1: Core notification creation function implemented

**Required decisions:**
- Mention format: @username or @profileId? (likely: @username based on FlutterFlow patterns)
- Maximum mentions per post (to prevent spam)
- Should self-mentions create notifications?

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What format are mentions stored in posts? (@username, @profileId, or structured field?)
2. Is there a maximum number of mentions per post?
3. How should we handle invalid mentions (username not found)?
4. Should mentions in HTML-formatted posts be parsed differently?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review posts collection schema in Firestore rules
- Check existing post creation logic in mystage-app (FlutterFlow)
- Determine mention format (structured field vs. text parsing)

**Design phase:**
- Design mention extraction logic (regex or structured field access)
- Design profile lookup strategy (query by username vs. direct reference)
- Design error handling for invalid/missing profiles

**Implementation phase:**
- Create onPostCreated trigger in functions/src/posts.py
- If mentions are structured field:
  - Extract mention profile references directly
- If mentions are text-based (@username):
  - Parse post.text with regex to find @username patterns
  - Query profiles collection to resolve usernames to profile documents
- For each mentioned profile:
  - Call create_notification_for_accounts(mentioned_profile, "mention", author_profile, {post_ref})
- Add rate limiting (max 10 mentions per post)
- Add unit tests with Firebase Emulator

**Review phase:**
- Test mention detection with various post formats
- Verify profile lookup works correctly
- Test fan-out with multi-manager profiles
- Code review focusing on mention parsing and error handling

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Mention detection correctly identifies all @mentions in posts
- [ ] Profile lookup resolves mentions to profile documents
- [ ] Notifications created for each mentioned profile with fan-out
- [ ] Invalid mentions handled gracefully (logged, not failing)
- [ ] Self-mentions handled correctly (based on decision)
- [ ] Rate limiting prevents mention spam (max 10 mentions/post)
- [ ] Unit tests achieve >85% coverage
- [ ] Integration tests verify end-to-end (post with mention → notification created)

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Medium - Mention parsing and profile lookup complexity
- **Risk**: 🟡 Medium - Parsing logic can be tricky

---

### Task 2.5: Implement Direct Message Triggers

#### SCOPE OF WORK
Implement onCreate trigger for chat messages (chats/{chatId}/messages/{messageId}) that creates "dm" notifications for message recipients. Handles both 1:1 DMs and group chats (if applicable).

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/chats.py` - New onCreate trigger for chat messages
- Recipient determination logic (who should be notified)
- Notification creation for each recipient account
- Deduplication logic (don't notify if user is currently viewing chat)
- Unit tests for DM notification creation

**Acceptance Criteria:**
- onMessageCreated trigger creates "dm" notification for recipient(s)
- Sender does not receive notification for their own message
- Group chat handling (all participants except sender notified)
- Deduplication prevents notification if recipient is viewing chat (future enhancement)
- Unit tests cover: 1:1 DM, group chat, self-message
- Error handling for missing chat, invalid recipients

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 2.1: Core notification creation function implemented

**Required decisions:**
- How to determine recipients (read chat.participants field?)
- Should we check if recipient is currently viewing chat to skip notification?
- How are group chats structured in Firestore?

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What is the schema for chats collection? (participants field, structure?)
2. Are group chats supported or only 1:1 DMs?
3. How can we determine if a user is currently viewing a chat (to skip notification)?
4. Should notifications include message preview text?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review chats collection schema in mystage-databases
- Review existing chat implementation in mystage-app (FlutterFlow)
- Check if there's an "active chat" indicator per user

**Design phase:**
- Design recipient determination logic (extract from chat.participants)
- Design notification metadata (chat reference, message preview)
- Design deduplication strategy (check if user is viewing chat)

**Implementation phase:**
- Create onMessageCreated trigger in functions/src/chats.py
- Extract chat document to read participants field
- Filter participants (exclude sender)
- For each recipient:
  - Resolve participant to profile/account
  - Call create_notification_for_accounts(recipient_profile, "dm", sender_profile, {chat_ref, message_id})
- Add deduplication (skip notification if user is in chat)
- Add unit tests with Firebase Emulator

**Review phase:**
- Test with 1:1 DMs in development Firestore
- Test with group chats (if applicable)
- Verify sender doesn't receive notification
- Code review focusing on recipient determination

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] DM trigger creates notifications for all recipients except sender
- [ ] 1:1 DMs work correctly (one notification to recipient)
- [ ] Group chats work correctly (notifications to all participants except sender)
- [ ] Sender never receives notification for own message
- [ ] Deduplication prevents notification if user is viewing chat (if implemented)
- [ ] Unit tests achieve >85% coverage
- [ ] Integration tests verify end-to-end (send DM → notification created)

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Medium - Recipient determination and group chat handling
- **Risk**: 🟡 Medium - Chat schema complexity

---

### Task 2.6: Implement Daily Cleanup Function

#### SCOPE OF WORK
Create a Cloud Scheduler-triggered function that runs daily to delete notifications older than 7 days. Implements batch deletion to handle large volumes efficiently and logs cleanup statistics for monitoring.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend
**Team**: Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- `functions/src/notifications/cleanup.py` - Daily cleanup function
- Cloud Scheduler configuration (cron: `0 2 * * *` for 2am daily)
- Batch deletion logic (handle 1000s of old notifications)
- Cleanup statistics logging (count of deleted notifications)
- Unit tests for cleanup logic

**Acceptance Criteria:**
- Function triggered daily by Cloud Scheduler
- Deletes all notifications where createdAt < (now - 7 days)
- Batch deletion handles large volumes (500 documents per batch)
- Logs cleanup statistics (count deleted, execution time)
- Unit tests verify correct date filtering and batch deletion
- Error handling prevents partial deletions

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 1.3: Schema deployed to development Firestore

**Required decisions:**
- Cleanup time (2am UTC confirmed)
- Batch size for deletion (500 recommended)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What timezone should cleanup run in? (UTC, PST, user's timezone?)
2. Should we soft-delete (mark as deleted) or hard-delete notifications?
3. How should we handle errors mid-batch (rollback, continue, retry)?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review Cloud Scheduler setup in GCP console
- Review Firebase Admin SDK batch deletion patterns
- Check existing scheduled functions in mystage-app-backend

**Design phase:**
- Design Cloud Scheduler cron configuration
- Design batch deletion loop (query → batch delete → repeat)
- Design error handling strategy (log and continue)

**Implementation phase:**
- Create cleanup_old_notifications() function in functions/src/notifications/cleanup.py
- Configure Cloud Scheduler to trigger function daily at 2am UTC
- Implement batch deletion logic:
  - Query notifications where createdAt < (now - 7 days), limit 500
  - Create batch delete operation
  - Execute batch
  - Repeat until no more old notifications
- Add logging for cleanup statistics (count deleted, errors)
- Add unit tests with Firebase Emulator

**Review phase:**
- Test cleanup function in development Firestore (create old notifications, run cleanup)
- Verify batch deletion works with large volumes (1000+ old notifications)
- Monitor execution time and cost
- Code review focusing on batch logic and error handling

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Cloud Scheduler configured to trigger function daily at 2am UTC
- [ ] Function deletes notifications older than 7 days
- [ ] Batch deletion handles 1000+ notifications efficiently
- [ ] Cleanup statistics logged (count deleted, execution time)
- [ ] Unit tests achieve >90% coverage
- [ ] Integration test verifies cleanup in development Firestore
- [ ] Error handling prevents partial deletions

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Low-Medium - Scheduled function with batch deletion
- **Risk**: 🟢 Low - Standard cleanup pattern

---

## Phase 3: Frontend Notification Center (Weeks 6-8)

### Task 3.1: Implement Notification Center UI (FlutterFlow)

#### SCOPE OF WORK
Build the notification center UI in FlutterFlow including bell icon with badge count, notification list screen, and notification item cards with profile images, timestamps, and action buttons.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app
**Team**: Frontend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- Bell icon component with unread badge count (navigation bar or app bar)
- NotificationCenterPage (FlutterFlow page)
- Notification list view (ListView.builder with Firestore query)
- Notification item card component (profile image, text, timestamp, read indicator)
- Empty state UI (when no notifications)
- Loading state UI (while loading notifications)

**Acceptance Criteria:**
- Bell icon displays unread count badge (query: receiverAccount == currentUser && read == false)
- Tapping bell icon navigates to NotificationCenterPage
- Notification list displays 7 days of notifications (query: receiverAccount == currentUser, order: createdAt DESC)
- Each notification shows: profile image, formatted text, relative timestamp ("5m ago"), read/unread indicator
- List automatically updates when new notifications arrive (Firestore real-time listener)
- Empty state shows when no notifications exist
- Loading state shows while initial query loads

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 1.3: Schema deployed (so Firestore query can access notifications/)
- Task 2.1-2.4: Backend triggers implemented (so notifications are being created)

**Required decisions:**
- Badge count query optimization (query on every app open or cache?)
- Notification text formatting (how to display "User A liked your post")

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Where should the bell icon be placed? (Bottom navigation bar, app bar, both?)
2. Should badge count be queried on every app open or cached in local state?
3. What should the notification text format be? (e.g., "{actorName} liked your post" or richer formatting?)
4. Should notification center have pagination or infinite scroll?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing FlutterFlow pages in mystage-app for UI patterns
- Check existing Firestore query implementations in FlutterFlow
- Review FlutterFlow real-time listener setup

**Design phase:**
- Design bell icon placement and badge display
- Design NotificationCenterPage layout (list view with custom card components)
- Design notification item card (text, image, timestamp layout)
- Design empty state UI

**Implementation phase:**
- **Bell Icon Component**:
  - Add bell icon to navigation (app bar or bottom nav)
  - Add Firestore query for badge count: `notifications.where(receiverAccount == currentUser && read == false).count()`
  - Display badge with count
  - Add onTap navigation to NotificationCenterPage
- **NotificationCenterPage**:
  - Create new FlutterFlow page
  - Add Firestore query: `notifications.where(receiverAccount == currentUser).orderBy(createdAt, DESC).limit(50)`
  - Setup real-time listener for query
  - Build ListView with notification item cards
  - Add empty state widget (if query returns 0 results)
  - Add loading state widget (while query loading)
- **Notification Item Card**:
  - Display actor profile image (circular avatar)
  - Display formatted notification text (from notification.text field or generate from metadata)
  - Display relative timestamp (using Flutter timeago package)
  - Show read/unread indicator (blue bar or background color)

**Review phase:**
- UI/UX review (design team)
- Test with real notifications in development app
- Test real-time updates (create notification → see it appear instantly)
- Code review (FlutterFlow component structure)

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Bell icon displays correct unread badge count
- [ ] Tapping bell icon navigates to NotificationCenterPage
- [ ] Notification list displays all user notifications (7 days)
- [ ] Each notification shows profile image, text, timestamp, read status
- [ ] Real-time updates work (new notifications appear instantly)
- [ ] Empty state displays when no notifications
- [ ] Loading state displays during initial query
- [ ] UI reviewed and approved by design team

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Medium - FlutterFlow UI with Firestore real-time queries
- **Risk**: 🟡 Medium - FlutterFlow can be finicky with real-time listeners

---

### Task 3.2: Implement Notification Actions (Mark Read, Delete)

#### SCOPE OF WORK
Add interactive actions to notification items: mark as read/unread (tap notification or swipe gesture), delete notification (swipe gesture or button), and tap-to-navigate (deep link to content).

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app
**Team**: Frontend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- Mark as read action (tap notification → update notification.read = true)
- Mark as unread action (swipe or button → update notification.read = false)
- Delete notification action (swipe or button → update notification.deleted = true)
- Tap-to-navigate action (tap notification → deep link to content page)
- Optimistic UI updates (instant visual feedback before Firestore update completes)

**Acceptance Criteria:**
- Tapping notification marks it as read and navigates to content (deep link)
- Swipe left shows delete action
- Swipe right shows mark read/unread action (toggle)
- Deleting notification removes it from list instantly (optimistic update)
- Marking read/unread updates visual indicator instantly
- Firestore updates execute in background (with error handling)
- Badge count decreases when notification marked as read

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 3.1: Notification center UI implemented
- Security rules allow users to update their own notifications (read, deleted fields)

**Required decisions:**
- Swipe gesture direction (left to delete, right to mark read?)
- Soft delete (deleted = true) or hard delete (remove document)?

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Should delete be soft-delete (deleted = true) or hard-delete (remove document)?
2. What swipe gesture directions should be used? (left = delete, right = mark read?)
3. Should there be a confirmation dialog for delete?
4. Should marking read navigate to content immediately or require second tap?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review FlutterFlow swipe gesture components (Dismissible, Slidable)
- Review FlutterFlow Firestore update actions
- Check existing deep linking configuration in mystage-app

**Design phase:**
- Design swipe gesture actions (Slidable widget with actions)
- Design optimistic UI update strategy (update local state, then Firestore)
- Design error handling (what if Firestore update fails?)

**Implementation phase:**
- **Mark Read on Tap**:
  - Add onTap handler to notification item card
  - Update Firestore: `notifications/{notificationId}.update({read: true, readAt: now})`
  - Implement optimistic update (update local state immediately)
  - Navigate to deep link page (Task 3.3)
- **Swipe Actions**:
  - Wrap notification item in Slidable widget
  - Add left swipe action: Delete (update deleted = true)
  - Add right swipe action: Toggle read/unread (update read field)
  - Implement optimistic updates for both actions
- **Badge Count Update**:
  - Badge count query automatically updates when read status changes (real-time listener)
- **Error Handling**:
  - Show snackbar if Firestore update fails
  - Revert optimistic update if error occurs

**Review phase:**
- Test all actions with real notifications in development app
- Verify optimistic updates work correctly
- Test error scenarios (offline mode, Firestore errors)
- UI/UX review (gesture smoothness, visual feedback)

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Tapping notification marks as read and navigates to content
- [ ] Swipe gestures work for delete and mark read/unread
- [ ] Optimistic UI updates provide instant visual feedback
- [ ] Badge count decreases immediately when marking read
- [ ] Error handling shows user-friendly messages
- [ ] All actions tested in development app
- [ ] UI/UX reviewed and approved

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Medium - Swipe gestures and optimistic updates
- **Risk**: 🟡 Medium - FlutterFlow gesture handling can be tricky

---

### Task 3.3: Implement Deep Linking to Content

#### SCOPE OF WORK
Configure FlutterFlow deep linking to navigate from notifications to specific content pages (PostDetailPage, ProfilePage, ChatPage) with correct context (post ID, profile ID, chat ID). Handles both in-app navigation and push notification deep links.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app
**Team**: Frontend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- Deep link configuration for all notification types (6 types)
- Navigation logic (extract content ID from notification, navigate to page)
- URL parameter handling (deep link URLs like `mystage://post/123`)
- Fallback handling (if deep link fails, stay on notification center)
- Deep link testing documentation

**Acceptance Criteria:**
- Tapping "like" notification navigates to PostDetailPage with correct post ID
- Tapping "comment" notification navigates to PostDetailPage with correct post ID
- Tapping "reply" notification navigates to PostDetailPage with correct post and comment ID
- Tapping "mention" notification navigates to PostDetailPage with correct post ID
- Tapping "follow" notification navigates to ProfilePage with correct profile ID
- Tapping "dm" notification navigates to ChatPage with correct chat ID
- Deep links work from push notifications (tap notification when app closed → app opens to correct page)
- Invalid deep links fallback to notification center (with error message)

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 1.2: Notification config defines deep link page constants
- Task 3.2: Tap-to-navigate action implemented

**Required decisions:**
- Deep link URL scheme (mystage://post/123 or custom scheme?)
- FlutterFlow page names (must match notification_config.py constants)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What deep link URL scheme should be used? (mystage:// or https://mystage.app/?)
2. What are the exact FlutterFlow page names? (PostDetailPage, ProfilePage, ChatPage?)
3. How should we handle deep links when app is killed (cold start)?
4. Should we track deep link success/failure in analytics?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review FlutterFlow deep linking documentation
- Check existing deep linking setup in mystage-app (if any)
- Review iOS Universal Links and Android App Links configuration

**Design phase:**
- Design deep link URL structure for each notification type
- Design navigation logic (switch statement based on notification.type)
- Design fallback handling (try-catch with fallback to notification center)

**Implementation phase:**
- **FlutterFlow Deep Link Configuration**:
  - Configure deep link scheme (mystage://) in FlutterFlow settings
  - Configure iOS Universal Links and Android App Links (if needed)
- **Navigation Logic**:
  - Extract notification type and metadata from notification document
  - Switch based on type:
    - `like`, `comment`, `mention` → PostDetailPage(postId: notification.metadata.postRef.id)
    - `reply` → PostDetailPage(postId: notification.metadata.postRef.id, commentId: notification.metadata.commentRef.id)
    - `follow` → ProfilePage(profileId: notification.actorProfile.id)
    - `dm` → ChatPage(chatId: notification.metadata.chatRef.id)
- **Push Notification Deep Links**:
  - Configure push notification payload to include deep link URL
  - Test deep links from push notifications (app in background, app killed)
- **Fallback Handling**:
  - Wrap navigation in try-catch
  - If error: show snackbar, stay on notification center

**Review phase:**
- Test all deep link types in development app
- Test deep links from push notifications (all 3 states: foreground, background, killed)
- Test fallback handling (invalid content ID, missing page)
- Document deep link testing process

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] All 6 notification types navigate to correct pages with correct IDs
- [ ] Deep links work from in-app notifications (tap in notification center)
- [ ] Deep links work from push notifications (tap push → app opens to page)
- [ ] Fallback handling shows error and stays on notification center
- [ ] Deep linking tested on iOS and Android
- [ ] Deep linking works when app is killed (cold start)
- [ ] Deep link testing documented

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Medium-High - Deep linking can be complex in FlutterFlow
- **Risk**: 🔴 High - Deep linking is notoriously finicky, especially cold starts

---

### Task 3.4: Implement Push Notification Permissions & Setup

#### SCOPE OF WORK
Configure FlutterFlow to request push notification permissions from users, handle permission states (granted, denied, provisional), and integrate with FlutterFlow's existing FCM token management system.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app
**Team**: Frontend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- Push notification permission request flow (prompt user for permission)
- Permission state handling (granted, denied, ask later)
- Integration with FlutterFlow FCM token management
- App icon badge count configuration (iOS)
- Settings page integration (global push on/off toggle)

**Acceptance Criteria:**
- App requests push notification permission on first launch or when notification settings accessed
- Permission states handled: granted (enable push), denied (show in-app only message), provisional (iOS)
- FCM token stored in FlutterFlow-managed collection (users/{uid}/fcm_tokens/)
- App icon badge displays unread notification count (iOS)
- Settings page has global push notification toggle (enable/disable)
- Push notification settings persist across app restarts

#### PREREQUISITES

**Dependencies from previous tasks:**
- FlutterFlow push notification infrastructure setup (assumed to exist)

**Required decisions:**
- When to request permission (first launch, on notification settings page, on first notification?)
- How to handle permission denial (show message, disable push toggle?)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. When should we request push notification permission? (first launch, settings page, other?)
2. Is FlutterFlow's FCM token management already configured? (ff_user_push_notifications/, users/{uid}/fcm_tokens/)
3. Should we have a settings page for notification preferences?
4. What should happen if user denies permission? (show message, re-prompt later?)

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review FlutterFlow push notification documentation
- Check existing FCM token management in mystage-app (if configured)
- Review iOS and Android permission best practices

**Design phase:**
- Design permission request timing (first launch, settings page)
- Design permission state handling (granted, denied, provisional)
- Design settings page UI (global toggle, per-type toggles in Phase 2)

**Implementation phase:**
- **Permission Request**:
  - Add push notification permission request to app initialization or settings page
  - Use FlutterFlow's built-in permission request actions
  - Handle permission states: granted (continue), denied (show message)
- **FCM Token Management**:
  - Verify FlutterFlow is storing tokens in users/{uid}/fcm_tokens/
  - Ensure tokens are refreshed when they change
- **App Icon Badge**:
  - Configure iOS badge count to display unread notification count
  - Query badge count: `notifications.where(receiverAccount == currentUser && read == false).count()`
  - Update badge on app open and when notifications change
- **Settings Page**:
  - Add global push notification toggle (enable/disable)
  - Store preference in user preferences (local storage or Firestore)
  - Disable push job creation in backend if user disabled push (Phase 2 enhancement)

**Review phase:**
- Test permission request flow on iOS and Android
- Verify FCM tokens are stored correctly
- Test app icon badge count updates
- Test settings toggle (enable/disable push)

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Push notification permission requested appropriately (first launch or settings)
- [ ] Permission states handled correctly (granted, denied, provisional)
- [ ] FCM tokens stored in FlutterFlow-managed collection
- [ ] App icon badge displays correct unread count (iOS)
- [ ] Settings page has global push toggle
- [ ] Permission and settings tested on iOS and Android

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Low-Medium - FlutterFlow handles most of FCM setup
- **Risk**: 🟡 Medium - iOS permission handling can be tricky

---

### Task 3.5: Create FlutterFlow Custom Action for Profile Notifications

#### SCOPE OF WORK
Create a FlutterFlow custom action that wraps the `app_create_profile_notification` Cloud Function, allowing FlutterFlow pages and workflows to trigger notifications directly for user-initiated actions (e.g., when a user mentions someone, tags a profile, or triggers other notification-worthy events from the UI).

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app
**Team**: Frontend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- FlutterFlow custom action: `createProfileNotification`
- Action parameters: `profileRef` (string), `notificationType` (string), `actorProfileRef` (string, optional), `metadata` (JSON, optional)
- Error handling for failed Cloud Function calls
- Documentation for when/how to use this action in FlutterFlow

**Acceptance Criteria:**
- Custom action callable from FlutterFlow workflows and page actions
- Action calls `app_create_profile_notification` Cloud Function with proper parameters
- Firebase Auth token automatically included (FlutterFlow handles this)
- Error handling shows user-friendly error messages if call fails
- Action returns success status and notifications created count
- Documentation includes usage examples for common scenarios (mention, tag, etc.)

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 2.2: `app_create_profile_notification` Cloud Function deployed

**Required decisions:**
- Which notification types should be triggerable from FlutterFlow vs backend-only?
- Should action have loading state indicator?

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Which notification types should be callable from FlutterFlow? (All user-initiated types or subset?)
2. Should the action show a loading indicator while calling the Cloud Function?
3. Should errors be shown to users or logged silently?
4. Are there specific FlutterFlow pages that need this action integrated immediately?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review FlutterFlow custom action documentation
- Check existing custom actions in mystage-app for patterns
- Review `app_create_profile_notification` API contract

**Design phase:**
- Design action parameter structure (match Cloud Function parameters)
- Design error handling strategy (user-facing vs silent)
- Identify initial use cases (which pages/workflows need this)

**Implementation phase:**
- **Create Custom Action**:
  - In FlutterFlow: Settings → Custom Code → Custom Actions
  - Create new action: `createProfileNotification`
  - Add parameters:
    - `profileRef` (String) - Path to profile being notified (e.g., "profiles/abc123")
    - `notificationType` (String) - Type of notification (e.g., "mention", "tag")
    - `actorProfileRef` (String, optional) - Profile triggering notification
    - `metadata` (JSON, optional) - Additional context
  - Implement action:
    ```dart
    Future<Map<String, dynamic>> createProfileNotification({
      required String profileRef,
      required String notificationType,
      String? actorProfileRef,
      Map<String, dynamic>? metadata,
    }) async {
      try {
        final callable = FirebaseFunctions.instance
            .httpsCallable('app_create_profile_notification');

        final result = await callable.call({
          'profile_ref': profileRef,
          'notification_type': notificationType,
          'actor_profile': actorProfileRef,
          'metadata': metadata ?? {},
        });

        return {
          'success': true,
          'notifications_created': result.data['notifications_created'],
        };
      } catch (e) {
        return {
          'success': false,
          'error': e.toString(),
        };
      }
    }
    ```

- **Add Error Handling**:
  - Catch Cloud Function errors
  - Return structured error response
  - Log errors for debugging

- **Documentation**:
  - Document action parameters
  - Provide usage examples for common scenarios
  - Document which notification types are supported

**Review phase:**
- Test action in FlutterFlow preview
- Verify Cloud Function is called correctly
- Test error scenarios (invalid parameters, network failure)
- Review with frontend team

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Custom action created in FlutterFlow
- [ ] Action successfully calls `app_create_profile_notification` Cloud Function
- [ ] Action parameters match Cloud Function API
- [ ] Error handling returns structured error responses
- [ ] Action tested in FlutterFlow preview mode
- [ ] Action tested in development app on device
- [ ] Documentation created with usage examples
- [ ] Code reviewed and approved

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Low - Straightforward Cloud Function wrapper
- **Risk**: 🟢 Low - Standard FlutterFlow custom action pattern

---

## Phase 4: Testing, Monitoring & Launch (Weeks 9-10)

### Task 4.1: Integration & End-to-End Testing

#### SCOPE OF WORK
Comprehensive testing of the entire notification system from trigger event → backend notification creation → push delivery → in-app display → user actions. Test all 6 notification types across iOS and Android devices.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-platform (test documentation)
**Team**: Backend + Frontend
**Also Affects**: mystage-app (testing in app), mystage-app-backend (trigger testing)

#### EXPECTED OUTPUTS

**Deliverables:**
- Integration test plan document (all notification types, all user flows)
- Test results documentation (pass/fail for each scenario)
- Bug reports for any issues found
- Performance test results (notification creation latency, query performance)
- Cross-device sync test results (mark read on device A → updates on device B)

**Acceptance Criteria:**
- All 6 notification types tested end-to-end (trigger → notification → push → display)
- Cross-device sync tested (notification center, badge count, read status)
- Deep linking tested for all notification types (from in-app and push)
- Performance tested (notification creation <1s, query <500ms, badge count <200ms)
- Error handling tested (offline mode, Firestore errors, permission denied)
- iOS and Android both tested (push notifications, deep links, permissions)

#### PREREQUISITES

**Dependencies from previous tasks:**
- All backend triggers implemented (Task 2.1-2.5)
- All frontend UI implemented (Task 3.1-3.4)
- Schema deployed to development Firestore (Task 1.3)

**Required decisions:**
- Test environment (development Firestore, test devices)
- Test data setup (test accounts, test profiles, test content)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Should we use development Firestore or a separate test Firestore database?
2. Are there test devices available (iOS and Android physical devices)?
3. Should we automate some tests (E2E test framework) or all manual testing?
4. What performance benchmarks are acceptable? (notification creation time, query time)

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing testing documentation in mystage repos
- Check if E2E testing framework is available (Flutter integration tests)
- Identify test devices and test accounts

**Design phase:**
- Design integration test matrix (6 notification types × multiple scenarios)
- Design performance test scenarios (1 manager vs. 5 managers, etc.)
- Design cross-device sync test scenarios

**Implementation phase:**
- **Integration Testing**:
  - Test each notification type end-to-end:
    1. Create trigger event (like post, send DM, etc.)
    2. Verify notification created in Firestore
    3. Verify push job created (if push-enabled)
    4. Verify push delivered to device
    5. Verify notification appears in notification center
    6. Verify deep link navigates correctly
  - Test fan-out scenarios (profile with multiple managers)
  - Test deduplication (duplicate trigger within 1 hour)
- **Performance Testing**:
  - Measure notification creation latency (onCreate trigger → notification in Firestore)
  - Measure query performance (notification list, badge count)
  - Measure cross-device sync latency (mark read → update on other device)
- **Cross-Device Testing**:
  - Test read status sync (mark read on iPhone → updates on Android)
  - Test delete sync (delete on iPad → disappears on iPhone)
  - Test badge count sync (mark read → badge decreases on all devices)
- **Error Handling Testing**:
  - Test offline mode (create notification while offline → sync when online)
  - Test permission denied (user denies push → in-app still works)
  - Test deep link failure (invalid content ID → fallback to notification center)

**Review phase:**
- Review test results with team
- Create bug reports for any failures
- Re-test after bug fixes

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] All 6 notification types pass end-to-end testing
- [ ] Cross-device sync works correctly (read status, delete, badge count)
- [ ] Deep linking works for all notification types (in-app and push)
- [ ] Performance meets benchmarks (creation <1s, query <500ms, badge <200ms)
- [ ] Error handling tested and working correctly
- [ ] iOS and Android both tested successfully
- [ ] Test results documented and reviewed

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Medium - Comprehensive testing across platforms
- **Risk**: 🟡 Medium - May discover bugs requiring fixes

---

### Task 4.2: Monitoring & Alerting Setup

#### SCOPE OF WORK
Configure monitoring dashboards and alerts for notification system health: track notification creation rates, push delivery success rates, error rates, query performance, and user engagement metrics (click-through rate, disable rate).

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-app-backend (logging configuration)
**Team**: Backend
**Also Affects**: GCP Monitoring (dashboards, alerts)

#### EXPECTED OUTPUTS

**Deliverables:**
- GCP Monitoring dashboard for notification system metrics
- Cloud Logging queries for notification-related logs
- Alerts for error conditions (high error rate, push delivery failures)
- Performance monitoring (onCreate trigger execution time, query latency)
- User engagement metrics tracking (click-through rate, disable rate)

**Acceptance Criteria:**
- Dashboard shows: notification creation rate (per type), push delivery success rate, error rate, query performance
- Alerts configured: error rate > 5%, push delivery failure rate > 10%, onCreate trigger timeout
- Logs include: notification creation events, push job creation, errors, deduplication events
- Metrics tagged by notification type (like, comment, follow, etc.)
- Dashboard accessible to engineering team

#### PREREQUISITES

**Dependencies from previous tasks:**
- Backend functions deployed with logging (Task 2.1-2.5)

**Required decisions:**
- Alerting thresholds (error rate, delivery failure rate)
- Dashboard layout and metrics priority

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What GCP project should monitoring be configured in?
2. Who should receive alerts? (email, Slack, PagerDuty?)
3. What are acceptable thresholds for error rate and delivery failure rate?
4. Should we track user engagement metrics (click-through, disable rate) in analytics or logging?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review GCP Monitoring documentation
- Check existing monitoring dashboards in mystage projects
- Review Cloud Logging query syntax

**Design phase:**
- Design dashboard layout (charts, metrics, time ranges)
- Design alert conditions (error rate, delivery failure, timeouts)
- Design logging structure (what to log, log levels, structured logging)

**Implementation phase:**
- **Logging Setup**:
  - Add structured logging to all backend functions (Cloud Logging)
  - Log: notification creation events, fan-out count, push job creation, errors, deduplication events
  - Use log levels appropriately (INFO, WARNING, ERROR)
- **Dashboard Creation**:
  - Create GCP Monitoring dashboard: "Notification System Health"
  - Add charts:
    - Notification creation rate (per notification type)
    - Push delivery success rate
    - Error rate (onCreate trigger failures)
    - Query performance (P50, P95, P99 latency)
    - Fan-out amplification (average managers per profile)
- **Alert Configuration**:
  - Alert 1: Error rate > 5% (5-minute window)
  - Alert 2: Push delivery failure rate > 10% (15-minute window)
  - Alert 3: onCreate trigger timeout (execution time > 60s)
  - Configure notification channels (email, Slack)

**Review phase:**
- Test alerts by triggering error conditions
- Verify dashboard displays correct metrics
- Review with team for additional metrics needed

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] GCP Monitoring dashboard created and accessible
- [ ] Dashboard shows notification creation rate, push delivery success, error rate, query performance
- [ ] Alerts configured for error conditions (error rate, delivery failure, timeout)
- [ ] Logging includes all notification events with structured data
- [ ] Alerts tested and verified working
- [ ] Team trained on dashboard usage

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Low-Medium - Standard GCP monitoring setup
- **Risk**: 🟢 Low - Well-understood monitoring patterns

---

### Task 4.3: Production Deployment

#### SCOPE OF WORK
Deploy notification system to production in a phased rollout: deploy schema and backend functions first, test with internal accounts, then deploy frontend app to beta testers, and finally roll out to all users while monitoring metrics.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-platform (deployment plan documentation)
**Team**: Backend + Frontend
**Also Affects**: mystage-databases, mystage-app-backend, mystage-app

#### EXPECTED OUTPUTS

**Deliverables:**
- Production deployment plan (step-by-step)
- Deployment checklist (pre-deployment, deployment, post-deployment)
- Rollback plan (how to disable notifications if issues arise)
- Production smoke test results (verify notifications working in production)
- Post-deployment monitoring report (first 24 hours)

**Acceptance Criteria:**
- Schema deployed to production Firestore (notifications/, indexes, security rules)
- Backend functions deployed to production (onCreate triggers, cleanup function)
- Cloud Scheduler configured for daily cleanup (production)
- Frontend app deployed to production (TestFlight/Play Store)
- Smoke tests pass in production (create notification, verify delivery)
- Monitoring dashboard shows healthy metrics (no errors, successful delivery)
- Rollback plan documented and tested

#### PREREQUISITES

**Dependencies from previous tasks:**
- All testing completed (Task 4.1)
- Monitoring configured (Task 4.2)

**Required decisions:**
- Rollout strategy (beta testers first, percentage rollout, or full rollout?)
- Rollback trigger conditions (what error rate requires rollback?)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. Should we do a phased rollout (beta → 10% → 50% → 100%) or full rollout?
2. What is the production Firestore project ID?
3. Who has permission to deploy to production?
4. What are the rollback trigger conditions (error rate, disable rate, delivery failure rate)?

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review existing production deployment processes in mystage repos
- Check Firebase project configuration (production vs. development)
- Review App Store and Play Store release processes

**Design phase:**
- Design deployment sequence (database → backend → frontend)
- Design smoke test scenarios (verify core functionality in production)
- Design rollback procedure (disable onCreate triggers, redeploy previous version)

**Implementation phase:**
- **Pre-Deployment**:
  - Run final integration tests in development
  - Review monitoring dashboard (ensure it's working)
  - Prepare rollback plan
  - Create production deployment checklist
- **Deployment Step 1: Database Schema**:
  - Deploy notifications/ schema to production Firestore
  - Deploy indexes (wait for indexes to build - may take hours)
  - Deploy security rules
  - Verify in Firebase console
- **Deployment Step 2: Backend Functions**:
  - Deploy onCreate triggers to production
  - Deploy cleanup function
  - Configure Cloud Scheduler for production
  - Verify functions deployed in GCP console
- **Deployment Step 3: Frontend App**:
  - Deploy app update to TestFlight (iOS beta)
  - Deploy app update to Play Store (Android beta)
  - Test with beta testers (internal team)
  - If successful: release to production (all users)
- **Post-Deployment**:
  - Run smoke tests (create test notifications, verify delivery)
  - Monitor dashboard for first 24 hours (watch error rate, delivery rate)
  - Monitor user feedback (support channels, app reviews)
  - Monitor metrics (session frequency, notification disable rate)

**Review phase:**
- Post-deployment review meeting (24 hours after launch)
- Review metrics vs. success criteria
- Identify issues and prioritize fixes
- Plan Phase 2 enhancements

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Schema deployed to production Firestore (verified)
- [ ] Backend functions deployed to production (verified)
- [ ] Frontend app deployed to production (TestFlight/Play Store)
- [ ] Smoke tests pass in production
- [ ] Monitoring shows healthy metrics (first 24 hours)
- [ ] No critical issues reported (support tickets, app crashes)
- [ ] Post-deployment review completed
- [ ] Rollback plan documented and ready (if needed)

#### EFFORT ESTIMATE
- **Size**: XS
- **Estimated Time**: 4 hours
- **Complexity**: Medium - Multi-repo deployment coordination
- **Risk**: 🟡 Medium - Production deployment always carries risk

---

### Task 4.4: User Engagement Metrics & Iteration Planning

#### SCOPE OF WORK
Track user engagement metrics post-launch (session frequency, click-through rate, notification disable rate), compare to pre-launch baseline, and plan Phase 2 enhancements based on learnings.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-platform (metrics documentation, Phase 2 planning)
**Team**: Product + Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- User engagement metrics report (week 1, week 2, week 4 post-launch)
- Comparison to baseline metrics (pre-notification vs. post-notification)
- User feedback summary (support tickets, app reviews, user interviews)
- Phase 2 recommendations (new notification types, features, improvements)
- Updated initiatives/_planning/notification-system.md with Phase 2 scope

**Acceptance Criteria:**
- Metrics tracked: session frequency increase, 30-day retention, click-through rate, disable rate
- Baseline comparison documented (% change in session frequency, retention)
- User feedback collected and summarized (top requests, top complaints)
- Phase 2 priorities identified (based on metrics + feedback)
- Recommendations reviewed with product and engineering teams

#### PREREQUISITES

**Dependencies from previous tasks:**
- Production deployment complete (Task 4.3)
- Monitoring configured (Task 4.2)

**Required decisions:**
- Metrics tracking period (1 week, 2 weeks, 1 month?)
- Phase 2 scope (what features to prioritize next?)

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. How long should we track metrics before planning Phase 2? (1 week, 2 weeks, 1 month?)
2. What analytics tool are we using? (Firebase Analytics, Mixpanel, custom?)
3. Who should be involved in Phase 2 planning discussions? (product, engineering, design?)
4. What are the most important metrics to track? (session frequency, retention, disable rate?)

#### IMPLEMENTATION APPROACH

**Research phase:**
- Set up analytics tracking (if not already configured)
- Define baseline metrics (pre-notification launch)
- Review success metrics from initiative spec

**Design phase:**
- Design metrics collection approach (Firebase Analytics events, custom logging)
- Design reporting cadence (daily, weekly)
- Design user feedback collection process (support tickets, in-app surveys)

**Implementation phase:**
- **Metrics Tracking**:
  - Track session frequency (app opens per user per week)
  - Track 30-day retention rate (% users who return after 30 days)
  - Track notification click-through rate (% notifications tapped)
  - Track notification disable rate (% users who disable push or specific types)
  - Compare to baseline (pre-notification metrics)
- **User Feedback Collection**:
  - Review support tickets related to notifications
  - Review app store reviews mentioning notifications
  - Conduct user interviews (optional, 5-10 users)
  - Summarize feedback (top requests, top complaints)
- **Phase 2 Planning**:
  - Analyze metrics vs. success criteria
  - Identify areas for improvement (low click-through, high disable rate)
  - Prioritize Phase 2 features based on data:
    - New notification types (shares, tags, milestones)
    - Per-type notification preferences (mute likes, mute follows)
    - Notification grouping (combine similar notifications)
    - Admin notifications (system messages, account alerts)
  - Update initiatives/_planning/notification-system.md with Phase 2 scope

**Review phase:**
- Review metrics report with product and engineering teams
- Discuss Phase 2 priorities and timeline
- Document Phase 2 scope and effort estimate

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] User engagement metrics tracked for 2-4 weeks post-launch
- [ ] Baseline comparison documented (session frequency, retention, etc.)
- [ ] User feedback collected and summarized
- [ ] Phase 2 priorities identified and documented
- [ ] Metrics report reviewed with product and engineering
- [ ] initiatives/_planning/notification-system.md updated with Phase 2 scope

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours (spread over 2-4 weeks post-launch)
- **Complexity**: Low-Medium - Data analysis and planning
- **Risk**: 🟢 Low - Metrics and planning work

---

### Task 4.5: Plan Notification System Phase 2 & 3

#### SCOPE OF WORK
Create detailed planning documents for Phase 2 (Music Industry Features + Advanced Controls) and Phase 3 (NFT/Merch + Advanced Features) based on Phase 1 learnings, user feedback, and business priorities. Define notification types, technical requirements, effort estimates, and implementation timeline for future phases.

#### REPOSITORY/LOCATION
**Primary Repository**: mystage-platform
**Team**: Product + Backend
**Also Affects**: None

#### EXPECTED OUTPUTS

**Deliverables:**
- Phase 2 detailed specification document (notification types, features, technical requirements)
- Phase 3 preliminary scope document (high-level features, dependencies)
- Effort estimates for Phase 2 implementation (weeks, team size)
- Updated `initiatives/_planning/notification-system.md` with refined Phase 2/3 scope
- Priority ranking for Phase 2 notification types (based on Phase 1 data)

**Acceptance Criteria:**
- Phase 2 spec includes all notification types from design doc (artist content, venue updates, admin/moderation)
- Phase 2 spec includes advanced controls (per-type preferences, quiet hours, manual artist push)
- Phase 3 scope covers NFT/merch, live streaming, collaboration features
- Effort estimates account for Phase 1 lessons learned (actual vs estimated effort)
- Phase 2 priorities aligned with business goals and user feedback from Phase 1
- Technical dependencies identified (what needs to exist before Phase 2 can start)

#### PREREQUISITES

**Dependencies from previous tasks:**
- Task 4.4: User engagement metrics and feedback collected
- Phase 1 production deployment complete (Task 4.3)

**Required decisions:**
- Business priority for Phase 2 vs other initiatives
- Which Phase 2 features are must-have vs nice-to-have
- Timeline for Phase 2 implementation

#### CLARIFICATION NEEDED

Before proceeding with this task, please confirm:
1. What business priorities should guide Phase 2 scope? (user growth, retention, revenue?)
2. Are there specific notification types from old spec we must include? (friend_posted, upcoming_event, claim_response, etc.)
3. Should Phase 2 planning wait for specific metrics thresholds from Phase 1? (e.g., 80% CTR, <5% disable rate)
4. What's the rough timeline for Phase 2 start? (3 months, 6 months, 1 year after Phase 1?)

#### IMPLEMENTATION APPROACH

**Research phase:**
- Review Phase 1 metrics report (from Task 4.4)
- Analyze user feedback and feature requests
- Review old notification spec for missing types
- Check business roadmap for dependent initiatives (NFTs, streaming, etc.)

**Design phase:**
- Organize Phase 2 notification types by category (artist content, venue, admin, advanced controls)
- Map notification types to trigger events and data sources
- Design per-type preference UI (grouped categories vs individual toggles)
- Design manual push notification feature (artist → fans, rate limiting)
- Identify technical dependencies (what needs to exist first)

**Implementation phase:**
- **Phase 2 Specification**:
  - Document all notification types with trigger conditions and metadata
  - Spec per-type preference controls (backend + frontend)
  - Spec manual push notification feature (admin interface + backend)
  - Spec quiet hours / Do Not Disturb (if validated as needed)
  - Estimate effort for each Phase 2 feature (based on Phase 1 actuals)
  - Create implementation timeline (assume same team size as Phase 1)

- **Phase 3 Scope**:
  - High-level feature list (NFT drops, live streaming, collaboration)
  - Dependencies on other initiatives (exchange-nfts, streaming infrastructure)
  - Preliminary effort estimate (rough order of magnitude)
  - Technical unknowns and research needs

- **Prioritization**:
  - Rank Phase 2 notification types by: user demand (feedback), engagement impact (CTR), business value
  - Identify MVP subset for Phase 2 (what's must-have vs can wait for Phase 3)
  - Create phased rollout plan within Phase 2 (if needed)

**Review phase:**
- Review Phase 2/3 plans with product, engineering, design teams
- Validate effort estimates against Phase 1 learnings
- Get business approval for Phase 2 scope and timeline
- Update master initiative document with refined scope

#### ACCEPTANCE CRITERIA

This task is complete when:
- [ ] Phase 2 specification document created with all notification types and features
- [ ] Phase 3 preliminary scope documented
- [ ] Effort estimates for Phase 2 calculated (based on Phase 1 actuals)
- [ ] Phase 2 notification types prioritized by user demand and business value
- [ ] Technical dependencies identified and documented
- [ ] initiatives/_planning/notification-system.md updated with refined Phase 2/3 scope
- [ ] Phase 2/3 plans reviewed and approved by product and engineering

#### EFFORT ESTIMATE
- **Size**: S
- **Estimated Time**: 8 hours
- **Complexity**: Low-Medium - Planning and documentation work
- **Risk**: 🟢 Low - Planning task, low technical risk

---

## Risk Mitigation

### High-Risk Areas

**1. Notification Spam/Fatigue**
- **Mitigation**: Conservative Phase 1 push strategy (only 4 types push-enabled), deduplication, monitoring disable rate
- **Contingency**: Code-level toggles to quickly disable notification types, rate limiting per user
- **Monitoring**: Track notification disable rate weekly, alert if > 10%

**2. Fan-Out Write Amplification**
- **Mitigation**: Most profiles have 1 manager (no amplification), bands/venues typically 2-3 managers (acceptable)
- **Contingency**: Monitor Firestore write costs, add rate limiting if costs become issue
- **Monitoring**: Track average managers per profile, track write costs vs. budget

**3. Deep Link Failures**
- **Mitigation**: Thorough testing of deep links for all notification types, fallback to notification center
- **Contingency**: Fix deep linking configuration in FlutterFlow, add logging to identify failures
- **Monitoring**: Track deep link success rate (analytics event), investigate failures

### Medium-Risk Areas

**4. Push Delivery Failures**
- **Mitigation**: Best-effort delivery approach, all notifications stored in-app regardless of push success
- **Contingency**: Monitor FCM delivery success rate, investigate failures with Firebase support
- **Monitoring**: Track push delivery success rate, alert if < 85%

**5. Cross-Device Sync Delays**
- **Mitigation**: Firestore real-time listeners are fast (<1s typically), acceptable delay
- **Contingency**: Monitor sync latency, investigate if > 1 second
- **Monitoring**: Track read status sync latency (client-side instrumentation)

### Low-Risk Areas

**6. Firestore Query Performance**
- **Mitigation**: Composite indexes ensure fast queries, badge count query is simple and indexed
- **Contingency**: Add caching if query cost becomes concern (Phase 2)
- **Monitoring**: Track query latency (P50, P95, P99), alert if P95 > 500ms

**7. onCreate Trigger Failures**
- **Mitigation**: Firebase Functions are reliable, comprehensive error logging, retry logic
- **Contingency**: Monitor error rate, investigate and fix trigger errors
- **Monitoring**: Track onCreate trigger error rate, alert if > 5%

## Success Metrics

### Primary Metrics (30 days post-launch)

1. **Session Frequency Increase**
   - **Target**: +15% increase in daily app opens per user
   - **Measurement**: Firebase Analytics (compare 30 days pre vs. 30 days post)
   - **Success**: ≥15% increase

2. **30-Day Retention Rate**
   - **Target**: +10% increase in 30-day retention
   - **Measurement**: Firebase Analytics (% users who return after 30 days)
   - **Success**: ≥10% increase

3. **Notification Disable Rate**
   - **Target**: <10% of users disable notifications
   - **Measurement**: User preferences (% users who disable push globally)
   - **Success**: <10% disable rate

### Secondary Metrics

4. **Click-Through Rate**
   - **Target**: >60% of notifications are tapped
   - **Measurement**: Analytics (tapped notifications / total notifications shown)
   - **Success**: ≥60% CTR

5. **Time to Respond to Social Interactions**
   - **Target**: Faster response to DMs and comments
   - **Measurement**: Time between notification creation and user response
   - **Success**: 30% reduction in median response time

6. **User-to-User Interaction Increase**
   - **Target**: +20% increase in comments, follows, likes
   - **Measurement**: Firestore queries (count of social actions per week)
   - **Success**: ≥20% increase

### Operational Metrics

7. **Push Delivery Success Rate**
   - **Target**: >90% of push jobs delivered successfully
   - **Measurement**: FCM delivery reports
   - **Success**: ≥90% delivery rate

8. **onCreate Trigger Error Rate**
   - **Target**: <2% error rate
   - **Measurement**: Cloud Logging (errors / total onCreate invocations)
   - **Success**: <2% error rate

9. **Query Performance**
   - **Target**: Badge count query <200ms P95, notification list query <500ms P95
   - **Measurement**: Client-side instrumentation
   - **Success**: Meet latency targets

## Implementation Timeline Summary

| Phase | Duration | Key Deliverables | Total Hours | Risk Level |
|-------|----------|------------------|-------------|------------|
| **Phase 1: Foundation** | 7 hours | Schema, indexes, security rules, notification config | 7h | 🟢 Low |
| **Phase 2: Backend Triggers** | 40 hours | Core function, HTTP wrappers, onCreate triggers, fan-out logic, deduplication, cleanup function | 40h | 🟡 Medium |
| **Phase 3: Frontend UI** | 28 hours | Notification center, mark read/delete, deep linking, push permissions, FlutterFlow custom action | 28h | 🟡 Medium |
| **Phase 4: Testing & Launch** | 28 hours | Integration testing, monitoring setup, production deployment, metrics tracking, Phase 2/3 planning | 28h | 🟡 Medium |

**Total Estimated Effort**: 103 hours (~2.6 weeks for 1 engineer, ~1.3 weeks for 2 engineers)
**Timeline with parallelization**: 2-3 weeks (backend + frontend work can be parallelized in Phases 2-3)
**Risk Level**: 🟡 Medium overall

### Task Breakdown by Hours:
- **XS (1-4h)**: 12 tasks (51 hours total)
- **S (8h)**: 9 tasks (72 hours total)
- **Total**: 21 tasks

## Next Steps After Completion

1. **Review this plan** with product and engineering teams
2. **Get approval** for scope and timeline
3. **Merge this PR** to move initiative from planning to active
4. **Run `/initiative-create-issues notification-system`** to generate GitHub issues
5. **Begin work** on Phase 1: Foundation & Schema

---

**Document History:**
- **2025-11-11** - Implementation plan created
  - Hierarchical breakdown into 4 phases, 18 tasks
  - Detailed task descriptions with effort estimates
  - Risk mitigation strategies and success metrics
  - Repository assignments and team ownership
