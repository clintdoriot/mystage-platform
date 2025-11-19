# Profile Onboarding Workflows

## Status
🟡 Planning

## Description

Improved onboarding workflows for different user types with specialized profiles.

## Affected Repositories

- **mystage-app** (mobile onboarding)
- **mystage-ff-pro-dashboard** (professional onboarding)
- **mystage-app-backend** (onboarding logic)
- **mystage-admin-interface** (approval workflows)
- **mystage-databases** (profile data)

## User Types & Workflows

### 1. Festival Vendors
**Need**: Specialized profile for vendors selling at festivals
**Features**:
- Vendor profile creation
- Festival association
- Product/service listings
- Payment integration

### 2. Artists/Venues Connected to Sticker Collections
**Need**: Connect artists/venues to their NFT sticker collections
**Features**:
- Claim NFT collection
- Verify ownership
- Manage collection details
- Link to profile

### 3. Industry Profiles for NFT Sticker Creation
**Need**: Verified industry professionals who can create/mint NFT stickers
**Features**:
- Identity verification
- Permission management
- Minting capabilities
- Revenue/royalty setup

## Key Components

### Profile Types & Permissions
- Define profile type taxonomy
- Permission system for NFT creation
- Verification workflows

### Onboarding Flows
- Step-by-step profile creation
- Document upload for verification
- Admin approval workflows

### Verification System
- Identity verification (for NFT creators)
- Ownership verification (for collections)
- Manual review process

## Dependencies

- Profile claim management (existing initiative)
- Admin interface: Approval workflows
- NFT system: Integration with sticker creation
- Role-based access control in admin interface

## Related Initiatives

- [NFT Architecture](nft-architecture.md)
- [Admin Interface: Roles & Access](admin-roles-access.md)
- [Profile Claim Management](profile-claim-management.md)

## Technical Challenges

- Identity verification (KYC-lite?)
- Fraud prevention
- Scalable approval workflow
- Permission propagation across systems

## Estimated Effort

(TBD - depends on verification requirements and NFT system)

## Success Criteria

- Smooth onboarding for all user types
- Clear verification process
- Admin team can efficiently review/approve
- Secure permission management for NFT creation
- Users can complete onboarding without support

## Priority

Medium-High - Blocks NFT feature rollout

## Notes

- May need legal review for creator permissions
- Consider third-party identity verification services
- Start with manual approval, automate later
