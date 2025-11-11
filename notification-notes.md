# Notification System Technical Brainstorming - Session Notes

**Date**: 2025-11-08
**Last Updated**: 2025-11-11
**Purpose**: Capture key technical constraints and decisions for the notification system architecture

---

## Session Summary

**Status**: 🟢 Core Architecture Complete - Ready for Remaining Topics

**Progress:**
- ✅ Push notification provider selected (FCM)
- ✅ Platform constraints documented (FlutterFlow, Account/Profile model)
- ✅ Storage architecture defined (dual collections with fan-out model)
- ✅ Notification creation pattern established (backend onCreate triggers with fan-out)
- ✅ Notifications collection schema finalized (account-centric)
- ✅ Deduplication strategy defined (per account)
- ✅ Cross-device sync mechanism chosen (Firestore real-time listeners)
- ✅ Deep linking configuration approach established (constants file)
- ✅ 7-day auto-delete implementation planned (scheduled Cloud Function)
- ✅ Badge count management - **decided: query on-demand**
- ✅ Fan-out architecture - **decided: create notification per account**

**Next Steps:**
1. Continue technical brainstorming to cover remaining topics:
   - Performance considerations (indexing strategy, query optimization)
   - Testing strategy (how to test push notifications)
   - Monitoring & alerting (metrics to track)
   - Rollout strategy (feature flags, gradual rollout)
   - Security considerations (authorization, PII handling)
2. Update design specification with complete technical architecture
3. Move to implementation planning phase

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

### ✅ Fan-Out Architecture
**Decision**: Create separate notification document for each account managing a profile

**Rationale**:
- **Query Performance**: Direct Firestore queries `where('receiverAccount', '==', accountRef)` are fast and indexable
- **Independent Read Status**: Each account can mark notifications read/unread independently
- **Badge Count Simplicity**: Simple query per account, no complex aggregation
- **Cross-Device Sync**: Firestore real-time listeners work naturally per account
- **Firestore Query Limitations**: Cannot efficiently query nested map fields (Option A would require client-side filtering)
- **Storage Cost**: Minimal (2-3x for multi-manager profiles, most profiles have 1 manager)
- **Scalability**: Indexed queries scale better than client-side filtering

**Trade-offs Accepted**:
- More storage (1 notification → N documents for N account managers)
- Write complexity (fan-out logic in onCreate triggers)
- Multiple deletes needed (N documents vs 1)

**Implementation Pattern**:
```python
# For a notification targeting a profile:
1. Get profile document → read managers list
2. For each account in managers list:
   - Create notification document with receiverAccount = that account
   - Each notification has independent read/unread status
   - Deduplication key includes accountId to prevent duplicates per account
```

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
- **Accounts** (`users/{accountId}`): Login credentials, device FCM tokens
- **Profiles** (`profiles/{profileId}`): Public-facing identities (artist, venue, fan)
- **Relationship**: Many-to-many via `profiles.managers` field
  - One Account can manage multiple Profiles
  - One Profile can be managed by multiple Accounts (stored as `managers: [accountRef1, accountRef2]`)

**Data Structure:**
```python
# profiles/{profileId}
{
  'name': 'The Rolling Stones',
  'managers': [
    ref('users/account1'),  # manager
    ref('users/account2'),  # guitarist
    ref('users/account3')   # drummer
  ],
  # ... other profile fields
}

# users/{accountId}/fcm_tokens/{tokenId}
{
  'token': 'fcm_device_token_string',
  'platform': 'ios',  # or 'android'
  'createdAt': timestamp
}
```

**Example:**
- Band Profile "The Rolling Stones" → `managers: [account1, account2, account3]`
- Each Account has multiple devices with FCM tokens stored in subcollection

**Notification Challenge:**
- Events are **profile-centric** (e.g., "Someone liked The Rolling Stones' post")
- Notifications must be **account-centric** (each account needs independent read status)
- FCM tokens are **account-centric** (stored under `users/{accountId}/fcm_tokens`)
- **Fan-out required**: 1 Profile Event → N Account Notifications → M Device Push Notifications

**Fan-Out Flow:**
1. Event occurs for Profile → Read `profile.managers` list
2. Create N notification documents (one per account in managers list)
3. Create push job(s) with all account refs
4. FlutterFlow queries FCM tokens for each account → delivers to M devices

**Note on FlutterFlow's "users":**
- FlutterFlow thinks of "users" as individuals with FCM tokens
- In MyStage, these are "Accounts"
- FCM tokens are stored under Accounts, NOT Profiles

