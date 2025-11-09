# Notification System Technical Brainstorming - Session Notes

**Date**: 2025-11-08
**Last Updated**: 2025-11-09
**Purpose**: Capture key technical constraints and decisions for the notification system architecture

---

## Session Summary

**Status**: 🟡 Partial - Awaiting Product Owner Input

**Progress:**
- ✅ Push notification provider selected (FCM)
- ✅ Platform constraints documented (FlutterFlow, Account/Profile model)
- ✅ Storage architecture defined (dual collections)
- ✅ Notification creation pattern established (backend onCreate triggers)
- ✅ Notifications collection schema finalized
- ✅ Deduplication strategy defined
- ✅ Cross-device sync mechanism chosen (Firestore real-time listeners)
- ✅ Deep linking configuration approach established (constants file)
- ✅ 7-day auto-delete implementation planned (scheduled Cloud Function)
- ⏳ Badge count management - **needs product owner decision**

**Next Steps:**
1. Get product owner input on badge count management approach
2. Continue technical brainstorming to cover remaining topics:
   - Performance considerations (indexing strategy, query optimization)
   - Testing strategy (how to test push notifications)
   - Monitoring & alerting (metrics to track)
   - Rollout strategy (feature flags, gradual rollout)
   - Security considerations (authorization, PII handling)
3. Update design specification with complete technical architecture
4. Move to implementation planning phase

---

## Key Decisions Made

### ✅ Push Notification Provider
**Decision**: Use Firebase Cloud Messaging (FCM)
**Rationale**:
- Already heavily invested in Firebase ecosystem
- Supports both iOS and Android
- Seamless integration with existing infrastructure
- Free tier suitable for Phase 1

---

## Critical Platform Constraints

### FlutterFlow Frontend
- **Frontend Framework**: FlutterFlow (no-code platform for Flutter apps)
- **Implication**: Front-end team uses visual builders and custom code

### FlutterFlow's Built-in Push Notification System

FlutterFlow has existing FCM + Firestore-based push notification infrastructure:

**Collections:**
- `ff_push_notifications/{id}` - Broadcast notifications
- `ff_user_push_notifications/{id}` - User-targeted notifications, prevented from system wide notifications
- `users/{uid}/fcm_tokens/{tokenId}` - Device token storage

**Key Functions:**
- `addFcmToken` - Registers device FCM tokens under users
- `sendPushNotificationsTrigger` - onCreate trigger for ff_push_notifications
- `sendUserPushNotificationsTrigger` - onCreate trigger for ff_user_push_notifications
- `sendScheduledPushNotifications` - Pub/Sub scheduler (can be set to desired interval)
- `sendPushNotifications` - Core delivery logic (batches up to 500 tokens)

**Schema (ff_user_push_notifications):**
```
{
  notification_title: string (required)
  notification_text: string (required)
  notification_image_url: string (optional)
  notification_sound: string (optional)
  initial_page_name: string (optional) // Deep link page
  parameter_data: string (optional) // JSON params for deep link
  user_refs: string (required) // Comma-separated Firestore user paths
  scheduled_time: timestamp (optional)
  status: string (output - "succeeded" or "failed")
  num_sent: number (output)
  error: string (output)
}
```

**We can:**
- Use their `addFcmToken` function (or implement our own version)
- Write to `ff_push_notifications` and `ff_user_push_notifications` to trigger push delivery
- Leverage their batching and delivery infrastructure if desired

---

## MyStage Data Model: Accounts vs Profiles

**CRITICAL COMPLEXITY**: N-to-N relationship between Accounts and Profiles

**MyStage Model:**
- **Accounts**: Login credentials, device FCM tokens
- **Profiles**: Public-facing identities (artist, venue, fan)
- **Relationship**: Many-to-many
  - One Account can manage multiple Profiles
  - One Profile can be managed by multiple Accounts

**Example:**
- Band Profile "The Rolling Stones" managed by 3 Accounts (manager, guitarist, drummer)
- Each Account has multiple devices (iPhone, iPad, Android)

**Notification Challenge:**
- Notifications are **profile-centric** (e.g., "Someone liked The Rolling Stones' post")
- FCM tokens are **account-centric** (stored under `users/{accountId}/fcm_tokens`)
- **Fan-out required**: Notification for 1 Profile → Must deliver to N Accounts → Each with M devices

