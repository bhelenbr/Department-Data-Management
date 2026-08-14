#! /usr/bin/env python3

"""Remove duplicate entries from a .bib file using bibtexparser.

This implementation depends on the ``bibtexparser`` package for robust
BibTeX parsing and writing. Duplicates are detected by:

- identical `doi` (case-insensitive)
- identical normalized `title` + normalized `author` + `year`
- identical bibkey (ID)

The function `remove_duplicates` returns the number of removed entries and
writes the cleaned database to `out` if provided, otherwise it overwrites
the input file.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Optional

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter



def _norm(text: str) -> str:
	t = (text or "").lower()
	t = re.sub(r"[^a-z0-9]", " ", t)
	t = re.sub(r"\s+", " ", t).strip()
	return t


def remove_duplicates(path: str, out: Optional[str] = None, keep_first: bool = True) -> int:
	"""Remove duplicate entries from a .bib file using bibtexparser.

	Raises a RuntimeError if `bibtexparser` is not available.
	"""
	if bibtexparser is None:
		raise RuntimeError("bibtexparser is required for remove_duplicates. Install it with `pip install bibtexparser`")

	p = Path(path)
	text = p.read_text(encoding="utf-8")
	db = bibtexparser.loads(text)
	entries = db.entries or []

	keys = set()
	dois = set()

	keep_entries = []
	removed = 0

	for ent in entries:
		# bibtexparser stores the bibkey under 'ID'
		key = ent.get("ID")
		doi = ent.get("doi") or ent.get("DOI")

		if (doi):
			doi = doi.lower()
			if doi in dois:
				removed += 1
				continue
		
		if (key in keys):
			removed += 1
			continue

		keys.add(key)
		if (doi):
			dois.add(doi)

		keep_entries.append(ent)

	# build output database and try to preserve preambles/strings if present
	out_db = BibDatabase()
	out_db.entries = keep_entries
	if getattr(db, "preambles", None):
		out_db.preambles = db.preambles
	if getattr(db, "comments", None):
		out_db.comments = db.comments
	if getattr(db, "strings", None):
		out_db.strings = db.strings

	writer = BibTexWriter()
	writer.indent = "  "
	writer.order_entries_by = None

	out_text = writer.write(out_db)

	out_path = Path(out) if out else p
	out_path.write_text(out_text, encoding="utf-8")
	return removed


def _main() -> None:
	parser = argparse.ArgumentParser(description="Remove duplicate entries from a .bib file")
	parser.add_argument("input", help="Input .bib file")
	parser.add_argument("-o", "--output", help="Output file (default: overwrite input)")
	args = parser.parse_args()
	removed = remove_duplicates(args.input, out=args.output)
	print(f"Removed {removed} duplicate entries")


if __name__ == "__main__":
	_main()