---

## Two Parallel Requirements

From the design specification (`initiatives/_planning/notification-system.md`):

### 1. In-App Notification Center
- Persistent notification history (7-day retention)
- Browseable inbox with read/unread status
- Mark as read/unread, delete individual notifications
- Cross-device read status sync
- Profile images, timestamps, deep links
- Query: "Show me all notifications for my account" (`where('receiverAccount', '==', myAccountRef)`)

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
**Decision**: Dual storage with separate collections + fan-out model

**Collections:**
1. **`notifications/{notificationId}`** - In-app notification center (ACCOUNT-CENTRIC)
   - Purpose: Persistent storage for notification history
   - **Account-centric with fan-out**: One notification document per account
   - 7-day retention with auto-cleanup
   - Each account has independent read/unread status
   - Query pattern: `where('receiverAccount', '==', myAccountRef).where('deleted', '==', False)`
   - Fan-out: 1 profile event → N notification documents (N = number of managers)

2. **`ff_user_push_notifications/{pushId}`** - Push notification delivery
   - Purpose: Transient push delivery jobs
   - Account-centric (FCM tokens belong to accounts)
   - Triggers FlutterFlow's existing FCM delivery infrastructure
   - Contains comma-separated account refs for batch delivery
   - Status tracking (succeeded/failed, num_sent, error)
   - Typically 1 push job per profile (delivers to all manager accounts)

**Rationale:**
- Clean separation of concerns (persistent storage vs transient delivery)
- Leverage FlutterFlow's existing push delivery infrastructure
- In-app queries don't need to see push delivery metadata
- Account-centric model enables independent read status and efficient queries
- Fan-out at write time (onCreate trigger) = fast reads, simple queries

---

### ✅ Notification Creation Pattern
**Decision**: Backend onCreate triggers with fan-out (primary pattern)

**Architecture:**
```
User Action (like, comment, follow, mention, etc.)
  ↓
FlutterFlow writes to source collection (likes/, comments/, follows/, posts/)
  ↓
Backend onCreate trigger fires (onLikeCreated, onCommentCreated, etc.)
  ↓
Backend function:
  1. Identify target profile(s) affected by the action
  2. For each target profile:
     a. Read profile.managers to get list of account refs
     b. For each account in managers list:
        - Check deduplication (per account)
        - Create in-app notification with receiverAccount = that account
     c. If notification type configured for push:
        - Create push job with all account refs for this profile
  ↓
FlutterFlow's sendUserPushNotificationsTrigger fires (for each push job)
  ↓
FlutterFlow's delivery logic:
  - Parses comma-separated user_refs
  - For each account: queries fcm_tokens subcollection
  - Batches and sends to Firebase Cloud Messaging (up to 500 tokens)
  - Updates status fields (succeeded/failed, num_sent)
```

**Key Backend Triggers:**
- `onLikeCreated` - When someone likes a post
- `onCommentCreated` - When someone comments
- `onFollowCreated` - When someone follows
- `onDmCreated` - When someone sends a DM
- `onPostCreated` - When post contains mentions (@username)
- Auth triggers for account events (email verification, etc.)
- Scheduled functions for periodic notifications (profile completion prompts)

**Notification Type Configuration:**
- Code-based configuration (Phase 1)
- Each type specifies: enabled, usePush (true/false), title template, body template, deep link page
- Example: DMs/comments/replies/mentions use push, likes/follows are in-app only

**Fan-out Strategy:**
- Backend reads `profile.managers` array to get account refs
- **In-app notifications**: Create N separate documents (one per account)
- **Push notifications**: Create 1 push job per profile with comma-separated account refs
- FlutterFlow's existing triggers handle FCM token lookup and delivery to all devices
- Example: 1 Profile Event → 2 Manager Accounts → 2 In-App Notifications + 1 Push Job → 4 Device Push Notifications