**Note on FlutterFlow's "users":**
- FlutterFlow thinks of "users" as individuals with FCM tokens
- If we use FlutterFlow's built in action to send push notifications, we'd need a custom action to get all accounts for a set of profiles.
- In MyStage, these are "Accounts"
- FCM tokens would be added to Accounts, NOT Profiles

---

## Two Parallel Requirements

From the design specification (`initiatives/_planning/notification-system.md`):

### 1. In-App Notification Center
- Persistent notification history (7-day retention)
- Browseable inbox with read/unread status
- Mark as read/unread, delete individual notifications
- Cross-device read status sync
- Profile images, timestamps, deep links
- Query: "Show me all notifications for profiles I manage"

### 2. Push Notification Delivery
- Real-time delivery to devices (even when app closed)
- Deep linking from push to specific in-app page
- Badge count on app icon
- Global push on/off toggle
- Selective push by notification type (DMs/comments = push and in-app, likes/follows = in-app only)

**These are SEPARATE but RELATED systems:**
- In-app notifications = persistent storage, queried by app
- Push notifications = transient delivery mechanism

---

### ✅ Storage Architecture
**Decision**: Dual storage with separate collections

**Collections:**
1. **`notifications/{notificationId}`** - In-app notification center
   - Purpose: Persistent storage for notification history
   - Profile-centric (notifications belong to profiles)
   - 7-day retention with auto-cleanup
   - Read/unread status, deletion, cross-device sync
   - Query pattern: Get all notifications for a specific profile

2. **`ff_user_push_notifications/{pushId}`** - Push notification delivery
   - Purpose: Transient push delivery jobs
   - Account-centric (FCM tokens belong to accounts)
   - Triggers FlutterFlow's existing FCM delivery infrastructure
   - Contains account refs for fan-out
   - Status tracking (succeeded/failed, num_sent, error)

**Rationale:**
- Clean separation of concerns (persistent storage vs transient delivery)
- Leverage FlutterFlow's existing push delivery infrastructure
- In-app queries don't need to see push delivery metadata
- Different data models (profile-centric vs account-centric)

---

### ✅ Notification Creation Pattern
**Decision**: Backend onCreate triggers (primary pattern)

**Architecture:**
```
User Action (like, comment, follow, etc.)
  ↓
FlutterFlow writes to source collection (likes/, comments/, follows/)
  ↓
Backend onCreate trigger fires (onLikeCreated, onCommentCreated, etc.)
  ↓
Backend function:
  1. Check deduplication (query existing unread notifications)
  2. Create in-app notification (write to notifications/)
  3. Query managing accounts (profile_accounts collection)
  4. Create push job if configured (write to ff_user_push_notifications/)
  ↓
FlutterFlow's sendUserPushNotificationsTrigger fires
  ↓
FlutterFlow's delivery logic:
  - Queries FCM tokens for each account
  - Batches and sends to Firebase Cloud Messaging
  - Updates status fields
```

**Key Backend Triggers:**
- `onLikeCreated` - When someone likes a post
- `onCommentCreated` - When someone comments
- `onFollowCreated` - When someone follows
- `onDmCreated` - When someone sends a DM
- `onMentionCreated` - When someone mentions (@username)
- Auth triggers for account events (email verification, etc.)
- Scheduled functions for periodic notifications (profile completion prompts)

**Notification Type Configuration:**
- Code-based configuration (Phase 1)
- Each type specifies: enabled, usePush (true/false), title template, body template, deep link page
- Example: DMs/comments/replies/mentions use push, likes/follows are in-app only

**Fan-out Strategy:**
- Backend queries `profile_accounts` collection to find all accounts managing a profile
- Backend writes comma-separated account refs to `ff_user_push_notifications.user_refs`
- FlutterFlow's existing triggers handle FCM token lookup and delivery to devices
- Example: 1 Profile → 2 Accounts → 4 Devices (each account has 2 devices)

**FlutterFlow Team Workflow:**
- Like button → Firestore Action: Create Document in `likes/` collection
- Comment button → Firestore Action: Create Document in `comments/` collection
- Follow button → Firestore Action: Create Document in `follows/` collection
- **No custom notification logic needed in frontend** - backend handles everything

**Fallback for Ad-hoc Notifications:**
- Callable Cloud Function `createNotification` for notifications not tied to onCreate triggers
- Frontend or other backend functions can call directly
- Use cases: onboarding messages, periodic prompts, admin-initiated notifications

