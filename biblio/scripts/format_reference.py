#!/usr/bin/env python3
"""
Format bibliographic references in BibTeX or org-mode format.
"""

import argparse
import json
import sys
import re


def sanitize_bibtex_key(text: str) -> str:
    """Sanitize text for use as BibTeX citation key."""
    # Remove special characters, keep only alphanumeric and hyphens
    return re.sub(r'[^a-zA-Z0-9-]', '', text.replace(" ", "-"))


def generate_citation_key(ref: dict) -> str:
    """Generate a BibTeX citation key from reference data."""
    authors = ref.get("authors", [])
    year = ref.get("year", "")

    if authors:
        first_author = authors[0].split()[-1]  # Last name
        first_author = sanitize_bibtex_key(first_author)
    else:
        first_author = "unknown"

    title_words = ref.get("title", "").split()[:3]
    title_part = sanitize_bibtex_key("-".join(title_words))

    return f"{first_author}{year}{title_part}"[:50]  # Limit length


def format_bibtex_authors(authors: list) -> str:
    """Format author list for BibTeX."""
    return " and ".join(authors)


def to_bibtex(ref: dict, citation_key: str = None) -> str:
    """Convert reference to BibTeX format."""
    if citation_key is None:
        citation_key = generate_citation_key(ref)

    # Determine entry type
    ref_type = ref.get("type", "article")
    if ref_type == "journal-article":
        entry_type = "article"
    elif ref_type == "book-chapter":
        entry_type = "inbook"
    elif ref_type == "proceedings-article":
        entry_type = "inproceedings"
    elif ref.get("arxiv_id"):
        entry_type = "misc"
    else:
        entry_type = "article"

    lines = [f"@{entry_type}{{{citation_key},"]

    # Title
    if ref.get("title"):
        lines.append(f'  title = {{{ref["title"]}}},')

    # Authors
    if ref.get("authors"):
        authors_str = format_bibtex_authors(ref["authors"])
        lines.append(f'  author = {{{authors_str}}},')

    # Year
    if ref.get("year"):
        lines.append(f'  year = {{{ref["year"]}}},')

    # Journal/Venue
    if ref.get("journal"):
        lines.append(f'  journal = {{{ref["journal"]}}},')
    elif ref.get("venue"):
        lines.append(f'  journal = {{{ref["venue"]}}},')

    # Volume
    if ref.get("volume"):
        lines.append(f'  volume = {{{ref["volume"]}}},')

    # Issue/Number
    if ref.get("issue"):
        lines.append(f'  number = {{{ref["issue"]}}},')

    # Pages
    if ref.get("pages"):
        lines.append(f'  pages = {{{ref["pages"]}}},')

    # DOI
    if ref.get("doi"):
        lines.append(f'  doi = {{{ref["doi"]}}},')

    # arXiv ID
    if ref.get("arxiv_id"):
        lines.append(f'  eprint = {{{ref["arxiv_id"]}}},')
        lines.append(f'  archivePrefix = {{arXiv}},')

    # URL
    if ref.get("url"):
        lines.append(f'  url = {{{ref["url"]}}},')

    # Publisher
    if ref.get("publisher"):
        lines.append(f'  publisher = {{{ref["publisher"]}}},')

    # Remove trailing comma from last field
    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]

    lines.append("}")

    return "\n".join(lines)


def to_orgmode(ref: dict, level: int = 2) -> str:
    """Convert reference to org-mode format."""
    stars = "*" * level
    title = ref.get("title", "Untitled")
    authors = ", ".join(ref.get("authors", []))
    year = ref.get("year", "")

    lines = [f"{stars} {title}"]
    lines.append(f":PROPERTIES:")
    lines.append(f":AUTHORS: {authors}")
    if year:
        lines.append(f":YEAR: {year}")
    if ref.get("doi"):
        lines.append(f":DOI: {ref['doi']}")
        lines.append(f":DOI_URL: https://doi.org/{ref['doi']}")
    if ref.get("arxiv_id"):
        lines.append(f":ARXIV: {ref['arxiv_id']}")
        lines.append(f":ARXIV_URL: https://arxiv.org/abs/{ref['arxiv_id']}")
    if ref.get("url"):
        lines.append(f":URL: {ref['url']}")
    if ref.get("journal"):
        lines.append(f":JOURNAL: {ref['journal']}")
    if ref.get("venue"):
        lines.append(f":VENUE: {ref['venue']}")
    if ref.get("volume"):
        lines.append(f":VOLUME: {ref['volume']}")
    if ref.get("issue"):
        lines.append(f":ISSUE: {ref['issue']}")
    if ref.get("pages"):
        lines.append(f":PAGES: {ref['pages']}")
    if ref.get("publisher"):
        lines.append(f":PUBLISHER: {ref['publisher']}")
    if ref.get("source"):
        lines.append(f":SOURCE: {ref['source']}")
    lines.append(f":END:")

    if ref.get("summary"):
        lines.append("")
        lines.append(ref["summary"])
    elif ref.get("abstract"):
        lines.append("")
        lines.append(ref["abstract"])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format bibliographic references")
    parser.add_argument("--format", choices=["bibtex", "orgmode"], required=True,
                        help="Output format")
    parser.add_argument("--input", help="Input JSON file (default: stdin)")
    parser.add_argument("--citation-key", help="Custom citation key for BibTeX")
    parser.add_argument("--level", type=int, default=2,
                        help="Heading level for org-mode format (default: 2)")

    args = parser.parse_args()

    # Read input
    if args.input:
        with open(args.input, 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    # Handle single reference or list of references
    if isinstance(data, list):
        references = data
    else:
        references = [data]

    # Format each reference
    formatted_refs = []
    for ref in references:
        if args.format == "bibtex":
            formatted_refs.append(to_bibtex(ref, args.citation_key))
        else:  # orgmode
            formatted_refs.append(to_orgmode(ref, args.level))

    # Print results
    separator = "\n\n" if args.format == "bibtex" else "\n\n"
    print(separator.join(formatted_refs))


if __name__ == "__main__":
    main()
