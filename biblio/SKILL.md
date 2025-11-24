---
name: biblio
description: Search and retrieve bibliographic references from academic sources (CrossRef, arXiv, DBLP), look up papers by DOI, check open access availability, download PDFs, and format references in BibTeX or org-mode format. Use this skill when users need to find academic papers, build bibliographies, or manage references for research or writing.
---

# Biblio - Academic Reference Management

## Overview

This skill provides comprehensive bibliographic search and reference management capabilities, replicating functionality from biblio.el for Claude Code. Search multiple academic sources, retrieve metadata, check open access status, download PDFs, and format references in BibTeX or org-mode format.

## When to Use This Skill

Use this skill when users request:
- Searching for academic papers by keywords or topic
- Looking up papers by DOI
- Building bibliographies for LaTeX documents or research
- Finding open access versions of papers
- Converting references to BibTeX or org-mode format
- Downloading PDFs from open access sources
- Managing references in org-mode files

## Core Workflows

### 1. Search for Papers by Keywords

Search multiple academic databases simultaneously.

**User requests:**
- "Find papers about machine learning"
- "Search for research on neural networks"
- "Look up papers about quantum computing from arXiv"

**Process:**

1. Use `scripts/biblio_search.py` to search academic sources:
   ```bash
   python3 scripts/biblio_search.py "machine learning" --source all --max-results 10
   ```

2. Available sources:
   - `crossref` - Comprehensive academic database (all disciplines)
   - `arxiv` - Scientific preprints (physics, math, CS)
   - `dblp` - Computer science publications
   - `all` - Search all sources (default)

3. The script returns JSON with standardized metadata:
   - title, authors, year, journal/venue
   - DOI, arXiv ID, URLs
   - source information

4. Present results to user with clear formatting
5. Offer to format selected papers in BibTeX or org-mode

**Example:**
```bash
python3 scripts/biblio_search.py "transformer architecture" --source arxiv --max-results 5
```

### 2. Look Up Paper by DOI

Retrieve detailed metadata for a specific DOI.

**User requests:**
- "Get the BibTeX for DOI 10.1234/example"
- "Look up this paper: https://doi.org/10.1145/3..."
- "Find the full reference for DOI 10.1038/..."

**Process:**

1. Use `scripts/biblio_doi.py` to look up the DOI:
   ```bash
   python3 scripts/biblio_doi.py "10.1234/example"
   ```

2. The script returns comprehensive metadata from CrossRef
3. Format the result using `format_reference.py` (see below)

**Example:**
```bash
# Look up and format as BibTeX
python3 scripts/biblio_doi.py "10.1145/3544548.3580895" | \
  python3 scripts/format_reference.py --format bibtex
```

### 3. Check Open Access and Download PDFs

Check if papers are available as open access and download PDFs.

**User requests:**
- "Is this paper available open access?"
- "Download the PDF for this DOI"
- "Find free versions of these papers"

**Process:**

1. Check open access status:
   ```bash
   python3 scripts/biblio_pdf.py check --doi "10.1234/example"
   # or for arXiv
   python3 scripts/biblio_pdf.py check --arxiv "2301.12345"
   ```

2. Returns JSON with:
   - `is_open_access`: Boolean
   - `pdf_url`: Direct PDF link (if available)
   - `source`: Where the OA version is hosted

3. Download PDF if available:
   ```bash
   python3 scripts/biblio_pdf.py download "https://arxiv.org/pdf/2301.12345.pdf" "paper.pdf"
   ```

**Note:** arXiv papers are always open access. For other sources, use the Unpaywall API (via DOI check).

### 4. Format References

Convert references to BibTeX or org-mode format.

**User requests:**
- "Format this as BibTeX"
- "Add this reference to my bibliography.bib file"
- "Convert these papers to org-mode format"
- "Create BibTeX entries for my references.org"

**Process:**

1. Format as BibTeX:
   ```bash
   python3 scripts/format_reference.py --format bibtex < results.json
   ```

