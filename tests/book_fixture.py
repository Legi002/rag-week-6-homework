from __future__ import annotations

import hashlib


START = "*** START OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"
END = "*** END OF THE PROJECT GUTENBERG EBOOK THE PRINCE ***"


def _chapters() -> list[str]:
    roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI"]
    blocks = []
    for number, marker in enumerate(roman, start=1):
        suffix = "[1]" if marker == "XVIII" else ""
        blocks.append(f"CHAPTER {marker}.{suffix}\nSYNTHETIC CHAPTER {number} TITLE\n\n")
        blocks.append(f"Synthetic chapter {number} begins with Prince material.\n")
        if marker == "III":
            blocks.append("Prince errors: 1) weakened small powers, 2) strengthened great powers, 3) invited foreigners, 4) failed to settle, and 5) sent no colonies.\n")
        if marker == "XII":
            blocks.append("Mercenaries are useless and dangerous because they lack discipline.\n")
        if marker == "XVII":
            blocks.append("A prince must be feared and loved, but it is much safer to be feared than loved when either must be dispensed with.\n")
    return blocks


def fixture_body() -> str:
    parts = [
        "_ Nicolo Machiavelli, born at Florence\n\nThis editorial note includes Unicode: Æ and café.\n",
        "INTRODUCTION\n\nNicolo Machiavelli was born at Florence on 3rd May 1469.\n",
        "YOUTH — Æt. 1-25—1469-94\n\nYouth was a period in Florence.\n",
        "OFFICE — Æt. 25-43—1494-1512\n\nOffice was held in Florence.\n",
        "LITERATURE AND DEATH — Æt. 43-58—1512-27\n\nLiterature and death came later.\n",
        "THE MAN AND HIS WORKS\n\nThe man and his works are discussed.\n",
        "DEDICATION\n\nA dedication for a prince.\n\nTHE PRINCE\nExcluded title banner.\n",
        *_chapters(),
        "DESCRIPTION OF THE METHODS ADOPTED BY THE DUKE VALENTINO WHEN MURDERING\nA VICTIM\nAT SINIGAGLIA\n\nBy Nicolo Machiavelli\nThe byline remains section content.\n",
        "THE LIFE OF CASTRUCCIO CASTRACANI OF LUCCA\n\nBy Nicolo Machiavelli\nThe final appendix closes the fixture.\n",
    ]
    return "".join(parts)


def make_fixture_text(body: Optional[str] = None) -> str:
    return (
        "Title: The Prince\n"
        "Author: Nicolo Machiavelli\n"
        "Translator: W. K. Marriott\n"
        "Release date: February 11, 2006 [eBook #1232]\n"
        "Most recently updated: July 24, 2026\n"
        "Language: English\n\n"
        f"{START}\n"
        "The Prince\n\nContents\n INTRODUCTION\n CHAPTER I. LIST ENTRY\n\n"
        f"{fixture_body() if body is None else body}"
        f"{END}\n\nProject Gutenberg License material outside the book body.\n"
    )


def fixture_manifest(raw: Optional[str] = None):
    from src.book_corpus import BookManifest

    source = make_fixture_text() if raw is None else raw
    canonical = source.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    start = canonical.index(START + "\n") + len(START) + 1
    end = canonical.index(END, start)
    body = canonical[start:end]
    return BookManifest(
        ebook_id="1232",
        title="The Prince",
        author="Nicolo Machiavelli",
        translator="W. K. Marriott",
        language="English",
        release_date="2006-02-11",
        updated_date="2026-07-24",
        source_sha256=hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        body_sha256=hashlib.sha256(body.encode("utf-8")).hexdigest(),
        section_ids=(
            "editorial-note", "introduction", "youth", "office", "literature-death",
            "man-works", "dedication", *(f"chapter-{n:02}" for n in range(1, 27)),
            "appendix-valentino", "appendix-castruccio",
        ),
    )