**Example Fan-Out Flow:**
```python
@functions_framework.cloud_event
def on_post_created(cloud_event):
    post_doc = event.data.after.to_dict()

    # For each mentioned profile in the post
    for mentioned_profile_ref in post_doc.get('mentions', []):
        # Get profile document to read managers list
        profile_doc = mentioned_profile_ref.get()
        account_refs = profile_doc.get('managers', [])

        # Fan-out: Create notification for EACH account
        for account_ref in account_refs:
            dedupe_key = f"mention_{post_doc.id}_{post_doc['authorProfile'].id}_{account_ref.id}"
            existing = db.collection('notifications').where('dedupeKey', '==', dedupe_key).limit(1).get()
            if not existing:
                db.collection('notifications').add({
                    'receiverAccount': account_ref,
                    'receiverProfile': mentioned_profile_ref,
                    'type': 'mention',
                    'dedupeKey': dedupe_key,
                    'read': False,
                    # ... other fields
                })

        # Create ONE push job for all accounts of this profile
        if NOTIFICATION_TYPES['mention']['usePush']:
            db.collection('ff_user_push_notifications').add({
                'notification_title': f"{author_name} mentioned {profile_name}",
                'notification_text': post_doc['content'][:100],
                'initial_page_name': 'PostDetailPage',
                'parameter_data': json.dumps({'postId': post_doc.id}),
                'user_refs': ','.join([ref.path for ref in account_refs])
            })
```

**FlutterFlow Team Workflow:**
- Like button → Firestore Action: Create Document in `likes/` collection
- Comment button → Firestore Action: Create Document in `comments/` collection
- Follow button → Firestore Action: Create Document in `follows/` collection
- Post with mentions → Firestore Action: Create Document in `posts/` collection
- **No custom notification logic needed in frontend** - backend handles everything

**Fallback for Ad-hoc Notifications:**
- Callable Cloud Function `createNotification` for notifications not tied to onCreate triggers
- Frontend or other backend functions can call directly
- Use cases: onboarding messages, periodic prompts, admin-initiated notifications

**Rationale:**
- **Reliability**: Notifications guaranteed to be created (not dependent on frontend completing)
- **Security**: Backend enforces rules, frontend can't fake notifications
- **Consistency**: Works from app, admin interface, APIs, future integrations
- **FlutterFlow simplicity**: Team just creates core data, backend handles fan-out
- **Future-proof**: Easy to add new notification types without frontend changes
- **Independent read status**: Each account manages their own notification state

---

---

## Detailed Technical Decisions

### ✅ Notifications Collection Schema

**Collection**: `notifications/{notificationId}` (ACCOUNT-CENTRIC with FAN-OUT)

**Schema** (Python/Firestore):
```python
{
  # Identity (ACCOUNT-CENTRIC)
  "id": str,                             # Auto-generated document ID
  "receiverAccount": DocumentReference,  # THIS account (primary query field)
  "receiverProfile": DocumentReference,  # Profile that was targeted (context)

  # Type & Content
  "type": str,                        # "like", "comment", "follow", "dm", "mention", etc.
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

  # State management (PER ACCOUNT)
  "read": bool,                       # Read/unread status for THIS account (default: False)
  "deleted": bool,                    # Soft delete flag for THIS account (default: False)
  "createdAt": firestore.SERVER_TIMESTAMP,
  "readAt": firestore.SERVER_TIMESTAMP | None,

  # Push notification tracking
  "hasPush": bool,                    # Whether this notification type uses push

  # Deduplication (PER ACCOUNT)
  "dedupeKey": str,                   # Includes accountId: "type_entity_source_accountId"
}
```

**Key Decisions:**
- **Account-centric**: `receiverAccount` is the primary field (one document per account)
- **Fan-out model**: Same event creates N documents (one per managing account)
- Use DocumentReferences for all profile/account relationships (not string IDs)
- **Independent state**: Each account has their own `read`, `deleted`, `readAt` fields
- Soft delete with `deleted: bool`, hard delete after 7 days via scheduled cleanup
- Type-specific `dedupeKey` includes `accountId`: `"type_{entityId}_{sourceId}_{accountId}"`
- `receiverProfile` provides context (which profile was targeted) but isn't the query field

**Fan-Out Example:**
- Event: User X likes Profile A's post
- Profile A has managers: [Account 1, Account 2]
- Result: 2 notification documents created:
  - `{receiverAccount: ref('users/account1'), receiverProfile: ref('profiles/profileA'), ...}`
  - `{receiverAccount: ref('users/account2'), receiverProfile: ref('profiles/profileA'), ...}`

**Indexes Required:**
- `receiverAccount + createdAt` (descending) - Main query: "all notifications for my account"
- `receiverAccount + read` - Badge count: "unread notifications for my account"
- `dedupeKey` - Deduplication queries (per account)
- `createdAt` - Cleanup queries (7-day auto-delete)

---

### ✅ Deduplication Strategy

