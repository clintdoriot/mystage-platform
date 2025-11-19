# Extraction Improvements

## Status
🟡 Planning / 🟢 Active (ongoing)

## Description

Iterative improvements to extraction flow and prompts to improve data extraction accuracy from scraped content.

## Affected Repositories

- **mystage-event-sourcing** (extraction system)

## Purpose

Continuously improve the accuracy and quality of structured data extracted from scraped web pages.

## Key Areas

### 1. Extraction Flow Improvements
- Multi-stage extraction
- Validation and error detection
- Retry logic for failures
- Handling edge cases

### 2. Prompt Engineering
- Refine extraction prompts
- Add examples and context
- Improve structured output format
- Handle ambiguous data

### 3. Quality Assurance
- Extraction accuracy metrics
- Comparison with ground truth
- Error pattern analysis
- A/B testing of prompts

### 4. Feedback Loop
- Learn from admin corrections
- Incorporate manual fixes into prompts
- Track improvement over time

## Technical Approach

- LLM-based extraction (currently using pydantic-ai)
- Structured output with validation
- Iterative prompt refinement
- Deep evals for testing

## Dependencies

- Pydantic-ai update (in progress)
- Deep evals setup (in progress)
- Admin interface for data correction (provides feedback)

## Metrics to Track

- Extraction accuracy %
- Fields populated %
- Manual correction rate
- Extraction cost per page
- Processing time

## Estimated Effort

**Ongoing** - This is continuous improvement

Per iteration: 1-2 weeks
Measurement infrastructure: 1 week (if not done)

## Success Criteria

- Extraction accuracy > 90%
- Reduced manual correction needed
- Improved data quality
- Lower cost per extraction
- Faster extraction time

## Priority

High - Data quality is fundamental

## Notes

- This is ongoing work, not a one-time project
- Requires measurement infrastructure (deep evals)
- Benefits from admin feedback loop
- Consider A/B testing prompt changes
