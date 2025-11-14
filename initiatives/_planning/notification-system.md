# Comprehensive Notification System

**Status**: 🟡 Planning - Design Phase Complete
**Created**: 2025-11-08
**Last Updated**: 2025-11-08
**Priority**: High
**Phase**: Design Specification

## Business Context

### Problem Statement

Users are not currently aware of social interactions and important updates within the MyStage platform, leading to missed engagement opportunities and reduced retention. Without notifications, users must manually check the app to discover new followers, comments, likes, content from favorite artists, and other activities - creating friction that reduces overall platform engagement.

### Business Goals

- **Increase user engagement**: Drive more frequent app opens and session activity
- **Improve retention**: Keep users coming back through timely, relevant notifications
- **Enable social interactions**: Alert users when others engage with their content, creating reciprocal engagement loops
- **Reduce notification fatigue**: Build a system that respects user attention and prevents spam

### Success Metrics

**Primary Metrics:**
1. **Session frequency increase** - Users opening app more often (tracked pre/post launch)
2. **30-day retention rate** - Long-term user retention improvement
3. **Notification disable rate** - Health metric (lower is better, indicates quality notifications)

**Secondary Metrics:**
- Click-through rate on notifications
- Time to respond to social interactions (DMs, comments)
- % of notifications marked as read
- User-to-user interaction increase (comments, follows, likes)

### Target Users

- **Primary Users**: All MyStage app users (fans, artists, venues)
- **Secondary Users**: Platform administrators (Phase 2)
- **Stakeholders**: Product team, engineering, user experience designers

### Business Impact

**Expected Outcomes:**
- Higher daily active users through timely engagement prompts
- Increased social interaction volume (2-way engagement loops)
- Improved user satisfaction through awareness of platform activity
- Foundation for future features (chat, community, NFTs, etc.)

**User Value:**
- Stay informed about favorite artists' activities (shows, releases, content)
- Quick response path for social interactions
- Never miss important updates or engagement opportunities
- Control over notification preferences

## Product Requirements

### Functional Requirements

#### In-App Notification Center

**What it does:**
Provides a dedicated inbox for all user notifications within the mystage-app, accessible via bell icon with unread badge count.

**User value:**
Central location to review all activity and updates, organized chronologically with clear read/unread status.

**Must have:**
- Bell icon in app navigation with unread count badge
- Dedicated notifications screen/tab
- 7-day notification history
- Mark as read/unread functionality
- Delete individual notifications
- Profile image/avatar for each notification
- Timestamp display (relative format: "5m ago", "2h ago")
- Unread highlight bar or indicator
- Deep link to specific content when tapped
- Auto-delete notifications after 7 days

**Nice to have:**
- Quick actions directly from notification (Like, Reply, View)
- Swipe gestures (swipe to delete, swipe to mark read)
- Pull to refresh

#### Push Notifications

**What it does:**
Delivers notifications to user's device even when app is closed, with configurable enable/disable per notification type.

**User value:**
Real-time awareness of important activities without needing to open the app constantly.

**Must have:**
- Push notification infrastructure (Firebase Cloud Messaging or similar)
- Deep linking from push notification to specific in-app page
- Badge count on app icon
- Push notifications also appear in notification center (not push-only)
- Global push on/off toggle in settings
- System-level notification permissions handling
- Configurable per notification type in code (which types use push vs in-app only)

**Nice to have:**
- Rich notifications with images/thumbnails
- Notification grouping at OS level (if supported)

#### Cross-Device Sync

**What it does:**
Synchronizes notification read status across all user devices (multiple phones/tablets).

**User value:**
Mark notification as read on one device, it's read everywhere - prevents duplicate work.

**Must have:**
- Real-time sync of read/unread status
- Delivery to all registered user devices
- Badge count sync across devices

#### Deduplication

**What it does:**
Prevents duplicate notifications if user already has an unread notification of the same type from the same source.

**User value:**
Reduces notification spam and fatigue.

**Must have:**
- Check for existing unread notification before creating new one
- If duplicate exists, don't create new notification (or update timestamp of existing)
- Applies to same notification type + same source (e.g., same user liking same post)

### User Experience Requirements

**Key User Workflows:**

