#!/usr/bin/env python3
"""
Handle PDF downloads and metadata extraction for bibliographic references.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import re


def check_open_access(doi: str = None, arxiv_id: str = None) -> dict:
    """
    Check if a paper is available as open access.

    Args:
        doi: Digital Object Identifier
        arxiv_id: arXiv identifier

    Returns:
        Dictionary with open access information
    """
    result = {
        "is_open_access": False,
        "pdf_url": None,
        "source": None
    }

    # Check arXiv first (always open access)
    if arxiv_id:
        result["is_open_access"] = True
        result["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        result["source"] = "arXiv"
        return result

    # Check Unpaywall API for DOI
    if doi:
        doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
        url = f"https://api.unpaywall.org/v2/{doi}?email=user@example.com"

        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = json.loads(response.read().decode())

                if data.get("is_oa"):
                    result["is_open_access"] = True

                    # Try to get best OA location
                    best_oa = data.get("best_oa_location") or data.get("first_oa_location")
                    if best_oa and best_oa.get("url_for_pdf"):
                        result["pdf_url"] = best_oa["url_for_pdf"]
                        result["source"] = best_oa.get("host_type", "Unknown")

        except Exception as e:
            print(f"Error checking Unpaywall: {e}", file=sys.stderr)

    return result


def download_pdf(url: str, output_path: str) -> bool:
    """
    Download a PDF from a URL.

    Args:
        url: URL of the PDF
        output_path: Path to save the PDF

    Returns:
        True if successful, False otherwise
    """
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (compatible; BiblioBot/1.0)")

        with urllib.request.urlopen(req, timeout=60) as response:
            content_type = response.headers.get("Content-Type", "")

            if "application/pdf" not in content_type:
                print(f"Warning: Content-Type is {content_type}, not PDF", file=sys.stderr)

            with open(output_path, 'wb') as f:
                f.write(response.read())

        print(f"Downloaded: {output_path}")
        return True

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Download error: {e}", file=sys.stderr)
        return False


def extract_doi_from_pdf(pdf_path: str) -> str:
    """
    Extract DOI from PDF file (requires pdftotext or similar).

    Args:
        pdf_path: Path to PDF file

    Returns:
        DOI if found, None otherwise
    """
    # This is a simplified version. In production, you'd use PyPDF2, pdfplumber, or pdftotext
    try:
        import subprocess
        result = subprocess.run(
            ["pdftotext", "-l", "2", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=10
        )

        text = result.stdout

        # Common DOI patterns
        doi_patterns = [
            r'(?:doi:|DOI:)\s*(10\.\d{4,}/[^\s]+)',
            r'(10\.\d{4,}/[^\s]+)',
        ]

        for pattern in doi_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                doi = match.group(1).rstrip('.,;')
                return doi

        return None

    except FileNotFoundError:
        print("pdftotext not found. Install poppler-utils to extract DOI from PDFs.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error extracting DOI: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Handle PDF operations for bibliographic references")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Check open access
    check_parser = subparsers.add_parser("check", help="Check if paper is open access")
    check_parser.add_argument("--doi", help="DOI to check")
    check_parser.add_argument("--arxiv", help="arXiv ID to check")

    # Download PDF
    download_parser = subparsers.add_parser("download", help="Download PDF")
    download_parser.add_argument("url", help="URL of PDF to download")
    download_parser.add_argument("output", help="Output file path")

    # Extract DOI from PDF
    extract_parser = subparsers.add_parser("extract-doi", help="Extract DOI from PDF")
    extract_parser.add_argument("pdf", help="Path to PDF file")

    args = parser.parse_args()

    if args.command == "check":
        if not args.doi and not args.arxiv:
            print("Error: Must provide either --doi or --arxiv", file=sys.stderr)
            sys.exit(1)

        result = check_open_access(doi=args.doi, arxiv_id=args.arxiv)
        print(json.dumps(result, indent=2))

    elif args.command == "download":
        success = download_pdf(args.url, args.output)
        sys.exit(0 if success else 1)

    elif args.command == "extract-doi":
        doi = extract_doi_from_pdf(args.pdf)
        if doi:
            print(doi)
        else:
            print("No DOI found", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