**Decision**: Skip creating duplicate notifications per account

**Implementation**:
```python
# Deduplication includes accountId - prevents duplicate per account
dedupe_key = f"{type}_{entity_id}_{source_id}_{account_id}"

existing = db.collection('notifications').where(
    'dedupeKey', '==', dedupe_key
).limit(1).get()

if existing:
    # Skip creating duplicate for THIS account
    return
```

**Deduplication Key Format**:
- General format: `"type_{entityId}_{sourceId}_{accountId}"`
- **MUST include accountId** since we fan out per account
- Exact format defined when implementing each notification type
- Examples:
  - Like: `"like_{postId}_{sourceProfileId}_{accountId}"`
  - Follow: `"follow_{sourceProfileId}_{accountId}"`
  - Comment: `"comment_{postId}_{sourceProfileId}_{accountId}"`
  - Mention: `"mention_{postId}_{sourceProfileId}_{accountId}"`

**Why AccountId in Dedupe Key:**
- Each account gets their own notification document
- Same event creates N notifications (one per manager)
- Dedupe prevents duplicate notifications **per account**, not globally
- Example: If User X likes Profile A's post twice:
  - First like → creates 2 notifications (one for each manager)
  - Second like → skipped (dedupe key exists for each account)

**Note**: Not overly concerned with deduplication complexity in Phase 1. Will refine as needed.

---

### ✅ Cross-Device Sync Mechanism

**Decision**: Firestore Real-Time Listeners (Phase 1)

**Implementation**:
```python
# Backend: Update read status for THIS account's notification
notification_ref.update({
    'read': True,
    'readAt': firestore.SERVER_TIMESTAMP
})

# Frontend: Real-time listener on all devices for THIS account
db.collection('notifications')
  .where('receiverAccount', '==', myAccountRef)
  .where('deleted', '==', False)
  .orderBy('createdAt', 'desc')
  .snapshots()  # Real-time updates across all devices for this account
```

**How It Works:**
- Account 1 marks notification as read on their iPhone
- Update written to Firestore: `notifications/{docId}.read = true`
- Account 1's iPad listener receives update → UI updates instantly
- Account 2's devices see NO change (different notification document)

**Rationale**:
- Built into Firestore, automatic sync across devices
- Account-centric queries are simple and fast
- Each account's read status is independent (as required)
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

### ✅ Badge Count Management

**Decision**: Query on-demand (when app opens/foregrounds)

**Implementation**:
```python
# Simple query - account-centric model makes this fast
def get_badge_count(account_ref):
    unread_count = db.collection('notifications')\
        .where('receiverAccount', '==', account_ref)\
        .where('read', '==', False)\
        .where('deleted', '==', False)\
        .count().get()

    return unread_count
```

**When to Update Badge:**
- App opens or foregrounds
- Real-time listener detects notification changes
- After marking notifications as read

**Rationale**:
- ✅ Always accurate (no drift)
- ✅ Simple implementation (no counter to maintain)
- ✅ Account-centric query is fast and indexed
- ✅ No reconciliation logic needed
- ✅ No risk of count getting out of sync
- ⚠️ Small query cost on app open (acceptable for Phase 1)

**Badge Count Includes:**
- All notifications (both push-enabled and in-app only)
- Account sees total unread count across all profiles they manage

**Optimization (Future):**
- If query cost becomes concern, can add counter with reconciliation
- For Phase 1, query approach is simpler and more reliable

---

---

## Complete Fan-Out Flow Example

**Scenario**: User X mentions two bands in a post
- Profile A (Rolling Stones) has managers: [Account 1, Account 2]
- Profile B (Beatles) has managers: [Account 3, Account 4]

### Step 1: User Creates Post
```python
post = {
  'content': 'Check out @TheRollingStones and @TheBeatles!',
  'authorProfile': ref('profiles/userX'),
  'mentions': [
    ref('profiles/profileA'),  # Rolling Stones
    ref('profiles/profileB')   # Beatles
  ]
}
# Written to posts/ collection by FlutterFlow
```

### Step 2: Backend Trigger Fires
```python
@functions_framework.cloud_event
def on_post_created(cloud_event):
    post_doc = event.data.after.to_dict()

    # For each mentioned profile
    for profile_ref in post_doc.get('mentions', []):
        profile_doc = profile_ref.get()
        account_refs = profile_doc.get('managers', [])

        # Fan-out: Create notification for each account
        for account_ref in account_refs:
            # ... create notification (see below)

        # Create push job for all accounts of this profile
        # ... create push job (see below)
```

