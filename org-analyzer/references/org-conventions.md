# Org-Mode System Conventions

This document describes the structure, conventions, and patterns used in the user's Emacs Org-mode personal organization system.

## File Structure

### Core Files
- **todo.org** - Primary task management with TODO items, habits, and recurring tasks
- **agenda.org** - Calendar events, meetings, scheduled appointments with time tracking
- **refile.org** - Temporary capture location for quick notes and items to be refiled
- **notes.org** - Long-form notes, meeting notes, and reference material
- **journal.org** - Daily journal entries and reflections
- **projects.org** - Project-specific tracking (minimal content)

### Archive Files
- **todo.org_archive** - Completed tasks (174KB - large file, use search/grep carefully)
- **agenda.org_archive** - Past meetings and events (265KB - very large, use search/grep)

**Note:** Archive files are very large. Always prefer searching main files first. Use Grep with specific date ranges or keywords when searching archives.

## Time Tracking System

### Clock Entry Format
Time tracking uses `:LOGBOOK:` drawers with the following format:

```
:LOGBOOK:
CLOCK: [2025-11-13 Thu 08:25]--[2025-11-13 Thu 09:30] =>  1:05
CLOCK: [2025-11-13 Thu 10:00]--[2025-11-13 Thu 11:45] =>  1:45
:END:
```

### Parsing Clock Entries
- Clock format: `CLOCK: [start-timestamp]--[end-timestamp] => duration`
- Start/end timestamps: `[YYYY-MM-DD Day HH:MM]`
- Duration format: `H:MM` or `HH:MM`
- Multiple clock entries can exist in a single LOGBOOK drawer
- Active (running) clocks appear without end timestamp

### Time Summaries
- Org-mode clocktable syntax may be present
- Clocked time is the **source of truth** for time spent
- Scheduled time may differ from actual clocked time

## Date and Timestamp Formats

### Scheduled Dates
```
SCHEDULED: <2025-11-18 Mon 09:00>
SCHEDULED: <2025-11-18 Mon 09:00>--<2025-11-21 Thu 17:00>
```

### Date Ranges
```
<2025-11-18 Mon 09:00>--<2025-11-21 Thu 17:00>
```

### Logbook Timestamps
```
[2025-11-13 Thu 08:25]
```

## Tags System

### Work Categories
- `:work:` - General work items
- `:work:cloud:` - Cloud architecture and strategy
- `:work:AI:` - AI/GenAI initiatives and investigations
- `:work:innovation:` - Innovation projects

### Event Types
- `:meeting:` - Meetings
- `:PHONE:` - Phone calls

### Personal Categories
- `:car:` - Car-related tasks
- `:school:` - School-related items

### Tag Combinations
Tags can be combined (e.g., `:work:AI:` or `:work:cloud:meeting:`)

## Task States

- `TODO` - Pending task
- `WAITING` - Blocked task
- `DONE` - Completed task
- Items without state keywords are informational/notes

## Org Entry Structure

Typical meeting entry:
```
** DONE Meeting Title                                           :work:meeting:
   SCHEDULED: <2025-11-13 Wed 10:00-11:00>
   :LOGBOOK:
   CLOCK: [2025-11-13 Wed 10:02]--[2025-11-13 Wed 10:58] =>  0:56
   :END:

   Meeting notes go here...
```

Typical task entry:
```
** TODO Task description                                        :work:AI:
   SCHEDULED: <2025-11-18 Mon>

   Task details...
```

## Habits System

The system includes recurring habits tracked in todo.org:
- **learn** - Daily learning activities
- **plan/review** - Planning and review sessions
- **maintenance** - Regular maintenance tasks
- **reading** - Reading habits

Habits typically have `.+1d` style repeaters for daily tracking.

## Work Context

The user's professional focus areas:
- Cloud architecture and strategy work
- AI/GenAI initiatives and investigations
- IT governance and architecture
- Team leadership and meetings
- Technical learning and development
- Work-life balance tracking

## Search and Grep Patterns

When searching for specific information:

### Find entries in date range
```
SCHEDULED: <2025-11-1[0-9]
CLOCK: \[2025-11-1[0-9]
```

### Find by tag
```
:work:AI:
:meeting:
```

### Find by state
```
\*\* TODO
\*\* DONE
\*\* WAITING
```

### Find clock entries
```
CLOCK: \[
:LOGBOOK:
```

## Best Practices for Analysis

1. **Start with main files** - Check todo.org, agenda.org before archives
2. **Use date-specific searches** - Grep for specific date patterns to limit results
3. **Parse LOGBOOK drawers** - Extract clock entries for accurate time tracking
4. **Respect file sizes** - Archive files are 174-265KB, use targeted searches
5. **Trust clocked time** - Use CLOCK entries as source of truth, not scheduled times
6. **Aggregate by tags** - Group activities by tag combinations for categorization
7. **Check habit consistency** - Look for repeating patterns in todo.org
