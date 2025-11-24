# Bibliographic API Reference

This document provides details about the academic search APIs used by the biblio skill.

## CrossRef API

**Base URL:** `https://api.crossref.org/`

**Endpoints:**
- Search: `GET /works?query={query}&rows={max_results}`
- DOI Lookup: `GET /works/{doi}`

**Features:**
- Comprehensive academic publication database
- Excellent metadata quality
- Covers most disciplines
- Rate limits: 50 requests/second (with polite pool)

**Polite Pool:** Add `mailto` parameter to get better rate limits:
```
https://api.crossref.org/works?query=machine+learning&mailto=user@example.com
```

**Documentation:** https://api.crossref.org/

## arXiv API

**Base URL:** `http://export.arxiv.org/api/query`

**Parameters:**
- `search_query`: Query string (e.g., `all:machine learning` or `ti:neural networks`)
- `start`: Starting index (0-based)
- `max_results`: Maximum results to return

**Search Prefixes:**
- `ti:` - Title
- `au:` - Author
- `abs:` - Abstract
- `cat:` - Category
- `all:` - All fields

**Features:**
- Free access to scientific preprints
- Always open access with PDF links
- Strong in physics, mathematics, CS
- Returns XML format

**Documentation:** https://arxiv.org/help/api/

## DBLP API

**Base URL:** `https://dblp.org/search/publ/api`

**Parameters:**
- `q`: Query string
- `h`: Maximum hits (default: 30, max: 1000)
- `f`: First hit (0-based)
- `format`: Response format (xml or json)

**Features:**
- Computer science bibliography
- Excellent for CS publications
- Conference and journal papers
- Returns structured metadata

**Documentation:** https://dblp.org/faq/How+to+use+the+dblp+search+API.html

## Unpaywall API

**Base URL:** `https://api.unpaywall.org/v2/`

**Endpoint:** `GET /{doi}?email={email}`

**Features:**
- Checks open access availability for DOIs
- Provides PDF links when available
- Tracks legal open access sources
- Requires email parameter

**Response Fields:**
- `is_oa`: Boolean indicating OA status
- `best_oa_location`: Best OA source with PDF URL
- `oa_status`: Type of OA (gold, green, bronze, hybrid, closed)

**Documentation:** https://unpaywall.org/products/api

## Rate Limiting and Best Practices

1. **Be Polite:**
   - Add email/mailto to requests when supported
   - Respect rate limits
   - Cache results when possible

2. **Error Handling:**
   - Handle 404 (not found) gracefully
   - Implement timeouts (30 seconds for searches, 60 for PDFs)
   - Retry with exponential backoff on 5xx errors

3. **Attribution:**
   - Track source of each reference
   - Provide links to original sources
   - Credit the APIs in documentation

## Common Fields Mapping

Different APIs return different field names. Here's the standardized mapping:

| Standard Field | CrossRef        | arXiv          | DBLP           |
|---------------|-----------------|----------------|----------------|
| title         | title           | title          | title          |
| authors       | author          | author         | authors        |
| year          | published       | published      | year           |
| venue         | container-title | -              | venue          |
| doi           | DOI             | -              | doi            |
| url           | URL             | id             | url            |
| type          | type            | -              | type           |

## BibTeX Entry Types

Map publication types to BibTeX entry types:

- `journal-article` → `@article`
- `proceedings-article` → `@inproceedings`
- `book-chapter` → `@inbook`
- `book` → `@book`
- `thesis` → `@phdthesis` or `@mastersthesis`
- arXiv papers → `@misc` with `eprint` and `archivePrefix`
- Default → `@article`

## Org-Mode Format

Store references as org-mode headings with properties:

```org
** Paper Title
:PROPERTIES:
:AUTHORS: Author1, Author2
:YEAR: 2024
:DOI: 10.1234/example
:DOI_URL: https://doi.org/10.1234/example
:JOURNAL: Journal Name
:VOLUME: 42
:ISSUE: 3
:PAGES: 123-145
:URL: https://example.com/paper.pdf
:SOURCE: CrossRef
:END:

Abstract or notes go here.
```
