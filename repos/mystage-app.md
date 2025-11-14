# MyStage App

## Overview

Primary mobile application for iOS and Android, built with FlutterFlow.

## Technology Stack

- **Platform**: FlutterFlow
- **Deployment**: iOS App Store, Google Play Store
- **Base**: Extends mystage-ff-base-lib

## Purpose

Primary consumer-facing application for fans to:
- Discover local music events
- Find artists and venues
- (Additional features to be documented)

## Development Process

- Built using FlutterFlow visual development platform
- Git is used as **backup only**, not primary development workflow
- Changes typically made through FlutterFlow interface

## Related Repositories

- **mystage-ff-base-lib** - Base FlutterFlow project this extends
- **mystage-app-backend** - Backend functions consumed by app
- **mystage-event-sourcing** - Source of event/artist/venue data
- **mystage-databases** - Direct database access

## Current Status

Active development. Needs better documentation and Claude tooling setup.

## Related Initiatives

- [Comprehensive Notification System](../initiatives/_planning/notification-system.md) - Phase 1 (in-app notification center, push notifications)
- [Chat System Integration](../initiatives/_planning/chat-integration.md) - Real-time messaging
- [Profile Onboarding Workflows](../initiatives/_planning/profile-onboarding.md) - Improved user onboarding

## Notes

- FlutterFlow-based means limited traditional git workflow
- Primary distribution channel for the platform
- Consumer of data from event-sourcing pipeline
