---
name: ai-check
description: Automatically detects AI writing patterns and produces cleaned copy with AI tells removed, followed by an explanation of what was changed. Scans for AI tells—generic phrasing, stock openers, formal transitions, correlative constructions, vague authority claims, and other patterns—then outputs the revised text first and technical details second. Auto-triggers when generating, editing, reviewing, or polishing any written content for Every.
---

# AI Check

## Overview

This skill identifies common linguistic patterns that signal AI-generated writing—what the industry calls "AI tells"—and suggests more natural, human alternatives. It draws on comprehensive lexicons of phrases, structures, and vocabulary that language models overuse, organized by category, severity, and rationale.

**Workflow:** This skill outputs cleaned copy FIRST (with AI tells already removed), then explains what was changed and why. This ensures the writer gets immediately usable text before diving into the technical details of the fixes.

**Important:** When Claude generates new copy (tweets, emails, articles, etc.), this skill automatically runs in the background. The user will receive cleaned copy without AI tells, followed by an explanation of what patterns were avoided or removed.

## When This Skill Auto-Triggers

This skill automatically activates when:
- **Generating any written content** – tweets, social posts, emails, articles, essays, marketing copy, or any other text
- Reviewing or editing any Every essay, article, or written content
- Polishing drafts for publication
- Checking prose for authenticity and human voice
- Working with any text that will be published under the Every brand

## Core Detection Categories

### 1. Generic Phrasing
Identifies overused connective phrases and hedges that add no substance:
- "It's worth noting that..."
- "It's important to understand..."
- "At the end of the day..."
- "The fact of the matter is..."
- "In today's world..."

### 2. Stock Openers
Catches formulaic sentence beginnings that signal AI generation:
- "In the ever-evolving landscape of..."
- "In an era where..."
- "In recent years..."
- "As we navigate..."
- "In the realm of..."

### 3. Formal Transitions
Spots unnecessarily formal or academic transitions:
- "Furthermore..."
- "Moreover..."
- "Nevertheless..."
- "Consequently..."
- "Thus..."

### 4. Correlative Constructions
Identifies balanced parallel structures that feel mechanical:
- "Not only X, but also Y"
- "Both X and Y"
- "On one hand... on the other hand..."

### 5. Vague Authority Claims
Catches unsubstantiated authority phrases:
- "Studies show..."
- "Research indicates..."
- "Experts agree..."
- "It is widely known..."
- "Common wisdom suggests..."

### 6. Hedging Language
Identifies excessive qualification and uncertainty:
- "It could be argued..."
- "One might say..."
- "To some extent..."
- "It seems that..."
- "It appears..."

### 7. Buzzword Overload
Detects overuse of trendy business/tech jargon:
- "Leverage"
- "Synergy"
- "Paradigm shift"
- "Game-changer"
- "Disruptive"
- "Ecosystem"

### 8. Repetitive Sentence Structure
Identifies monotonous sentence patterns and suggests variation in:
- Length (short, medium, long)
- Type (declarative, interrogative, exclamatory)
- Opening words (avoid starting multiple sentences with the same word)

## Workflow

1. **Scan Input**: Analyze the provided text for AI tells across all categories
2. **Clean First**: Output the revised text with AI tells removed, maintaining the original meaning and flow
3. **Explain Second**: Provide a clear breakdown of:
   - What patterns were found
   - How they were fixed
   - Why the changes improve readability and authenticity
4. **Suggest Alternatives**: When appropriate, offer multiple ways to rephrase problematic sections

## Output Format

### Cleaned Text
[Provide the complete revised text here, with all AI tells removed]

---

### Changes Made

**Category: [Category Name]**
- **Original**: "[problematic phrase]"
- **Revised**: "[improved version]"
- **Rationale**: [Brief explanation of why this improves the text]

[Repeat for each significant change]

### Summary
[Brief overview of the main improvements and any remaining recommendations]

## Guidelines

- **Preserve voice and intent**: Never change the meaning or core message
- **Maintain natural flow**: Ensure revisions sound conversational, not stilted
- **Context matters**: Some formal language is appropriate in certain contexts (academic writing, legal documents)
- **Don't over-correct**: Not every instance of these patterns is problematic—use judgment
- **Prioritize clarity**: If removing a pattern hurts clarity, keep it and explain why

## Example

**Original**:
"In today's rapidly evolving digital landscape, it's important to understand that leveraging AI tools can be a game-changer for businesses. Moreover, studies show that companies that embrace this paradigm shift see significant improvements. It's worth noting that this transformation requires both technical expertise and strategic vision."

**Cleaned Version**:
"AI tools fundamentally change how businesses operate. Companies that adopt them early see measurable improvements in efficiency and output. But successful adoption requires technical skill and clear strategy."

**Changes Made**:

**Category: Stock Openers**
- **Original**: "In today's rapidly evolving digital landscape"
- **Revised**: [Removed]
- **Rationale**: Generic opener adds no information

**Category: Generic Phrasing**
- **Original**: "it's important to understand that"
- **Revised**: [Removed]
- **Rationale**: Unnecessary hedge that weakens the statement

**Category: Buzzword Overload**
- **Original**: "leveraging AI tools can be a game-changer"
- **Revised**: "AI tools fundamentally change"
- **Rationale**: Replaced jargon with clear, direct language

**Category: Formal Transitions**
- **Original**: "Moreover, studies show that"
- **Revised**: "Companies that adopt them early see"
- **Rationale**: Removed unnecessary transition and vague authority claim

**Category: Vague Authority Claims**
- **Original**: "studies show"
- **Revised**: [Removed]
- **Rationale**: Unsubstantiated claim weakens credibility

**Category: Buzzword Overload**
- **Original**: "paradigm shift"
- **Revised**: [Removed/implied]
- **Rationale**: Replaced with clearer language about adoption

**Category: Correlative Constructions**
- **Original**: "both technical expertise and strategic vision"
- **Revised**: "technical skill and clear strategy"
- **Rationale**: Simplified language while maintaining meaning

## Notes

- This skill should run automatically whenever Claude generates written content
- When auto-triggering, output format should be streamlined for quick readability
- For longer documents, prioritize the most egregious AI tells
- Always provide actionable, specific feedback rather than general criticism
