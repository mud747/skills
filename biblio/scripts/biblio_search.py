#!/usr/bin/env python3
"""
Bibliographic search across multiple academic sources.
Supports CrossRef, arXiv, DBLP, and other sources.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


def search_crossref(query: str, max_results: int = 10) -> List[Dict]:
    """Search CrossRef API for academic publications."""
    base_url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": max_results,
        "mailto": "user@example.com"  # Polite pool
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get("message", {}).get("items", [])
    except Exception as e:
        print(f"CrossRef search error: {e}", file=sys.stderr)
        return []


def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
    """Search arXiv API for preprints."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            # arXiv returns XML, parse basic info
            content = response.read().decode()
            # Simple extraction - in production would use proper XML parser
            results = []
            entries = content.split("<entry>")[1:]

            for entry in entries[:max_results]:
                result = {}
                # Extract title
                if "<title>" in entry:
                    result["title"] = entry.split("<title>")[1].split("</title>")[0].strip()
                # Extract authors
                authors = []
                for author_block in entry.split("<author>")[1:]:
                    if "<name>" in author_block:
                        name = author_block.split("<name>")[1].split("</name>")[0].strip()
                        authors.append({"name": name})
                result["author"] = authors
                # Extract arXiv ID
                if "<id>" in entry:
                    arxiv_url = entry.split("<id>")[1].split("</id>")[0].strip()
                    result["arxiv_id"] = arxiv_url.split("/")[-1]
                # Extract published date
                if "<published>" in entry:
                    result["published"] = entry.split("<published>")[1].split("</published>")[0].strip()
                # Extract summary
                if "<summary>" in entry:
                    result["summary"] = entry.split("<summary>")[1].split("</summary>")[0].strip()

                results.append(result)

            return results
    except Exception as e:
        print(f"arXiv search error: {e}", file=sys.stderr)
        return []


def search_dblp(query: str, max_results: int = 10) -> List[Dict]:
    """Search DBLP for computer science publications."""
    base_url = "https://dblp.org/search/publ/api"
    params = {
        "q": query,
        "h": max_results,
        "format": "json"
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            hits = data.get("result", {}).get("hits", {}).get("hit", [])

            results = []
            for hit in hits:
                info = hit.get("info", {})
                result = {
                    "title": info.get("title"),
                    "authors": info.get("authors", {}).get("author", []),
                    "venue": info.get("venue"),
                    "year": info.get("year"),
                    "type": info.get("type"),
                    "doi": info.get("doi"),
                    "url": info.get("url")
                }
                results.append(result)

            return results
    except Exception as e:
        print(f"DBLP search error: {e}", file=sys.stderr)
        return []


def format_crossref_result(item: Dict) -> Dict:
    """Format CrossRef result into standardized structure."""
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
        "source": "CrossRef"
    }


def format_arxiv_result(item: Dict) -> Dict:
    """Format arXiv result into standardized structure."""
    authors = [author.get("name", "") for author in item.get("author", [])]
    year = item.get("published", "").split("-")[0] if item.get("published") else None

    return {
        "title": item.get("title"),
        "authors": authors,
        "year": year,
        "arxiv_id": item.get("arxiv_id"),
        "summary": item.get("summary"),
        "source": "arXiv"
    }


def format_dblp_result(item: Dict) -> Dict:
    """Format DBLP result into standardized structure."""
    authors = item.get("authors", [])
    if isinstance(authors, dict):
        authors = [authors.get("text", "")]
    elif isinstance(authors, list):
        authors = [a.get("text", "") if isinstance(a, dict) else str(a) for a in authors]

    return {
        "title": item.get("title"),
        "authors": authors,
        "year": item.get("year"),
        "venue": item.get("venue"),
        "doi": item.get("doi"),
        "url": item.get("url"),
        "type": item.get("type"),
        "source": "DBLP"
    }


def main():
    parser = argparse.ArgumentParser(description="Search academic sources for bibliographic references")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--source", choices=["crossref", "arxiv", "dblp", "all"], default="all",
                        help="Source to search (default: all)")
    parser.add_argument("--max-results", type=int, default=10,
                        help="Maximum number of results per source (default: 10)")
    parser.add_argument("--output", choices=["json", "simple"], default="json",
                        help="Output format (default: json)")

    args = parser.parse_args()

    all_results = []

    if args.source in ["crossref", "all"]:
        crossref_results = search_crossref(args.query, args.max_results)
        all_results.extend([format_crossref_result(r) for r in crossref_results])

    if args.source in ["arxiv", "all"]:
        arxiv_results = search_arxiv(args.query, args.max_results)
        all_results.extend([format_arxiv_result(r) for r in arxiv_results])

    if args.source in ["dblp", "all"]:
        dblp_results = search_dblp(args.query, args.max_results)
        all_results.extend([format_dblp_result(r) for r in dblp_results])

    if args.output == "json":
        print(json.dumps(all_results, indent=2))
    else:
        for i, result in enumerate(all_results, 1):
            print(f"\n{i}. {result.get('title', 'No title')}")
            print(f"   Authors: {', '.join(result.get('authors', []))}")
            print(f"   Year: {result.get('year', 'N/A')}")
            print(f"   Source: {result.get('source', 'Unknown')}")
            if result.get('doi'):
                print(f"   DOI: {result['doi']}")
            if result.get('arxiv_id'):
                print(f"   arXiv: {result['arxiv_id']}")


if __name__ == "__main__":
    main()