**Rationale:**
- **Reliability**: Notifications guaranteed to be created (not dependent on frontend completing)
- **Security**: Backend enforces rules, frontend can't fake notifications
- **Consistency**: Works from app, admin interface, APIs, future integrations
- **FlutterFlow simplicity**: Team just creates core data, backend handles notifications
- **Future-proof**: Easy to add new notification types without frontend changes

---

---

## Detailed Technical Decisions

### ✅ Notifications Collection Schema

**Collection**: `notifications/{notificationId}`

**Schema** (Python/Firestore):
```python
{
  # Identity
  "id": str,                          # Auto-generated document ID
  "receiverProfile": DocumentReference,  # Profile receiving the notification

  # Type & Content
  "type": str,                        # "like", "comment", "follow", "dm", etc.
  "title": str,                       # "John Doe liked your post"
  "body": str,                        # Additional details
  "imageUrl": str | None,             # Profile image or content thumbnail

  # Source context
  "sourceAccount": DocumentReference | None,   # Account that triggered (if applicable)
  "sourceProfile": DocumentReference | None,   # Profile that triggered (if applicable)
  "targetEntityId": str | None,       # The post/comment/etc being acted on
  "targetEntityType": str | None,     # "post", "comment", "profile", etc.

  # Deep linking
  "deepLinkPage": str,                # FlutterFlow page name
  "deepLinkParams": dict,             # JSON params for navigation

  # State management
  "read": bool,                       # Read/unread status (default: False)
  "deleted": bool,                    # Soft delete flag (default: False)
  "createdAt": firestore.SERVER_TIMESTAMP,
  "readAt": firestore.SERVER_TIMESTAMP | None,

  # Push notification tracking
  "hasPush": bool,                    # Whether this notification triggered a push
  "receiverAccounts": list[DocumentReference],  # Accounts that manage receiverProfile

  # Deduplication
  "dedupeKey": str,                   # Type-specific composite key for dedup
}
```

**Key Decisions:**
- Use DocumentReferences for all profile/account relationships (not string IDs)
- Soft delete with `deleted: bool`, hard delete after 7 days via scheduled cleanup
- Store `receiverAccounts` for query efficiency (avoid profile_accounts lookup on every query)
- `hasPush` tracks whether this notification triggered a push notification
- Type-specific `dedupeKey` format: `"type_<some_keys>"` (defined per notification type)

**Indexes Required:**
- `receiverProfile + createdAt` (descending) - Main query for notification center
- `dedupeKey` - Deduplication queries
- `createdAt` - Cleanup queries

---

### ✅ Deduplication Strategy

**Decision**: Skip creating duplicate notifications

**Implementation**:
```python
# Simple deduplication query - only check dedupeKey
existing = db.collection('notifications').where(
    'dedupeKey', '==', dedupe_key
).limit(1).get()

if existing:
    # Skip creating duplicate
    return
```

**Deduplication Key Format**:
- General format: `"type_<some_keys>"`
- Exact format defined when implementing each notification type
- Examples (to be confirmed during implementation):
  - Like: `"like_{postId}_{sourceProfileId}"`
  - Follow: `"follow_{sourceProfileId}"`
  - Comment: `"comment_{postId}_{sourceProfileId}"`

**Note**: Not overly concerned with deduplication complexity in Phase 1. Will refine as needed.

---

### ✅ Cross-Device Sync Mechanism

**Decision**: Firestore Real-Time Listeners (Phase 1)

**Implementation**:
```python
# Backend: Update read status
notification_ref.update({
    'read': True,
    'readAt': firestore.SERVER_TIMESTAMP
})

# Frontend: Real-time listener on all devices
db.collection('notifications')
  .where('receiverProfile', 'in', myManagedProfiles)
  .where('deleted', '==', False)
  .orderBy('createdAt', 'desc')
  .snapshots()  # Real-time updates across all devices
```

**Rationale**:
- Built into Firestore, automatic sync
- Works across all devices instantly
- No additional infrastructure needed
- Acceptable read costs for Phase 1 (optimize later if needed)

---

### ✅ Deep Linking Configuration

**Decision**: Backend maintains constants file with notification type configuration

