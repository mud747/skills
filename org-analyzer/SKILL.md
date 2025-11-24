---
name: org-analyzer
description: Analyze and review Emacs Org-mode files for weekly reviews, time tracking analysis, and activity summaries. Use when the user asks to review activities, analyze time spent, summarize weeks or date ranges, break down time by category/tag, check habit consistency, or generate reports from org-mode todo, agenda, and journal files.
---

# Org-Mode Analyzer

## Overview

Analyze Emacs Org-mode files to generate weekly reviews, time analysis reports, and activity summaries. This skill provides workflows for parsing org-mode files, extracting clock entries, analyzing time spent by category, and summarizing completed tasks and meeting attendance.

## When to Use This Skill

Use this skill when the user requests:
- Weekly or date-range activity reviews (e.g., "review my activities for the last week")
- Time analysis and breakdowns (e.g., "how much time did I spend in meetings last week?")
- Time categorization by tags (e.g., "break down my time by work category")
- Habit tracking consistency checks
- Summary reports from org-mode files

## Core Workflows

### 1. Weekly Activity Review

Generate comprehensive text summaries of activities for a specified period.

**Process:**

1. **Determine date range**
   - Parse user request for date range (e.g., "last week", "this week", "Nov 11-17")
   - Calculate specific start and end dates
   - Consider that "last week" typically means the most recent complete week (Mon-Sun or similar)

2. **Read main org files**
   - Start with `agenda.org` for meetings and events with clock entries
   - Read `todo.org` for completed tasks and habit tracking
   - Check `refile.org` for recent captures if relevant
   - Only search archive files if specifically needed (they are very large - 174-265KB)

3. **Extract relevant entries**
   - Use Grep to find entries in the date range:
     - `SCHEDULED: <2025-11-[date-pattern]` for scheduled items
     - `CLOCK: \[2025-11-[date-pattern]` for clock entries
     - `\*\* DONE` for completed tasks in the date range
   - Parse `:LOGBOOK:` drawers to extract clock entries
   - Identify meetings by `:meeting:` tag
   - Find completed tasks with `DONE` state

4. **Analyze and categorize**
   - Extract clock durations from format: `CLOCK: [start]--[end] => duration`
   - Group activities by tags (`:work:AI:`, `:work:cloud:`, `:meeting:`, etc.)
   - Calculate total time spent per category
   - Identify habit tracking patterns
   - Note key highlights and patterns

5. **Generate summary report**
   Include:
   - **Meetings attended** - List with titles, dates, and durations from clock entries
   - **Completed tasks** - DONE items with descriptions and tags
   - **Habit consistency** - Which habits were tracked and how often
   - **Time breakdown** - Total clock time by category/tag
   - **Key highlights** - Notable patterns, heavy time investments, or achievements

**Example output structure:**
```
Weekly Review: Nov 11-17, 2025

MEETINGS (Total: 8:45)
- AI Strategy Session (Wed 10:00, 0:56) :work:AI:meeting:
- Cloud Architecture Review (Thu 14:00, 1:45) :work:cloud:meeting:
...

COMPLETED TASKS (12 items)
- [DONE] Complete GenAI investigation report :work:AI:
- [DONE] Review architecture governance docs :work:
...

HABIT TRACKING
- Learn: 5/7 days
- Plan/Review: 6/7 days
- Reading: 4/7 days

TIME BREAKDOWN BY CATEGORY
- Meetings: 8:45
- Work:AI: 12:30
- Work:Cloud: 6:15
- Learning: 3:20

KEY HIGHLIGHTS
- Heavy focus on AI initiatives (12:30 hours)
- Strong habit consistency for planning (6/7 days)
- 12 tasks completed
```

### 2. Time Analysis

Analyze time spent with detailed breakdowns by category, tag, or activity type.

**Process:**

1. **Clarify analysis parameters**
   - Date range (specific dates, last week, this week, last month)
   - Categorization method (by tag, by activity type, by project)
   - Granularity (summary totals vs. detailed breakdown)

