#!/usr/bin/env python3
"""
PDF to JSON/Markdown Raw Text Extractor (Hebrew-compatible)
----------------------------------------------------------
Extracts all text from a PDF, page by page, and saves it.
It does NOT try to detect chapters or sections.

REQUIREMENT:
You must have pdfminer.six installed:
python -m pip install pdfminer.six
"""

import json
import re
from pathlib import Path
from datetime import datetime
import sys

try:
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer, LAParams
except ImportError:
    print("\n--- ERROR: Missing Dependency ---")
    print("Required library 'pdfminer.six' not found.")
    print("Please run this command in your terminal:")
    print("python -m pip install pdfminer.six")
    print("-----------------------------------")
    sys.exit(1)


class RawPDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"File not found: {pdf_path}")

        self.metadata = {
            "filename": self.pdf_path.name,
            "extraction_date": datetime.now().isoformat(),
            "total_pages": 0,
        }
        self.pages = []  # This will be a list of strings

    def extract_text(self):
        """Extract text from each page and keep proper Hebrew visual order."""
        laparams = LAParams(line_margin=0.3, word_margin=0.1, char_margin=2.0)
        
        try:
            pdf_pages = list(extract_pages(self.pdf_path, laparams=laparams))
        except Exception as e:
            print(f"Error during PDF processing: {e}")
            print("This can happen if the PDF is scanned or password-protected.")
            sys.exit(1)

        self.metadata["total_pages"] = len(pdf_pages)
        print(f"Starting raw text extraction... {self.metadata['total_pages']} pages found.")
        
        for i, layout in enumerate(pdf_pages, start=1):
            print(f"  Reading page {i}...")
            text_chunks = []

            for element in layout:
                if isinstance(element, LTTextContainer):
                    text = element.get_text()
                    # Clean extra spaces/newlines
                    text = re.sub(r"\s+\n", "\n", text)
                    text = text.strip()
                    text_chunks.append(text)

            page_text = "\n".join(text_chunks).strip()
            self.pages.append(page_text) # Just add the raw text string

        print("Text extraction complete.")

    def export_json(self, output_path: str):
        """Save all extracted page text to a simple JSON file."""
        # The JSON will be a simple list of strings
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.pages, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved JSON to {output_path}")

    def export_markdown(self, output_path: str):
        """Save all extracted page text to a Markdown file."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Raw Text Extract: {self.metadata['filename']}\n\n")
            for i, page_text in enumerate(self.pages, start=1):
                f.write(f"\n\n--- PAGE {i} ---\n\n")
                f.write(page_text)
        print(f"✅ Saved Markdown to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_raw_text.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_stem = Path(pdf_path).stem
    
    # Define output filenames
    output_json_path = f"{output_stem}_raw.json"
    output_md_path = f"{output_stem}_raw.md"

    try:
        # 1. Make sure you have the library you were already using
        try:
            import pdfminer
        except ImportError:
            print("Installing pdfminer.six...")
            import subprocess
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', 'pdfminer.six', '--break-system-packages', '--user']
            )

        # 2. Run the extraction
        extractor = RawPDFExtractor(pdf_path)
        extractor.extract_text()
        
        # 3. Save both files
        extractor.export_json(output_json_path)
        extractor.export_markdown(output_md_path)
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")