**Configuration File** (`notification_config.py`):
```python
NOTIFICATION_TYPES = {
    "like": {
        "enabled": True,
        "usePush": False,  # In-app only
        "titleTemplate": "{sourceProfile.name} liked your post",
        "bodyTemplate": "",
        "deepLinkPage": "PostDetailPage",  # Actual FlutterFlow page name
        "deepLinkParamKeys": ["postId"],
    },
    "comment": {
        "enabled": True,
        "usePush": True,  # Push + in-app
        "titleTemplate": "{sourceProfile.name} commented on your post",
        "bodyTemplate": "{comment.text}",
        "deepLinkPage": "PostDetailPage",
        "deepLinkParamKeys": ["postId", "commentId"],
    },
    "follow": {
        "enabled": True,
        "usePush": False,
        "titleTemplate": "{sourceProfile.name} started following you",
        "bodyTemplate": "",
        "deepLinkPage": "ProfilePage",
        "deepLinkParamKeys": ["profileId"],
    },
    "dm": {
        "enabled": True,
        "usePush": True,
        "titleTemplate": "{sourceProfile.name} sent you a message",
        "bodyTemplate": "{message.preview}",
        "deepLinkPage": "ChatThreadPage",
        "deepLinkParamKeys": ["threadId"],
    },
    # ... more types defined during implementation
}
```

**Rationale**:
- Single source of truth for notification configuration
- Easy to enable/disable notification types
- Backend needs actual FlutterFlow page names to generate `ff_user_push_notifications` docs
- Template strings for title/body generation
- Easy to add new types without code changes

---

### ✅ 7-Day Auto-Delete Implementation

**Decision**: Daily scheduled Cloud Function cleanup

**Implementation**:
```python
# Runs daily via Cloud Scheduler
@functions_framework.cloud_event
def cleanup_old_notifications(cloud_event):
    seven_days_ago = datetime.now() - timedelta(days=7)

    # Collections to clean
    collections = [
        'notifications',
        'ff_user_push_notifications',
        'ff_push_notifications'
    ]

    for collection_name in collections:
        old_docs = db.collection(collection_name).where(
            'createdAt', '<', seven_days_ago
        ).stream()

        # Batch delete (Firestore limit: 500 per batch)
        batch = db.batch()
        count = 0
        for doc in old_docs:
            batch.delete(doc.reference)
            count += 1
            if count >= 500:
                batch.commit()
                batch = db.batch()
                count = 0

        if count > 0:
            batch.commit()
```

**What gets deleted**:
- `notifications/{id}` - In-app notifications (soft-deleted or not)
- `ff_user_push_notifications/{id}` - Push delivery jobs
- `ff_push_notifications/{id}` - Broadcast push notifications

**Schedule**: Daily (Cloud Scheduler cron job)

---

## Open Architecture Questions

### Badge Count Management

**Context**: App icon needs to show unread notification count badge. One account can manage multiple profiles, so badge count = total unread across ALL managed profiles.

**Option A: Query on-demand** (when app opens/foregrounds)
```python
def get_badge_count(account_id):
    managed_profiles = get_profiles_for_account(account_id)

    unread_count = db.collection('notifications').where(
        'receiverProfile', 'in', managed_profiles
    ).where('read', '==', False).where('deleted', '==', False
    ).count().get()

    return unread_count
```
- ✅ Always accurate
- ✅ Simple implementation
- ⚠️ Query on every app open

**Option B: Maintain counter in accounts collection**
```python
# accounts/{accountId}
{
  "unreadNotificationCount": 5  # Maintained by backend triggers
}

# Backend increments/decrements on notification create/read
```
- ✅ Fast (no query needed)
- ✅ Real-time sync via account listener
- ⚠️ Risk of count drift (if updates fail)
- ⚠️ Needs reconciliation function to fix drift

**Questions for Product Owner:**
1. Which approach - query on-demand (A) or maintain counter (B)?
2. If counter approach, acceptable to have occasional drift that gets reconciled?
3. Should badge count include ALL notifications or only push-enabled types?
4. What's the expected max number of profiles per account? (affects query performance)

---

## Design Spec Reference

Full design specification: `initiatives/_planning/notification-system.md`
- 470+ lines of comprehensive product requirements
- Business goals, success metrics, user workflows
- Three-phase scope breakdown
- Risk assessment and mitigation strategies
- Phase 1 = Mobile app (mystage-app) only, core social notifications

---

## Repository Context

**Affected Repositories:**
- `mystage-app` - FlutterFlow mobile app (iOS/Android)
- `mystage-app-backend` - Firebase Functions for backend logic
- `mystage-databases` - Firestore schema and security rules

**Existing Infrastructure:**
- Firebase Functions (30+ already deployed)
- Firestore (primary database)
- Firebase Auth
- FlutterFlow's push notification infrastructure (ready to use, but how much of it should we use?)