### Step 3: In-App Notifications Created (4 total)
```python
# Notification 1: Account 1 (Rolling Stones manager)
{
  'receiverAccount': ref('users/account1'),
  'receiverProfile': ref('profiles/profileA'),
  'type': 'mention',
  'title': 'User X mentioned The Rolling Stones',
  'body': 'Check out @TheRollingStones and @TheBeatles!',
  'read': False,
  'dedupeKey': 'mention_post123_userX_account1',
  'hasPush': True,
  # ... other fields
}

# Notification 2: Account 2 (Rolling Stones guitarist)
{
  'receiverAccount': ref('users/account2'),
  'receiverProfile': ref('profiles/profileA'),
  'type': 'mention',
  'title': 'User X mentioned The Rolling Stones',
  'body': 'Check out @TheRollingStones and @TheBeatles!',
  'read': False,
  'dedupeKey': 'mention_post123_userX_account2',
  'hasPush': True,
  # ... other fields
}

# Notification 3: Account 3 (Beatles manager)
{
  'receiverAccount': ref('users/account3'),
  'receiverProfile': ref('profiles/profileB'),
  'type': 'mention',
  'title': 'User X mentioned The Beatles',
  'body': 'Check out @TheRollingStones and @TheBeatles!',
  'read': False,
  'dedupeKey': 'mention_post123_userX_account3',
  'hasPush': True,
  # ... other fields
}

# Notification 4: Account 4 (Beatles bassist)
{
  'receiverAccount': ref('users/account4'),
  'receiverProfile': ref('profiles/profileB'),
  'type': 'mention',
  'title': 'User X mentioned The Beatles',
  'body': 'Check out @TheRollingStones and @TheBeatles!',
  'read': False,
  'dedupeKey': 'mention_post123_userX_account4',
  'hasPush': True,
  # ... other fields
}
```

### Step 4: Push Jobs Created (2 total)
```python
# Push Job 1: Rolling Stones profile (delivers to accounts 1 & 2)
{
  'notification_title': 'User X mentioned The Rolling Stones',
  'notification_text': 'Check out @TheRollingStones and @TheBeatles!',
  'initial_page_name': 'PostDetailPage',
  'parameter_data': '{"postId": "post123"}',
  'user_refs': 'users/account1,users/account2',
  'status': 'pending',
  'createdAt': timestamp
}

# Push Job 2: Beatles profile (delivers to accounts 3 & 4)
{
  'notification_title': 'User X mentioned The Beatles',
  'notification_text': 'Check out @TheRollingStones and @TheBeatles!',
  'initial_page_name': 'PostDetailPage',
  'parameter_data': '{"postId": "post123"}',
  'user_refs': 'users/account3,users/account4',
  'status': 'pending',
  'createdAt': timestamp
}
```

### Step 5: FlutterFlow Delivers Push Notifications
```python
# For Push Job 1:
- Parse user_refs → [account1, account2]
- Query users/account1/fcm_tokens → [iPhone, iPad]
- Query users/account2/fcm_tokens → [Android]
- Send to FCM (3 devices)

# For Push Job 2:
- Parse user_refs → [account3, account4]
- Query users/account3/fcm_tokens → [iPhone]
- Query users/account4/fcm_tokens → [Android, Tablet]
- Send to FCM (3 devices)

# Total: 6 push notifications delivered
```

### Step 6: User Interaction
```python
# Account 1 opens app on iPhone
- Queries: where('receiverAccount', '==', account1)
- Sees: 1 unread notification (about Rolling Stones)
- Badge count: 1

# Account 1 marks notification as read on iPhone
- Updates: notifications/{notif1}.read = true
- All Account 1 devices (iPhone, iPad) sync instantly
- Account 2 sees NO change (different notification document)

# Account 3 opens app on iPhone
- Queries: where('receiverAccount', '==', account3)
- Sees: 1 unread notification (about Beatles)
- Badge count: 1
```

### Summary
- **1 Post** with 2 mentions
- **2 Profiles** mentioned
- **4 Accounts** managing those profiles
- **4 In-App Notifications** created (one per account)
- **2 Push Jobs** created (one per profile)
- **6 Push Notifications** delivered (to all devices)
- **Independent read status** (Account 1 marks read ≠ Account 2 marks read)

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
- FlutterFlow's push notification infrastructure (leveraged for delivery)