2. **Extract all clock entries in range**
   - Use Grep to find all `CLOCK:` entries in date range
   - Parse each clock entry for start time, end time, and duration
   - Extract associated entry title and tags

3. **Categorize and aggregate**
   - Group by requested categorization:
     - **By tag**: Sum all time for `:work:AI:`, `:work:cloud:`, etc.
     - **By activity type**: Meetings vs. tasks vs. habits
     - **By entry**: Individual time per task/meeting
   - Calculate totals and percentages
   - Identify top time-consuming activities

4. **Generate analysis report**
   Format results clearly with:
   - Total time tracked
   - Breakdown by requested category
   - Top 5 or top 10 activities by time
   - Percentage distribution if useful
   - Comparisons if multiple categories

**Example queries and responses:**

Query: "How much time did I spend in meetings last week?"
- Extract all entries with `:meeting:` tag in date range
- Sum clock durations
- Report total with breakdown by individual meetings

Query: "Break down my time by tag for the last week"
- Group all clock entries by primary tags
- Calculate totals for each tag
- Present sorted by time spent

Query: "Show me clock time by work category"
- Extract entries with `:work:AI:`, `:work:cloud:`, `:work:innovation:` tags
- Aggregate by subcategory
- Report totals and percentages

### 3. Habit Tracking Analysis

Review consistency and patterns in habit tracking.

**Process:**

1. **Identify habit entries** in `todo.org`
   - Look for recurring items with repeaters (`.+1d` patterns)
   - Common habits: learn, plan/review, maintenance, reading

2. **Count completions** in date range
   - Find DONE state changes or clock entries for habits
   - Calculate completion rate (e.g., 5/7 days)

3. **Report consistency**
   - List each habit with completion rate
   - Identify strong vs. weak consistency
   - Note any patterns or trends

## Important Notes

### File Handling
- **Main files first**: Always check `todo.org` and `agenda.org` before archives
- **Archive files are large**: `todo.org_archive` (174KB), `agenda.org_archive` (265KB)
- Use targeted Grep searches with specific date patterns for archives
- Avoid reading entire archive files; use search and read with offset/limit

### Time Tracking
- **Clock entries are source of truth**: Use actual `CLOCK:` entries, not scheduled times
- **Parse LOGBOOK drawers**: Time tracking lives in `:LOGBOOK:` ... `:END:` blocks
- **Duration format**: Can be `H:MM` or `HH:MM`
- **Multiple clock entries**: Single entries can have multiple clock periods

### Tags and Categories
- Tags can be combined: `:work:AI:meeting:`
- Work categories: `:work:`, `:work:cloud:`, `:work:AI:`, `:work:innovation:`
- Event types: `:meeting:`, `:PHONE:`
- Personal: `:car:`, `:school:`

### Date Parsing
- Scheduled format: `<2025-11-18 Mon 09:00>`
- Clock format: `[2025-11-13 Thu 08:25]`
- Use regex patterns for date range searches: `2025-11-1[0-9]` for Nov 10-19

## Reference Files

### references/org-conventions.md
Comprehensive documentation of the user's org-mode system including:
- Complete file structure details
- Time tracking format specifications
- All tag definitions and combinations
- Task state workflows
- Search and grep patterns
- Best practices for parsing org files

Load this reference file when:
- Encountering unfamiliar org-mode syntax
- Needing detailed format specifications
- Searching for specific patterns
- Troubleshooting parsing issues

## Tips for Effective Analysis

1. **Be efficient with large files** - Use Grep before Read for targeted extraction
2. **Trust clock entries** - Actual time tracked is more accurate than scheduled time
3. **Aggregate systematically** - Parse all relevant entries before summarizing
4. **Provide context** - Include dates, tags, and categories in summaries
5. **Format clearly** - Use structured text with sections and clear labels
6. **Calculate accurately** - Sum durations correctly (watch H:MM vs. HH:MM format)
7. **Highlight insights** - Note patterns, heavy investments, and achievements