1. **Social Engagement Response**
   - User starts from: Receives push notification "John liked your post"
   - User needs to: Quickly view the post and engage back (like John's content, comment, view profile)
   - Expected outcome: Deep link to the specific post, quick actions available

2. **Content Discovery from Followed Artists**
   - User starts from: Notification "Favorite Artist announced a new show" (Phase 2)
   - User needs to: View show details, RSVP, share with friends
   - Expected outcome: Deep link to show page, easy path to action

3. **Notification Management**
   - User starts from: Notification center with 15 unread notifications
   - User needs to: Review notifications, mark important ones as read, delete irrelevant ones
   - Expected outcome: Easy swipe actions, bulk actions, clear visual hierarchy

4. **Controlling Notification Preferences**
   - User starts from: App settings
   - User needs to: Disable push notifications globally (Phase 1) or by type (Phase 2)
   - Expected outcome: Simple toggle switches, immediate effect

**Platform Touchpoints:**
- ✅ Mobile app (mystage-app - iOS/Android)
- ❌ Web applications (Phase 2+)
- ❌ Admin interface (Phase 2)

**Accessibility & Usability:**
- Clear visual hierarchy (unread vs read)
- Timestamps in human-readable format
- Profile images for social context
- Deep links must work reliably (no broken links)
- Performance: Notification center loads instantly (<500ms)
- Handle offline mode gracefully (queue notifications, sync when online)

### Data Requirements

**What data do users need?**
- Notification type (follow, like, comment, etc.)
- Source user information (name, profile image, user ID)
- Target content information (which post, which comment, etc.)
- Timestamp (when notification was created)
- Read/unread status
- Deep link URL to specific content
- Optional: image/thumbnail associated with notification

**What data do users create/modify?**
- Read/unread status changes
- Notification deletion
- Notification preferences (enable/disable push)
- Device push tokens (for delivery)

### External Dependencies

**Third-Party Services:**
- **Firebase Cloud Messaging** (or similar) - Push notification delivery infrastructure
  - Why needed: Industry-standard push notification delivery to iOS/Android

**External APIs:**
- None required for Phase 1

**Other Dependencies:**
- **Firestore**: Notification storage, preferences, delivery status
- **mystage-app**: Integration points for notification center UI
- **Existing social features**: Follower relationships, posts, comments, likes (assumes these exist)

## Scope & Phasing

### Phase 1: Core Social Media Notifications (MVP)

**Platform:**
- mystage-app (mobile iOS/Android) only

**Notification Types:**

*Social Engagement (All Profile Types):*
- Someone followed you
- Someone liked your post/content
- Someone commented on your post
- Someone replied to your comment
- Someone mentioned you (@username)
- Someone shared your content
- Someone tagged you in a post/photo
- New direct message received
- Engagement milestones (100 followers, 1000 likes, etc.)

*Account & System:*
- Welcome to MyStage (onboarding)
- Password changed / Login from new device (security)
- Email verified
- Complete your profile prompts

**Capabilities:**
- In-app notification center with 7-day history
- Push notification infrastructure (selective about which types use push)
- Deep linking to specific pages
- Quick actions from notifications
- Swipe to delete/mark read
- Cross-device read sync
- Global push on/off toggle
- Deduplication (prevent duplicate unread notifications)
- Auto-delete after 7 days
- All notifications enabled by default (opt-out model)

**Push Strategy Phase 1:**
- Push-enabled: DMs, comments, replies, mentions (high engagement)
- In-app only: likes, follows, milestones (lower urgency)
- Configurable in code per notification type

**Out of Scope Phase 1:**
- Email delivery
- Per-notification-type controls (coming Phase 2)
- Notification bundling/grouping
- Web apps (fanex, pro-dashboard)
- Admin notifications
- Quiet hours / Do Not Disturb
- Frequency limits

---

### Phase 2: Music Industry Features + Advanced Controls

**Platform Expansion:**
- Add mystage-admin-interface support

**Notification Types Added:**

*Artist/Band Content Updates:*
- Favorite artist announced a new show
- Favorite artist released album/single
- Favorite artist posted new content
- Tickets available for followed artist's show
- Show you're attending has updates (time/lineup change, cancellation)
- Show selling out soon

*Venue Updates:*
- Favorite venue announced new event
- Venue posted new content/announcement

*Artist/Venue Business:*
- New follower (for artists/venues)
- Fan RSVP'd to your show
- Tip received
- Ticket sales milestones
- Profile claimed/verified
- Event data updated
- New review/rating received

*Admin/Moderation:*
- Content flagged for review
- Policy violation detected
- Pipeline failures (event-sourcing)
- Data quality issues
- System performance alerts
- Profile claim reviewed/approved/rejected
- User blocked/unblocked
- User banned from event

**Capabilities Added:**
- Per-notification-type controls (granular or grouped categories)
- Separate in-app vs push delivery preferences
- Manual push notifications from artists/venues (rate-limited: once per month)
- Notification history/archive beyond 7 days
- Quiet hours / Do Not Disturb (if validated as needed)

---

### Phase 3: Future Enhancements

**NFT & Merch (Dependent on Other Initiatives):**
- Artist dropped NFT collection
- NFT sold/purchased
- Merch drop notifications
- Merch order confirmations

**Advanced Features:**
- Artist going live (streaming)
- Collaboration requests
- Booking inquiries
- Email delivery channel (optional, may use external CRM instead)
- SMS notifications (if validated as needed)
- Notification bundling/grouping ("5 people liked your post")
- Advanced analytics milestones
- Email digest notifications (weekly summary)

**Extensibility for Future Initiatives:**
- System designed to easily add new notification types
- Plugin architecture for new delivery channels
- Template system for notification content

## Risks & Considerations

### Major Risks

**🔴 Notification Spam/Fatigue (MAJOR CONCERN)**
- **Risk**: Users overwhelmed with too many notifications, leading to disabling all notifications or app uninstall
- **Impact**: High - defeats entire purpose of notification system
- **Mitigation**:
  - Conservative Phase 1 push strategy (only high-value notifications)
  - Deduplication to prevent duplicate notifications
  - Track "disable rate" as key success metric
  - Monitor click-through rates to identify low-value notifications
  - 7-day auto-delete prevents cluttered inbox
  - Phase 2: Add granular per-type controls based on user feedback
  - Code-level configuration to quickly disable problematic notification types
  - Consider rate limiting per user (max notifications per hour/day)

### Moderate Risks

**🟡 Privacy Concerns**
- **Risk**: Notifications revealing sensitive information or enabling stalking behavior
- **Impact**: Medium - standard social media privacy considerations
- **Mitigation**:
  - Follow industry-standard social media privacy patterns
  - Don't notify for passive actions (profile views, searches)
  - User controls to disable notification types
  - Future: Block/mute functionality to prevent harassment

**🟡 Abuse/Harassment**
- **Risk**: Users spam others with notifications (mass following, comment spam)
- **Impact**: Medium - can degrade user experience
- **Mitigation**:
  - Rely on existing content moderation systems
  - Deduplication helps reduce spam impact
  - Admin notifications for policy violations
  - Future: Rate limiting, abuse detection patterns

### Low Risks

**🟢 Performance/Scale**
- **Risk**: System can't handle notification volume as platform grows
- **Impact**: Low - not expecting massive scale initially
- **Mitigation**:
  - Use proven infrastructure (Firebase, Firestore)
  - Monitor performance metrics
  - Optimize as platform grows

**🟢 Push Delivery Failures**
- **Risk**: Users don't receive push notifications due to infrastructure issues
- **Impact**: Low - acceptable failure rate for Phase 1
- **Mitigation**:
  - Best-effort delivery approach
  - All notifications stored in-app regardless of push success
  - Users can always check notification center

### Compliance & Legal

- **Privacy**: Comply with GDPR, CCPA (user control over notifications, data deletion)
- **Data Retention**: 7-day auto-delete aligns with data minimization principles
- **User Consent**: Push notifications require OS-level permission (iOS/Android handle this)
- **Spam Prevention**: Rate limiting on manual artist push notifications (Phase 2)

## Priority & Timeline

### Priority Justification

**Priority Level**: High

This initiative is ready to begin work now and is sufficiently high priority to start development immediately. The notification system is foundational infrastructure that enables social engagement and user retention - core to the platform's success.

### Time Sensitivity

- **Deadline**: None specified
- **Business driver**: Enable social engagement features, improve retention metrics

### Dependencies on Other Initiatives

**Blocks:**
- No initiatives are currently blocked by this (notifications enhance but don't block other work)

**Blocked by:**
- None - sufficient existing systems are in place to begin implementation

**Related:**
- Event Sourcing: Will eventually integrate for data-driven notifications (Phase 2+)
- Chat System: Will integrate with notification system once both are ready
- Social Features: Assumes basic social graph (followers, posts, comments) already exists

**Integration Points (Future):**
- Various systems will need to integrate with notifications once infrastructure exists
- Individual notification type implementations can be prioritized separately from core infrastructure

## Next Steps

### Immediate Next Steps

- [x] Design specification complete
- [ ] Technical brainstorming session (add architecture requirements)
  - Run: `/initiative-brainstorm-technical notification-system`
- [ ] Implementation planning (break down into phases and tasks)
  - Run: `/initiative-plan notification-system`
- [ ] Effort estimation (detailed breakdown by phase)
- [ ] Approval & prioritization confirmation

### Post-Planning Next Steps

- [ ] Review complete initiative (design + technical + plan)
- [ ] Merge PR to main
- [ ] Create GitHub issues
  - Run: `/initiative-create-issues notification-system`

## Open Questions

### Design Questions

- [ ] **Push notification triggers**: For Phase 1 social notifications, should all be immediate or some batched? (Defer to technical session)
- [ ] **Notification copy/templates**: Who writes notification text? Product team or hardcoded by engineers?
- [ ] **Images in notifications**: Required for all types or optional? Source from user profile images or separate notification images?
- [ ] **Quick actions**: Which notification types support inline actions vs just deep links?
- [ ] **Onboarding**: Should we educate users about notifications during first-run experience?

### Business Questions

- [ ] **Success metrics baseline**: What are current session frequency and 30-day retention rates (to measure improvement)?
- [ ] **Phase 1 timeline**: When does this need to launch? What's driving urgency?
- [ ] **Resource allocation**: How many engineers dedicated to this initiative?
- [ ] **Testing approach**: Beta test with subset of users before full rollout?
- [ ] **Artist manual notifications (Phase 2)**: How to prevent abuse of once-per-month limit?

### Technical Questions (For Technical Brainstorming Session)

- [ ] Firebase Cloud Messaging vs alternatives?
- [ ] Firestore schema design for notifications collection
- [ ] Real-time vs batched delivery architecture
- [ ] Deduplication implementation strategy
- [ ] Cross-device sync mechanism
- [ ] Deep linking URL structure and routing
- [ ] Notification service architecture (Cloud Functions? Backend service?)
- [ ] Integration points with mystage-app
- [ ] Testing strategy for push notifications
- [ ] Monitoring and alerting for notification delivery

---

## Technical Architecture

**Added**: 2025-11-11 - Technical Brainstorming Phase

### Affected Repositories

#### Primary Repositories

- **mystage-app-backend**: Backend notification logic (Firebase Functions)
  - Files/areas affected:
    - New functions for onCreate triggers (onLikeCreated, onCommentCreated, etc.)
    - Notification configuration file (notification_config.py)
    - Utility functions for fan-out and deduplication
    - Daily cleanup function for 7-day auto-delete
  - Type of work: New features (notification creation, delivery orchestration)

- **mystage-databases**: Database schema and security rules
  - Files/areas affected:
    - New Firestore collection: `notifications/`
    - Existing collection modified: `profiles/` (assumes managers field exists)
    - Leverage existing: `ff_user_push_notifications/`, `users/{uid}/fcm_tokens/`
    - New indexes for notification queries
    - Security rules for notification access
  - Type of work: Schema design, index creation, security rules

- **mystage-app**: Mobile app UI integration (FlutterFlow)
  - Files/areas affected:
    - Notification center screen/page
    - Bell icon with badge count in navigation
    - Deep linking configuration
    - Real-time Firestore listeners for notifications
    - Push notification permission handling
  - Type of work: New features (notification center UI, deep linking)

#### Secondary Repositories

- **mystage-platform**: Documentation updates
  - Architecture documentation (data flow, integration patterns)
  - Initiative tracking and effort estimates

### Integration Points

#### Database Integration

**Database**: Firestore (primary database)

**Collections**:

1. **`notifications/{notificationId}`** - In-app notification storage (ACCOUNT-CENTRIC)
   - **Operations**: Create (backend), Read (frontend), Update (mark read/delete), Delete (cleanup function)
   - **Schema Changes**: New collection (see Data Architecture section)
   - **Access Pattern**:
     - Backend creates notifications via onCreate triggers
     - Frontend queries: `where('receiverAccount', '==', myAccountRef).where('deleted', '==', false)`
     - Real-time listeners for cross-device sync

2. **`ff_user_push_notifications/{pushId}`** - Push notification delivery jobs (EXISTING - FlutterFlow)
   - **Operations**: Create (backend)
   - **Schema Changes**: None (uses existing FlutterFlow collection)
   - **Access Pattern**: Backend creates push job → FlutterFlow onCreate trigger delivers to FCM

3. **`profiles/{profileId}`** - Profile data (EXISTING)
   - **Operations**: Read (backend needs to read `managers` field)
   - **Schema Changes**: None (assumes `managers: [accountRef1, accountRef2]` field exists)
   - **Access Pattern**: Backend reads `profile.managers` to determine fan-out

4. **`users/{accountId}/fcm_tokens/{tokenId}`** - FCM device tokens (EXISTING - FlutterFlow)
   - **Operations**: Read (by FlutterFlow's push delivery function)
   - **Schema Changes**: None
   - **Access Pattern**: FlutterFlow queries tokens for push delivery

#### Event Integration

**Events Published**: None (notification system responds to events, doesn't publish)

**Events Consumed**:
- **onCreate triggers** for source collections (Phase 1 only):
  - `reactions/{reactionId}` → onReactionCreated (for likes: when reaction == "liked")
  - `comments/{commentId}` → onCommentCreated (for comments and replies)
  - `profile_relationships/{relationshipId}` → onProfileRelationshipCreated (for follows: when following == true)
  - `posts/{postId}` → onPostCreated (for mentions: parse post content for @mentions)
  - `chats/{chatId}/messages/{messageId}` → onMessageCreated (for DMs)
  - Note: Auth events (email verification, password change) deferred to Phase 2

**Message Queue**: Cloud Scheduler for daily cleanup (not Cloud Tasks/Pub/Sub)

#### External Services

- **Firebase Cloud Messaging (FCM)**
  - Purpose: Push notification delivery to iOS/Android devices
  - Integration method: Via FlutterFlow's existing push notification infrastructure
  - Access: Backend writes to `ff_user_push_notifications/`, FlutterFlow handles FCM delivery

- **FlutterFlow Push Infrastructure** (EXISTING)
  - Purpose: Manages FCM tokens and handles push delivery logic
  - Integration method: Backend creates push job documents, FlutterFlow triggers handle delivery
  - Components:
    - `sendUserPushNotificationsTrigger` - onCreate trigger for push jobs
    - `sendPushNotifications` - Core delivery logic (batches up to 500 tokens)
    - `addFcmToken` - Registers device FCM tokens

### Data Architecture

#### Data Models

```typescript
// Notification (in-app storage) - ACCOUNT-CENTRIC with FAN-OUT
interface Notification {
  id: string;                          // Auto-generated document ID
  receiverAccount: DocumentReference;  // THIS account (primary query field)
  receiverProfile: DocumentReference;  // Profile that was targeted (context)

  // Type & Content
  type: string;                        // "like", "comment", "follow", "dm", "mention", etc.
  title: string;                       // "John Doe liked your post"
  body: string;                        // Additional details
  imageUrl: string | null;             // Profile image or content thumbnail

  // Source context
  sourceAccount: DocumentReference | null;  // Account that triggered (if applicable)
  sourceProfile: DocumentReference | null;  // Profile that triggered (if applicable)
  targetEntityId: string | null;       // The post/comment/etc being acted on
  targetEntityType: string | null;     // "post", "comment", "profile", etc.

  // Deep linking
  deepLinkPage: string;                // FlutterFlow page name
  deepLinkParams: Record<string, any>; // JSON params for navigation

  // State management (PER ACCOUNT)
  read: boolean;                       // Read/unread status for THIS account
  deleted: boolean;                    // Soft delete flag for THIS account
  createdAt: Timestamp;
  readAt: Timestamp | null;

  // Push notification tracking
  hasPush: boolean;                    // Whether this notification type uses push

  // Deduplication (PER ACCOUNT)
  dedupeKey: string;                   // "type_{entityId}_{sourceId}_{accountId}"
}

// Push Notification Job (delivery) - Uses existing FlutterFlow schema
interface PushNotificationJob {
  notification_title: string;
  notification_text: string;
  notification_image_url?: string;
  initial_page_name?: string;          // Deep link page
  parameter_data?: string;             // JSON string of params
  user_refs: string;                   // Comma-separated account paths
  scheduled_time?: Timestamp;
  status?: string;                     // "succeeded" or "failed" (output)
  num_sent?: number;                   // (output)
  error?: string;                      // (output)
}

// Notification Type Configuration (backend config file)
interface NotificationTypeConfig {
  enabled: boolean;
  usePush: boolean;                    // Push + in-app vs in-app only
  titleTemplate: string;               // "{sourceProfile.name} liked your post"
  bodyTemplate: string;
  deepLinkPage: string;                // FlutterFlow page name
  deepLinkParamKeys: string[];         // ["postId", "commentId"]
}
```

#### Database Schema

**Collection: `notifications/{notificationId}` (NEW)**

Purpose: Persistent in-app notification storage with account-centric fan-out

Fields:
- `id` (string, auto-generated)
- `receiverAccount` (DocumentReference) - Primary query field
- `receiverProfile` (DocumentReference) - Context (which profile was targeted)
- `type` (string) - Notification type
- `title` (string) - Display title
- `body` (string) - Display body
- `imageUrl` (string, nullable)
- `sourceAccount` (DocumentReference, nullable)
- `sourceProfile` (DocumentReference, nullable)
- `targetEntityId` (string, nullable)
- `targetEntityType` (string, nullable)
- `deepLinkPage` (string)
- `deepLinkParams` (map)
- `read` (boolean, default false)
- `deleted` (boolean, default false)
- `createdAt` (timestamp)
- `readAt` (timestamp, nullable)
- `hasPush` (boolean)
- `dedupeKey` (string)

Indexes Required:
- `receiverAccount + createdAt` (descending) - Main query: "all notifications for my account"
- `receiverAccount + read` - Badge count: "unread notifications for my account"
- `dedupeKey` - Deduplication queries (per account)
- `createdAt` - Cleanup queries (7-day auto-delete)

Relationships:
- `receiverAccount` → `users/{accountId}` (who sees this notification)
- `receiverProfile` → `profiles/{profileId}` (which profile was targeted)
- `sourceAccount` → `users/{accountId}` (who triggered the notification)
- `sourceProfile` → `profiles/{profileId}` (which profile triggered it)

**Collection: `ff_user_push_notifications/{pushId}` (EXISTING - FlutterFlow)**

Purpose: Transient push delivery jobs

No changes needed - uses existing FlutterFlow schema

**Collection: `profiles/{profileId}` (EXISTING)**

Purpose: Profile data (assumes `managers` field exists)

Relevant Fields:
- `managers` (array of DocumentReferences) - Accounts that manage this profile

**Subcollection: `users/{accountId}/fcm_tokens/{tokenId}` (EXISTING - FlutterFlow)**

Purpose: FCM device tokens for push delivery

No changes needed - managed by FlutterFlow

#### Data Flow

**Flow 1: Notification Creation (Fan-Out Pattern)**

1. User action occurs (like, comment, follow, mention, etc.)
2. FlutterFlow writes to source collection (`likes/`, `comments/`, `posts/`, etc.)
3. Backend onCreate trigger fires (`onLikeCreated`, `onCommentCreated`, etc.)
4. Backend function:
   - Identifies target profile(s) affected by the action
   - For each target profile:
     - Reads `profile.managers` to get list of account refs
     - For each account in managers list:
       - Checks deduplication (per account): `where('dedupeKey', '==', dedupe_key).limit(1)`
       - If not duplicate: Creates in-app notification with `receiverAccount` = that account
     - If notification type configured for push (`usePush: true`):
       - Creates push job with all account refs for this profile
5. FlutterFlow's `sendUserPushNotificationsTrigger` fires (for each push job)
6. FlutterFlow's delivery logic:
   - Parses comma-separated `user_refs`
   - For each account: queries `users/{accountId}/fcm_tokens/` subcollection
   - Batches and sends to Firebase Cloud Messaging (up to 500 tokens per batch)
   - Updates push job status fields (`succeeded`/`failed`, `num_sent`)

**Flow 2: Notification Center Query (Real-Time)**

1. User opens app on any device
2. Frontend establishes Firestore listener:
   ```
   db.collection('notifications')
     .where('receiverAccount', '==', myAccountRef)
     .where('deleted', '==', false)
     .orderBy('createdAt', 'desc')
     .snapshots()
   ```
3. Real-time updates sync across all devices for this account
4. Badge count query (on-demand): count where `read == false`

**Flow 3: Mark Notification as Read (Cross-Device Sync)**

1. User marks notification as read on Device A
2. Frontend updates Firestore:
   ```
   notification_ref.update({
     read: true,
     readAt: serverTimestamp()
   })
   ```
3. Real-time listener on Device B (same account) receives update → UI updates
4. Other accounts (different managers of same profile) see NO change (different notification document)

**Flow 4: 7-Day Auto-Delete**

1. Cloud Scheduler triggers daily cleanup function
2. Function queries: `where('createdAt', '<', sevenDaysAgo)`
3. Batch deletes old notifications from:
   - `notifications/` collection
   - `ff_user_push_notifications/` collection (push delivery jobs)
   - `ff_push_notifications/` collection (broadcast notifications)

#### Complete Fan-Out Example

**Scenario**: User X mentions two bands in a post
- Profile A (Rolling Stones) has managers: [Account 1, Account 2]
- Profile B (Beatles) has managers: [Account 3, Account 4]

**Step 1: User Creates Post**
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

**Step 2: Backend Trigger Fires**
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

**Step 3: In-App Notifications Created (4 total)**
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

**Step 4: Push Jobs Created (2 total)**
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

**Step 5: FlutterFlow Delivers Push Notifications**
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

**Step 6: User Interaction**
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

**Summary of Fan-Out Flow:**
- **1 Post** with 2 mentions
- **2 Profiles** mentioned
- **4 Accounts** managing those profiles
- **4 In-App Notifications** created (one per account)
- **2 Push Jobs** created (one per profile)
- **6 Push Notifications** delivered (to all devices)
- **Independent read status** (Account 1 marks read ≠ Account 2 marks read)

#### Data Migration

- **Migration needed?**: No
- **Migration strategy**: N/A (new feature, no existing data)
- **Rollback plan**: Delete `notifications/` collection if rollback needed (no data dependencies)

### Technical Dependencies

#### Initiative Dependencies

- **Blocks**: None (notifications enhance but don't block other work)
- **Blocked by**: None (sufficient existing systems in place)
- **Coordination required**:
  - Chat System (future): Will need DM notification integration
  - Event Sourcing (future): May provide alternative event triggers

#### Technology Dependencies

**New libraries**: None (uses existing Firebase SDK, FlutterFlow libraries)

**New services**:
- Firebase Cloud Messaging (FCM) - Already available in Firebase/GCP, not yet integrated
- Cloud Scheduler - Already available in GCP, used for daily cleanup function

**Infrastructure**:
- Firebase Functions (existing) - For onCreate triggers and cleanup function
- Firestore (existing) - For notification storage
- Cloud Scheduler (new usage) - For daily cleanup cron job

#### Cross-Repository Dependencies

- **mystage-app-backend depends on mystage-databases**: Backend functions need notification schema deployed first
- **mystage-app depends on mystage-app-backend**: App needs backend functions deployed before testing
- **mystage-databases → mystage-app-backend → mystage-app**: Deployment order

### Implementation Approach

#### Architectural Decisions

**Decision 1: Fan-Out Architecture (Create notification per account)**

- **Rationale**:
  - Query performance: Direct Firestore queries are fast and indexable
  - Independent read status: Each account manages their own notification state
  - Badge count simplicity: Simple query per account, no complex aggregation
  - Cross-device sync: Firestore real-time listeners work naturally per account
- **Alternatives considered**:
  - Single notification + read status map: Rejected due to Firestore query limitations (can't efficiently query nested map fields)
- **Trade-offs**:
  - ✅ Pros: Fast queries, independent state, simple implementation
  - ⚠️ Cons: More storage (2-3x for multi-manager profiles), write complexity (fan-out logic)

**Decision 2: Leverage FlutterFlow's Push Infrastructure**

- **Rationale**:
  - Already exists and handles FCM token management
  - Proven delivery logic (batching, error handling)
  - Reduces implementation scope
- **Alternatives considered**:
  - Build custom push delivery: Rejected as unnecessary duplication
- **Trade-offs**:
  - ✅ Pros: Faster implementation, proven infrastructure
  - ⚠️ Cons: Tied to FlutterFlow's schema and behavior

**Decision 3: Backend onCreate Triggers (Primary Pattern)**

- **Rationale**:
  - Reliability: Notifications guaranteed to be created (not dependent on frontend)
  - Security: Backend enforces rules, frontend can't fake notifications
  - Consistency: Works from app, admin interface, APIs, future integrations
- **Alternatives considered**:
  - Frontend creates notifications directly: Rejected due to security and reliability concerns
- **Trade-offs**:
  - ✅ Pros: Reliable, secure, consistent, future-proof
  - ⚠️ Cons: Requires backend functions for each notification type

**Decision 4: Query On-Demand Badge Count**

- **Rationale**:
  - Always accurate (no drift)
  - Simple implementation (no counter to maintain)
  - Account-centric query is fast and indexed
- **Alternatives considered**:
  - Maintain counter in accounts collection: Rejected due to drift risk and reconciliation complexity
- **Trade-offs**:
  - ✅ Pros: Accurate, simple, no reconciliation logic
  - ⚠️ Cons: Small query cost on app open (acceptable for Phase 1)

#### Technology Choices

- **Firebase Cloud Messaging (FCM)**: Industry standard, integrated with Firebase ecosystem
- **Firestore Real-Time Listeners**: Built-in cross-device sync, no additional infrastructure
- **onCreate Triggers**: Reliable event-driven architecture pattern
- **Cloud Scheduler**: Simple, cost-effective for daily cleanup cron job

#### Phasing Strategy (Technical)

**Phase 1: Foundation (Weeks 1-2)**
- Define Firestore schema for `notifications/` collection
- Create indexes and security rules
- Implement notification configuration file (notification_config.py)
- Deploy schema to Firestore

**Phase 2: Backend Implementation (Weeks 3-5)**
- Implement onCreate triggers for Phase 1 notification types:
  - onLikeCreated, onCommentCreated, onFollowCreated
  - onPostCreated (mentions), onDmCreated
  - Auth triggers (email verification, password change)
- Implement fan-out logic (read profile.managers, create notifications per account)
- Implement deduplication logic
- Implement push job creation (write to ff_user_push_notifications/)
- Implement daily cleanup function (Cloud Scheduler)
- Unit tests for backend functions

**Phase 3: Frontend Integration (Weeks 6-8)**
- Implement notification center UI in mystage-app (FlutterFlow):
  - Bell icon with badge count
  - Notification list screen
  - Real-time Firestore listener
  - Mark as read/unread, delete actions
  - Swipe gestures
- Implement deep linking configuration
- Implement push notification permissions handling
- Badge count query and display
- End-to-end testing

**Phase 4: Testing & Launch (Week 9)**
- Integration testing (notification creation → delivery → UI)
- Push notification testing on iOS/Android
- Performance testing (query speed, badge count, real-time sync)
- Security review (Firestore rules, auth)
- Gradual rollout (feature flag or percentage-based)

### Performance Considerations

#### Performance Requirements

- **Response time**:
  - Notification center load: <500ms (per design spec)
  - Badge count query: <200ms
  - Mark as read: <100ms
- **Throughput**:
  - onCreate triggers: handle burst of notifications (e.g., viral post)
  - Push delivery: FlutterFlow batches up to 500 tokens per batch
- **Data volume**:
  - Expected: ~100-1000 notifications per user per month (Phase 1)
  - Storage: ~1-2KB per notification
  - 7-day retention limits growth

#### Scaling Strategy

- **Firestore queries**: Indexed queries scale well (receiverAccount + createdAt)
- **onCreate triggers**: Firebase Functions auto-scale based on event volume
- **Push delivery**: FlutterFlow batches tokens (up to 500 per batch)
- **Storage growth**: Controlled by 7-day auto-delete (max 7 days of notifications per user)

#### Optimization Opportunities

- **Badge count caching**: If query cost becomes concern, add counter with reconciliation (Phase 2)
- **Query optimization**: Monitor slow queries, add composite indexes as needed
- **Background processing**: onCreate triggers already async, no additional optimization needed
- **Read status sync**: Real-time listeners are efficient (Firestore only sends deltas)

### Security Architecture

#### Authentication

- **User authentication**: Existing Firebase Auth (no changes needed)
- **Token management**: Existing FCM token management via FlutterFlow (no changes needed)

#### Authorization

- **Permission model**: Account-centric (users can only access their own notifications)
- **Access control**: Firestore security rules:
  ```javascript
  match /notifications/{notificationId} {
    // Users can read their own notifications
    allow read: if request.auth.uid == resource.data.receiverAccount.id;

    // Users can update their own notifications (mark read, delete)
    allow update: if request.auth.uid == resource.data.receiverAccount.id
                  && request.resource.data.diff(resource.data).affectedKeys()
                     .hasOnly(['read', 'readAt', 'deleted']);

    // Only backend can create notifications
    allow create: if false; // Backend uses admin SDK
  }
  ```

#### Data Protection

- **Encryption at rest/in transit**: Firestore default (TLS in transit, encrypted at rest)
- **PII handling**:
  - Notification content may contain user names, profile images (not sensitive PII)
  - No email addresses, phone numbers, or payment info in notifications
- **Data retention**: 7-day auto-delete aligns with data minimization principles

### Technical Risks

#### High Risk

**Risk: Notification Spam/Fatigue**
- **Impact**: Users overwhelmed with notifications → disable all notifications or uninstall app
- **Likelihood**: Medium-High (major concern per design spec)
- **Mitigation**:
  - Conservative Phase 1 push strategy (only DMs, comments, replies, mentions)
  - Deduplication prevents duplicate notifications per account
  - Code-level configuration to quickly disable notification types
  - Monitor "disable rate" metric
- **Contingency**:
  - Feature flag to disable specific notification types
  - Rate limiting per user (max notifications per hour/day)

**Risk: Fan-Out Write Amplification**
- **Impact**: High Firestore write costs if profiles have many managers
- **Likelihood**: Low (most profiles have 1 manager, only bands/venues have multiple)
- **Mitigation**:
  - Monitor write costs
  - Most profiles have 1 manager (fans, solo artists) = no amplification
  - Bands/venues typically 2-3 managers = 2-3x writes
- **Contingency**:
  - If costs become issue, add rate limiting per profile
  - Consider batching notifications for non-urgent types

#### Medium Risk

**Risk: Push Delivery Failures**
- **Impact**: Users don't receive push notifications
- **Likelihood**: Low (FCM is reliable)
- **Mitigation**:
  - Best-effort delivery approach (acceptable failure rate)
  - All notifications stored in-app regardless of push success
  - Users can always check notification center
- **Contingency**: Monitor FCM delivery success rate, investigate failures

**Risk: Deep Link Failures**
- **Impact**: Tapping notification doesn't navigate to correct page
- **Likelihood**: Medium (FlutterFlow deep linking can be finicky)
- **Mitigation**:
  - Thorough testing of deep links for all notification types
  - Fallback to notification center if deep link fails
- **Contingency**: Fix deep linking configuration in FlutterFlow

#### Low Risk

**Risk: Cross-Device Sync Delays**
- **Impact**: Notification marked read on one device, still shows unread on another device
- **Likelihood**: Low (Firestore real-time listeners are fast)
- **Mitigation**: Monitor sync latency, investigate if > 1 second
- **Contingency**: Acceptable delay (not critical)

### Testing Strategy

#### Unit Testing

**Backend functions to test:**
- Notification creation logic (fan-out, deduplication)
- Push job creation
- Deduplication logic (per account)
- Cleanup function (7-day auto-delete)

**Key test scenarios:**
- Single profile, single manager (1 notification created)
- Single profile, multiple managers (N notifications created)
- Multiple profiles mentioned (fan-out across profiles)
- Duplicate notification attempt (deduplication works)
- Cleanup function (old notifications deleted)

#### Integration Testing

**Integrations to test:**
- onCreate triggers → notification creation
- Notification creation → push job creation
- Push job creation → FCM delivery (FlutterFlow)
- Real-time listeners → cross-device sync

**Test environments needed:**
- Development Firestore database
- Test Firebase project with FCM
- Test devices (iOS, Android) for push testing

#### End-to-End Testing

**Key user workflows to test:**
1. User A likes User B's post → User B receives notification + push
2. User A mentions Band C (2 managers) → Both managers receive notifications + push
3. User B marks notification as read on iPhone → iPad shows read instantly
4. User B deletes notification → notification disappears on all devices
5. User B disables push notifications → still receives in-app notifications

**Test data requirements:**
- Test accounts with multiple devices (iOS, Android)
- Test profiles with multiple managers (bands, venues)
- Test social actions (likes, comments, follows, mentions)

### Deployment Strategy

#### Deployment Steps

1. **Deploy Firestore schema** (mystage-databases):
   - Deploy `notifications/` collection schema
   - Deploy indexes
   - Deploy security rules
   - Verify in Firebase console

2. **Deploy backend functions** (mystage-app-backend):
   - Deploy onCreate triggers (onLikeCreated, etc.)
   - Deploy notification creation functions
   - Deploy cleanup function
   - Configure Cloud Scheduler for daily cleanup

3. **Deploy mobile app** (mystage-app):
   - Deploy notification center UI
   - Deploy deep linking configuration
   - Deploy push notification permissions handling
   - Deploy to TestFlight/Play Store beta

4. **Test end-to-end**:
   - Create test notifications
   - Verify push delivery (iOS, Android)
   - Verify cross-device sync
   - Verify deep linking works

5. **Gradual rollout**:
   - Enable for 10% of users (via feature flag or Firebase Remote Config)
   - Monitor metrics (session frequency, disable rate, errors)
   - Increase to 50%, then 100%

#### Feature Flags

- **Global notification toggle**: Enable/disable entire notification system
- **Per-type toggles**: Enable/disable specific notification types (Phase 2)
- **Push notification toggle**: Enable/disable push (in-app always enabled)

#### Rollback Plan

- **If notification system fails**:
  - Disable onCreate triggers (stop creating notifications)
  - Keep in-app notification center (users can still see existing notifications)
  - Investigate and fix, then re-enable

- **If push delivery fails**:
  - Disable push job creation (stop writing to ff_user_push_notifications/)
  - Keep in-app notifications (users can still see notifications in-app)
  - Investigate FCM issues, then re-enable

- **Data preservation**:
  - Existing notifications in `notifications/` collection are preserved
  - 7-day auto-delete continues (no manual cleanup needed)

### Monitoring & Observability

#### Metrics to Track

- **Notification creation rate**: Notifications created per minute (by type)
  - Why important: Detect spam, monitor growth
- **Push delivery success rate**: % of pushes successfully delivered
  - Why important: Ensure push infrastructure is working
- **Notification disable rate**: % of users who disable push notifications
  - Why important: Key health metric (lower is better, indicates quality)
- **Click-through rate**: % of notifications tapped
  - Why important: Identify low-value notification types
- **Badge count accuracy**: Badge count matches actual unread count
  - Why important: Ensure query-based badge count is performant
- **Query performance**: P50/P95/P99 latency for notification queries
  - Why important: Ensure <500ms notification center load time
- **Firestore read/write costs**: Cost per notification created
  - Why important: Monitor fan-out write amplification

#### Logging Requirements

**What to log:**
- Notification creation events (type, receiver, source)
- Push job creation events
- FCM delivery results (success/failure)
- Cleanup function execution (notifications deleted)
- Errors (trigger failures, FCM errors, query timeouts)

**Log levels:**
- INFO: Notification created, push sent
- WARN: FCM delivery failure, duplicate notification skipped
- ERROR: Trigger failure, Firestore write failure, query timeout

**Retention**: 30 days (standard Firebase Functions logs)

#### Alerts

**Alert conditions:**
- **onCreate trigger failure rate > 5%**: Backend function errors
  - Who gets notified: Engineering team (PagerDuty)
- **Push delivery success rate < 90%**: FCM delivery issues
  - Who gets notified: Engineering team (Slack)
- **Notification query latency > 1s (P95)**: Performance degradation
  - Who gets notified: Engineering team (Slack)
- **Notification disable rate > 20%**: Spam/fatigue issues
  - Who gets notified: Product team (Email)
- **Cleanup function failures**: Daily cleanup not running
  - Who gets notified: Engineering team (Slack)

### Technical Questions - RESOLVED

**All technical questions resolved during brainstorming session (2025-11-11):**

- ✅ **FlutterFlow page names**: Use spec'd names (PostDetailPage, ProfilePage, ChatThreadPage, etc.). Store in backend constants file (`notification_config.py`) for easy updates. FlutterFlow team will create/rename pages to match during implementation.

- ✅ **Existing social collections**: Confirmed all necessary collections exist:
  - `reactions/{reactionId}` - Post likes (reaction == "liked"), event bookmarks, reports
    - Document ID format: `{profileId}-{contentCollection}-{contentDocument}`
    - Backend processor: `appReactionsProcessor`
  - `profile_relationships/{relationshipId}` - Follows and blocks
    - Fields: `following` (bool), `blocking` (bool)
    - References: `profile` (follower), `target_profile` (followee)
    - Backend processor: `appProfileRelationshipsProcessor`
  - `comments/{commentId}` - Post comments with reply support
    - Fields: `root_id` (top-level parent), `parent_id` (direct parent)
    - Backend processor: `comments.py`
  - `posts/{postId}` - Social posts (can contain mentions)
  - `chats/{chatId}/messages/{messageId}` - Direct messages with reply support
    - Fields: `root_message` (top-level parent), `referenced_message` (direct parent)

- ✅ **Profile.managers field**: EXISTS in schema. Confirmed in firestore.rules with authorization checks throughout subcollections. Format: Array of DocumentReferences to accounts.

- ✅ **FCM token registration**: FlutterFlow manages FCM infrastructure entirely:
  - Collections (`ff_user_push_notifications/`, `ff_push_notifications/`, `users/{uid}/fcm_tokens/`) created by FlutterFlow
  - Functions (`sendUserPushNotificationsTrigger`, `sendPushNotifications`) deployed by FlutterFlow
  - No security rules needed (backend functions use admin SDK)
  - **Action required**: Configure FlutterFlow push notifications on Dev and Prod environments (1 setup task)

- ✅ **Cloud Scheduler pricing**: Negligible cost (few cents/month in Cloud Run execution costs). Free to schedule, only pay for function execution time.

- ✅ **Firestore database**: Use `main` database (same as users, profiles, posts, etc.). Simpler queries, single database connection, easier to join with user/profile data.

- ✅ **Testing strategy**: Use both approaches:
  - **Firebase Emulator Suite** for unit tests (fast, isolated, runs in CI/CD)
  - **Dev Firestore** for integration/E2E tests (tests real infrastructure, FlutterFlow push delivery, FCM)

- ✅ **Rollout strategy**: No feature flags needed. Full rollout to all users (low user count, acceptable risk). Can add code-based kill switches if needed later.

### Phase 1 Scope Refinement

**High Priority Notification Types (Push-enabled):**
- DMs (direct messages)
- Comments on posts
- Replies to comments
- Mentions in posts

**Lower Priority Notification Types (In-app only):**
- Likes on posts
- Follows

**Deferred to Phase 2:**
- Shares
- Tags
- Engagement milestones (100 followers, etc.)
- Account/System notifications (welcome, password changed, email verified, etc.)

---

## Document History

- **2025-11-08** - Complete design specification created (replaced rough draft)
  - Business context and problem statement defined
  - Comprehensive notification type inventory
  - Product requirements and user workflows documented
  - Three-phase scope breakdown finalized
  - Risk assessment and mitigation strategies identified
  - Success metrics and priorities established

- **2025-11-11** - Technical architecture added (technical brainstorming phase)
  - Repository impact analysis (mystage-app-backend, mystage-databases, mystage-app)
  - Integration points and data flow documented
  - Account-centric fan-out architecture defined
  - Firestore schema design with indexes
  - Technical dependencies and risks identified
  - Implementation phasing strategy (9 weeks)
  - Security, performance, and monitoring considerations
  - Testing strategy and deployment plan
  - All open technical questions resolved through infrastructure investigation
  - Confirmed existing collections (reactions/, profile_relationships/, comments/, posts/, chats/messages/)
  - Validated profiles.managers field exists
  - Clarified FlutterFlow push infrastructure (managed by FlutterFlow, setup task needed)
  - Phase 1 scope refined: 6 notification types (DMs, comments, replies, mentions, likes, follows)
