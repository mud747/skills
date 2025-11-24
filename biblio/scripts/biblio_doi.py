#!/usr/bin/env python3
"""
Look up bibliographic information by DOI.
"""

import argparse
import json
import sys
import urllib.request


def lookup_doi(doi: str) -> dict:
    """
    Look up bibliographic information for a DOI.

    Args:
        doi: Digital Object Identifier (with or without doi.org prefix)

    Returns:
        Dictionary containing bibliographic information
    """
    # Clean DOI
    doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")

    # CrossRef API
    url = f"https://api.crossref.org/works/{doi}"

    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get("message", {})
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"DOI not found: {doi}", file=sys.stderr)
        else:
            print(f"Error looking up DOI: {e}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {}


def format_result(item: dict) -> dict:
    """Format DOI lookup result into standardized structure."""
    authors = []
    for author in item.get("author", []):
        name_parts = []
        if "given" in author:
            name_parts.append(author["given"])
        if "family" in author:
            name_parts.append(author["family"])
        authors.append(" ".join(name_parts))

    title = item.get("title", [""])[0] if isinstance(item.get("title"), list) else item.get("title", "")

    return {
        "title": title,
        "authors": authors,
        "year": item.get("published-print", {}).get("date-parts", [[None]])[0][0] or
                item.get("published-online", {}).get("date-parts", [[None]])[0][0],
        "doi": item.get("DOI"),
        "journal": item.get("container-title", [""])[0] if isinstance(item.get("container-title"), list) else item.get("container-title"),
        "volume": item.get("volume"),
        "issue": item.get("issue"),
        "pages": item.get("page"),
        "publisher": item.get("publisher"),
        "type": item.get("type"),
        "url": item.get("URL"),
        "abstract": item.get("abstract"),
        "source": "CrossRef"
    }


def main():
    parser = argparse.ArgumentParser(description="Look up bibliographic information by DOI")
    parser.add_argument("doi", help="Digital Object Identifier (DOI)")
    parser.add_argument("--output", choices=["json", "simple"], default="json",
                        help="Output format (default: json)")

    args = parser.parse_args()

    result = lookup_doi(args.doi)

    if not result:
        sys.exit(1)

    formatted = format_result(result)

    if args.output == "json":
        print(json.dumps(formatted, indent=2))
    else:
        print(f"Title: {formatted.get('title', 'N/A')}")
        print(f"Authors: {', '.join(formatted.get('authors', []))}")
        print(f"Year: {formatted.get('year', 'N/A')}")
        print(f"Journal: {formatted.get('journal', 'N/A')}")
        if formatted.get('volume'):
            print(f"Volume: {formatted['volume']}")
        if formatted.get('issue'):
            print(f"Issue: {formatted['issue']}")
        if formatted.get('pages'):
            print(f"Pages: {formatted['pages']}")
        print(f"DOI: {formatted.get('doi', 'N/A')}")
        if formatted.get('url'):
            print(f"URL: {formatted['url']}")


if __name__ == "__main__":
    main()