2. Format as org-mode:
   ```bash
   python3 scripts/format_reference.py --format orgmode --level 2 < results.json
   ```

3. Save to file:
   - For BibTeX: Append to `.bib` file
   - For org-mode: Insert into `.org` file at appropriate location

**BibTeX output example:**
```bibtex
@article{Smith2024Attention,
  title = {Attention Is All You Need},
  author = {John Smith and Jane Doe},
  year = {2024},
  journal = {Nature},
  volume = {42},
  pages = {123-145},
  doi = {10.1038/example},
}
```

**Org-mode output example:**
```org
** Attention Is All You Need
:PROPERTIES:
:AUTHORS: John Smith, Jane Doe
:YEAR: 2024
:DOI: 10.1038/example
:DOI_URL: https://doi.org/10.1038/example
:JOURNAL: Nature
:VOLUME: 42
:PAGES: 123-145
:SOURCE: CrossRef
:END:
```

### 5. Complete Workflow Examples

**Example 1: Search and add to bibliography**
```bash
# Search for papers
python3 scripts/biblio_search.py "deep learning survey" --source all --max-results 5 > results.json

# Format as BibTeX
python3 scripts/format_reference.py --format bibtex < results.json >> bibliography.bib
```

**Example 2: DOI to org-mode**
```bash
# Look up DOI
python3 scripts/biblio_doi.py "10.1145/3544548.3580895" | \
  python3 scripts/format_reference.py --format orgmode >> references.org
```

**Example 3: Find and download open access paper**
```bash
# Check if open access
python3 scripts/biblio_pdf.py check --doi "10.1234/example" > oa_check.json

# If open access, download
# (extract pdf_url from oa_check.json)
python3 scripts/biblio_pdf.py download "https://..." "paper.pdf"
```

## Managing References in Org-Mode

For users with org-mode workflows:

1. **Central bibliography file:** Create `references.org` to store all references
2. **Per-project files:** Use separate files like `project-refs.org` for specific projects
3. **Search and add:** Search → format as orgmode → append to file
4. **Properties for queries:** Use org-mode properties to filter by year, author, topic

**Example org-mode structure:**
```org
* Machine Learning References

** Attention Is All You Need
:PROPERTIES:
:AUTHORS: Vaswani et al.
:YEAR: 2017
:ARXIV: 1706.03762
:TOPIC: transformers
:END:

** BERT: Pre-training of Deep Bidirectional Transformers
:PROPERTIES:
:AUTHORS: Devlin et al.
:YEAR: 2018
:ARXIV: 1810.04805
:TOPIC: transformers, NLP
:END:
```

## Tips and Best Practices

1. **Start broad, then narrow:**
   - Search all sources first to see what's available
   - Use specific sources (arXiv, DBLP) when you know where to look

2. **Check open access first:**
   - Always check OA status before trying to access papers
   - arXiv papers are always freely available

3. **Consistent citation keys:**
   - BibTeX keys auto-generate as `AuthorYearTitle`
   - Customize with `--citation-key` if needed

4. **Combine formats:**
   - Store in org-mode for note-taking
   - Export to BibTeX when writing papers

5. **API reference:**
   - See `references/api_reference.md` for detailed API documentation
   - Includes rate limits, best practices, field mappings

## Scripts Reference

All scripts support `--help` for detailed usage:

- `biblio_search.py` - Search academic sources
- `biblio_doi.py` - Look up by DOI
- `biblio_pdf.py` - PDF operations (check OA, download, extract DOI)
- `format_reference.py` - Format as BibTeX or org-mode

## Common Issues

**"No results found":**
- Try different search terms or sources
- Some specialized topics may only be in specific databases

**"DOI not found":**
- Verify the DOI is correct
- Try searching by title instead

**"PDF download failed":**
- Not all papers have open access PDFs
- Check OA status first before attempting download
- Some publishers block automated downloads

**"pdftotext not found":**
- Install poppler-utils: `brew install poppler` (macOS) or `apt-get install poppler-utils` (Linux)
- Only needed for extracting DOI from PDFs
