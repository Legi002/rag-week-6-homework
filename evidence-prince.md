# Prince Book Extension Evidence

Generated from actual `python -m src.cli` output on 2026-10-14. The external source remains outside Git.

## Source and policy

- Edition: English Project Gutenberg ebook 1232, *The Prince*, translated by W. K. Marriott; release 2006-02-11, updated 2026-07-24.
- File bytes: 308019; raw SHA-256: `33496a305f7a4b933784fb5aec95f920fbc3d4687794817e4cc444aa6578d2e4`.
- Canonical source SHA-256: `948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368`; canonical body SHA-256: `347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1`; body length: 282,640 Unicode characters.
- Sections: 35 total, including 26 chapters. Parser `prince-sections-v1`; normalizer `lf-v1`; tokenizer `book-lexical-v1`; admission `book-evidence-v1`.
- Chunk configurations: 400/80 and 800/120; top-k limits: 2 and 3; BM25 `k1=1.5`, `b=0.75`. BM25 scores are ranking signals, not answer confidence.
- Source commands use `--corpus-file PATH`; no application download or network call is involved.

## Five homework outcomes

1. **Chunking impact:** the two book configurations were exercised across all 12 fixed cases. Each uses exact canonical character windows; scores are configuration-specific and are not presented as confidence.
2. **Top-k retrieval:** both k=2 and k=3 were run for every case. Raw candidate display and admitted excerpt count are capped independently at k.
3. **Citation quality:** each positive answer cites only accepted excerpt IDs. The acceptance run checked every quote against its exact canonical half-open body offsets and section.
4. **Refusal behavior:** all seven fixed negative cases refused with zero accepted excerpts and zero answer citations, across all four setting combinations.
5. **Evidence pair:** the commands and representative positive/refusal outputs below were produced by the implemented CLI. Original homework evidence remains in `evidence.md`.

### Fixed-case matrix

Each cell is `answer/refusal; displayed raw candidates; admitted excerpts`. `Known false refusal` is labeled separately because the book contains the answer but literal matching rejects the paraphrase.

| Case | 400/80 k2 | 400/80 k3 | 800/120 k2 | 800/120 k3 |
|---|---:|---:|---:|---:|
| supported-five | answer; 2; 1 | answer; 3; 1 | answer; 2; 1 | answer; 3; 1 |
| supported-feared | answer; 2; 1 | answer; 3; 1 | answer; 2; 1 | answer; 3; 1 |
| supported-mercenaries | answer; 2; 1 | answer; 3; 1 | answer; 2; 1 | answer; 3; 1 |
| supported-birth | answer; 2; 2 | answer; 3; 2 | answer; 2; 2 | answer; 3; 2 |
| weather | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| weather-ordinal | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| birth-time | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| salary | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| temperature | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| wrong-year | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| negation | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |
| known-false-refusal (known false refusal) | refusal; 2; 0 | refusal; 3; 0 | refusal; 2; 0 | refusal; 3; 0 |

Observed result: supported cases 4/4 admitted, negatives 7/7 refused, and the one known paraphrase false refusal was recorded, for each of the four configuration/top-k pairs (48/48 expected outcomes). The 48 outcomes are application runs, not planning probes.

## Representative actual CLI output

### supported-five (800/120, k=3)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "What were the five errors of Louis?" --chunk-size 800 --overlap 120 --top-k 3 --show-retrieval
```

```text
Question:
What were the five errors of Louis?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 800
Overlap: 120
Top-k: 3
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-w43763-44563
    BM25 score: 12.24237257
    Section: chapter-03 (chapter)
    Heading: CONCERNING MIXED PRINCIPALITIES
    Source offsets: [43763, 44563)
    Text: o was able to drive him, Louis, out
in turn.

The wish to acquire is in truth very natural and common, and men always
do so when they can, and for this they will be praised not blamed; but
when they cannot do so, yet wish to do so by any means, then there is
folly and blame. Therefore, if France could have attacked Naples with
her own forces she ought to have done so; if she could not, then she
ought not to have divided it. And if the partition which she made with
the Venetians in Lombardy was justified by the excuse that by it she
got a foothold in Italy, this other partition merited blame, for it had
not the excuse of that necessity.

Therefore Louis made these five errors: he destroyed the minor powers,
he increased the strength of one of the greater powers in Italy, he
brought in a for
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-office-w6853-7653
    BM25 score: 10.45681218
    Section: office (front-matter)
    Heading: OFFICE — Æt. 25-43—1494-1512
    Source offsets: [6853, 7653)
    Text: ers of his time gives a fair indication of his activities, and
supplies the sources from which he drew the experiences and characters
which illustrate _The Prince_.

His first mission was in 1499 to Catherina Sforza, “my lady of Forli”
of _The Prince_, from whose conduct and fate he drew the moral that it
is far better to earn the confidence of the people than to rely on
fortresses. This is a very noticeable principle in Machiavelli, and is
urged by him in many ways as a matter of vital importance to princes.

In 1500 he was sent to France to obtain terms from Louis XII for
continuing the war against Pisa: this king it was who, in his conduct
of affairs in Italy, committed the five capital errors in statecraft
summarized in _The Prince_, and was consequently driven out. He, also,
it was wh
  Rank: 3
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-office-w7533-8333
    BM25 score: 6.90408765
    Section: office (front-matter)
    Heading: OFFICE — Æt. 25-43—1494-1512
    Source offsets: [7533, 8333)
    Text: d the five capital errors in statecraft
summarized in _The Prince_, and was consequently driven out. He, also,
it was who made the dissolution of his marriage a condition of support
to Pope Alexander VI; which leads Machiavelli to refer those who urge
that such promises should be kept to what he has written concerning the
faith of princes.

Machiavelli’s public life was largely occupied with events arising out
of the ambitions of Pope Alexander VI and his son, Cesare Borgia, the
Duke Valentino, and these characters fill a large space of _The
Prince_. Machiavelli never hesitates to cite the actions of the duke
for the benefit of usurpers who wish to keep the states they have
seized; he can, indeed, find no precepts to offer so good as the
pattern of Cesare Borgia’s conduct, insomuch that Ce

Accepted answer evidence:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-s44408-44634
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-w43763-44563
    Origin BM25 score: 12.24237257
    Admission policy: book-evidence-v1
    Source offsets: [44408, 44634)
    Text: Therefore Louis made these five errors: he destroyed the minor powers,
he increased the strength of one of the greater powers in Italy, he
brought in a foreign power, he did not settle in the country, he did
not send colonies.

Answer:
Matching source excerpts:
"Therefore Louis made these five errors: he destroyed the minor powers,
he increased the strength of one of the greater powers in Italy, he
brought in a foreign power, he did not settle in the country, he did
not send colonies."

Refused: False
Citations: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-s44408-44634

References:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-s44408-44634
    Section: chapter-03 (chapter)
    Heading: CONCERNING MIXED PRINCIPALITIES
    Source offsets: [44408, 44634)
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-w43763-44563
```

### supported-feared (400/80, k=2)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "Is it safer to be feared than loved?" --chunk-size 400 --overlap 80 --top-k 2 --show-retrieval
```

```text
Question:
Is it safer to be feared than loved?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 400
Overlap: 80
Top-k: 2
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-w136530-136929
    BM25 score: 14.22661925
    Section: chapter-17 (chapter)
    Heading: CONCERNING CRUELTY AND CLEMENCY, AND WHETHER IT IS BETTER TO BE LOVED THAN FEARED
    Source offsets: [136530, 136929)
    Text: wish to
be both, but, because it is difficult to unite them in one person, it
is much safer to be feared than loved, when, of the two, either must be
dispensed with. Because this is to be asserted in general of men, that
they are ungrateful, fickle, false, cowardly, covetous, and as long as
you succeed they are yours entirely; they will offer you their blood,
property, life, and children, as is s
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-w136209-136609
    BM25 score: 11.95979711
    Section: chapter-17 (chapter)
    Heading: CONCERNING CRUELTY AND CLEMENCY, AND WHETHER IT IS BETTER TO BE LOVED THAN FEARED
    Source offsets: [136209, 136609)
    Text: ble.

 [2] . . . against my will, my fate
A throne unsettled, and an infant state,
Bid me defend my realms with all my pow’rs,
And guard with these severities my shores.

Christopher Pitt.

Upon this a question arises: whether it be better to be loved than
feared or feared than loved? It may be answered that one should wish to
be both, but, because it is difficult to unite them in one person, it
i

Accepted answer evidence:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-s136495-136695
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-w136530-136929
    Origin BM25 score: 14.22661925
    Admission policy: book-evidence-v1
    Source offsets: [136495, 136695)
    Text: It may be answered that one should wish to
be both, but, because it is difficult to unite them in one person, it
is much safer to be feared than loved, when, of the two, either must be
dispensed with.

Answer:
Matching source excerpts:
"It may be answered that one should wish to
be both, but, because it is difficult to unite them in one person, it
is much safer to be feared than loved, when, of the two, either must be
dispensed with."

Refused: False
Citations: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-s136495-136695

References:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-s136495-136695
    Section: chapter-17 (chapter)
    Heading: CONCERNING CRUELTY AND CLEMENCY, AND WHETHER IT IS BETTER TO BE LOVED THAN FEARED
    Source offsets: [136495, 136695)
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c400-o80-chapter-17-w136530-136929
```

### supported-mercenaries (800/120, k=2)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "Why are mercenaries useless and dangerous?" --chunk-size 800 --overlap 120 --top-k 2 --show-retrieval
```

```text
Question:
Why are mercenaries useless and dangerous?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 800
Overlap: 120
Top-k: 2
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-12-w103542-104342
    BM25 score: 12.36849352
    Section: chapter-12 (chapter)
    Heading: HOW MANY KINDS OF SOLDIERY THERE ARE, AND CONCERNING MERCENARIES
    Source offsets: [103542, 104342)
    Text: te is not well armed, it follows that where they are
well armed they have good laws. I shall leave the laws out of the
discussion and shall speak of the arms.

I say, therefore, that the arms with which a prince defends his state
are either his own, or they are mercenaries, auxiliaries, or mixed.
Mercenaries and auxiliaries are useless and dangerous; and if one holds
his state based on these arms, he will stand neither firm nor safe; for
they are disunited, ambitious, and without discipline, unfaithful,
valiant before friends, cowardly before enemies; they have neither the
fear of God nor fidelity to men, and destruction is deferred only so
long as the attack is; for in peace one is robbed by them, and in war
by the enemy. The fact is, they have no other attraction or reason for
keeping th
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-19-w167020-167820
    BM25 score: 7.71462768
    Section: chapter-19 (chapter)
    Heading: THAT ONE SHOULD AVOID BEING DESPISED AND HATED
    Source offsets: [167020, 167820)
    Text: or although the prince is new, the constitution of the state
is old, and it is framed so as to receive him as if he were its
hereditary lord.

But returning to the subject of our discourse, I say that whoever will
consider it will acknowledge that either hatred or contempt has been
fatal to the above-named emperors, and it will be recognized also how
it happened that, a number of them acting in one way and a number in
another, only one in each way came to a happy end and the rest to
unhappy ones. Because it would have been useless and dangerous for
Pertinax and Alexander, being new princes, to imitate Marcus, who was
heir to the principality; and likewise it would have been utterly
destructive to Caracalla, Commodus, and Maximinus to have imitated
Severus, they not having sufficient valour

Accepted answer evidence:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-12-s103840-104274
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-12-w103542-104342
    Origin BM25 score: 12.36849352
    Admission policy: book-evidence-v1
    Source offsets: [103840, 104274)
    Text: Mercenaries and auxiliaries are useless and dangerous; and if one holds
his state based on these arms, he will stand neither firm nor safe; for
they are disunited, ambitious, and without discipline, unfaithful,
valiant before friends, cowardly before enemies; they have neither the
fear of God nor fidelity to men, and destruction is deferred only so
long as the attack is; for in peace one is robbed by them, and in war
by the enemy.

Answer:
Matching source excerpts:
"Mercenaries and auxiliaries are useless and dangerous; and if one holds
his state based on these arms, he will stand neither firm nor safe; for
they are disunited, ambitious, and without discipline, unfaithful,
valiant before friends, cowardly before enemies; they have neither the
fear of God nor fidelity to men, and destruction is deferred only so
long as the attack is; for in peace one is robbed by them, and in war
by the enemy."

Refused: False
Citations: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-12-s103840-104274

References:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-12-s103840-104274
    Section: chapter-12 (chapter)
    Heading: HOW MANY KINDS OF SOLDIERY THERE ARE, AND CONCERNING MERCENARIES
    Source offsets: [103840, 104274)
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-12-w103542-104342
```

### supported-birth (800/120, k=2)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "When was Nicolo Machiavelli born?" --chunk-size 800 --overlap 120 --top-k 2 --show-retrieval
```

```text
Question:
When was Nicolo Machiavelli born?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 800
Overlap: 120
Top-k: 2
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-w2733-3531
    BM25 score: 11.68732185
    Section: introduction (front-matter)
    Heading: INTRODUCTION
    Source offsets: [2733, 3531)
    Text: Nicolo Machiavelli was born at Florence on 3rd May 1469. He was the
second son of Bernardo di Nicolo Machiavelli, a lawyer of some repute,
and of Bartolommea di Stefano Nelli, his wife. Both parents were
members of the old Florentine nobility.

His life falls naturally into three periods, each of which singularly
enough constitutes a distinct and important era in the history of
Florence. His youth was concurrent with the greatness of Florence as an
Italian power under the guidance of Lorenzo de’ Medici, Il Magnifico.
The downfall of the Medici in Florence occurred in 1494, in which year
Machiavelli entered the public service. During his official career
Florence was free under the government of a Republic, which lasted
until 1512, when the Medici returned to power, and Machiavelli lost hi
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-w2433-2713
    BM25 score: 11.30320826
    Section: editorial-note (editorial-note)
    Heading: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
    Source offsets: [2433, 2713)
    Text: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
1512 held an official post at Florence which included diplomatic
missions to various European courts. Imprisoned in Florence, 1512;
later exiled and returned to San Casciano. Died at Florence on 22nd
June 1527._

Accepted answer evidence:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-s2733-2789
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-w2733-3531
    Origin BM25 score: 11.68732185
    Admission policy: book-evidence-v1
    Source offsets: [2733, 2789)
    Text: Nicolo Machiavelli was born at Florence on 3rd May 1469.
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-s2433-2488
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-w2433-2713
    Origin BM25 score: 11.30320826
    Admission policy: book-evidence-v1
    Source offsets: [2433, 2488)
    Text: _ Nicolo Machiavelli, born at Florence on 3rd May 1469.

Answer:
Matching source excerpts:
"Nicolo Machiavelli was born at Florence on 3rd May 1469."
"_ Nicolo Machiavelli, born at Florence on 3rd May 1469."

Refused: False
Citations: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-s2733-2789, pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-s2433-2488

References:
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-s2733-2789
    Section: introduction (front-matter)
    Heading: INTRODUCTION
    Source offsets: [2733, 2789)
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-w2733-3531
  Excerpt ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-s2433-2488
    Section: editorial-note (editorial-note)
    Heading: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
    Source offsets: [2433, 2488)
    Origin chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-w2433-2713
```

### weather (800/120, k=2)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "What was the weather in Florence on May 3, 1469?" --chunk-size 800 --overlap 120 --top-k 2 --show-retrieval
```

```text
Question:
What was the weather in Florence on May 3, 1469?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 800
Overlap: 120
Top-k: 2
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-w2433-2713
    BM25 score: 13.72684765
    Section: editorial-note (editorial-note)
    Heading: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
    Source offsets: [2433, 2713)
    Text: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
1512 held an official post at Florence which included diplomatic
missions to various European courts. Imprisoned in Florence, 1512;
later exiled and returned to San Casciano. Died at Florence on 22nd
June 1527._
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-w2733-3531
    BM25 score: 10.97885435
    Section: introduction (front-matter)
    Heading: INTRODUCTION
    Source offsets: [2733, 3531)
    Text: Nicolo Machiavelli was born at Florence on 3rd May 1469. He was the
second son of Bernardo di Nicolo Machiavelli, a lawyer of some repute,
and of Bartolommea di Stefano Nelli, his wife. Both parents were
members of the old Florentine nobility.

His life falls naturally into three periods, each of which singularly
enough constitutes a distinct and important era in the history of
Florence. His youth was concurrent with the greatness of Florence as an
Italian power under the guidance of Lorenzo de’ Medici, Il Magnifico.
The downfall of the Medici in Florence occurred in 1494, in which year
Machiavelli entered the public service. During his official career
Florence was free under the government of a Republic, which lasted
until 1512, when the Medici returned to power, and Machiavelli lost hi

Accepted answer evidence:
  None

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.
The local quote policy did not admit evidence; this does not prove the book lacks an answer.
Refusal reason: NO_ADMISSIBLE_SENTENCE

Refused: True
Citations: None
```

### birth-time (800/120, k=2)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "At what exact time was Nicolo Machiavelli born?" --chunk-size 800 --overlap 120 --top-k 2 --show-retrieval
```

```text
Question:
At what exact time was Nicolo Machiavelli born?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 800
Overlap: 120
Top-k: 2
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-introduction-w2733-3531
    BM25 score: 11.68732185
    Section: introduction (front-matter)
    Heading: INTRODUCTION
    Source offsets: [2733, 3531)
    Text: Nicolo Machiavelli was born at Florence on 3rd May 1469. He was the
second son of Bernardo di Nicolo Machiavelli, a lawyer of some repute,
and of Bartolommea di Stefano Nelli, his wife. Both parents were
members of the old Florentine nobility.

His life falls naturally into three periods, each of which singularly
enough constitutes a distinct and important era in the history of
Florence. His youth was concurrent with the greatness of Florence as an
Italian power under the guidance of Lorenzo de’ Medici, Il Magnifico.
The downfall of the Medici in Florence occurred in 1494, in which year
Machiavelli entered the public service. During his official career
Florence was free under the government of a Republic, which lasted
until 1512, when the Medici returned to power, and Machiavelli lost hi
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-editorial-note-w2433-2713
    BM25 score: 11.30320826
    Section: editorial-note (editorial-note)
    Heading: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
    Source offsets: [2433, 2713)
    Text: _ Nicolo Machiavelli, born at Florence on 3rd May 1469. From 1494 to
1512 held an official post at Florence which included diplomatic
missions to various European courts. Imprisoned in Florence, 1512;
later exiled and returned to San Casciano. Died at Florence on 22nd
June 1527._

Accepted answer evidence:
  None

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.
The local quote policy did not admit evidence; this does not prove the book lacks an answer.
Refusal reason: NO_ADMISSIBLE_SENTENCE

Refused: True
Citations: None
```

### known-false-refusal (800/120, k=2)

Command:

```text
python -m src.cli --corpus-file "$env:RAG_PRINCE_FILE" --question "What five errors did Louis XII make in Italy?" --chunk-size 800 --overlap 120 --top-k 2 --show-retrieval
```

```text
Question:
What five errors did Louis XII make in Italy?

Corpus profile: prince-book
Source: The Prince (translator: W. K. Marriott)
Source SHA-256: 948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368
Body SHA-256: 347d9c5737a33224642701e7548fbfd842200f118f84e704b71efd0612078be1
Parser version: prince-sections-v1
Token policy: book-lexical-v1
Admission policy: book-evidence-v1
Chunk size: 800
Overlap: 120
Top-k: 2
BM25 k1/b: 1.50/0.75

Raw ranked candidates:
  Rank: 1
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-office-w6853-7653
    BM25 score: 16.78151224
    Section: office (front-matter)
    Heading: OFFICE — Æt. 25-43—1494-1512
    Source offsets: [6853, 7653)
    Text: ers of his time gives a fair indication of his activities, and
supplies the sources from which he drew the experiences and characters
which illustrate _The Prince_.

His first mission was in 1499 to Catherina Sforza, “my lady of Forli”
of _The Prince_, from whose conduct and fate he drew the moral that it
is far better to earn the confidence of the people than to rely on
fortresses. This is a very noticeable principle in Machiavelli, and is
urged by him in many ways as a matter of vital importance to princes.

In 1500 he was sent to France to obtain terms from Louis XII for
continuing the war against Pisa: this king it was who, in his conduct
of affairs in Italy, committed the five capital errors in statecraft
summarized in _The Prince_, and was consequently driven out. He, also,
it was wh
  Rank: 2
    Chunk ID: pg1232-948dcf754b809ad1164d0f3bb2113e3bb340a1cf5ad6ddb7e8b55610aa318368-p1-c800-o120-chapter-03-w43763-44563
    BM25 score: 15.32555622
    Section: chapter-03 (chapter)
    Heading: CONCERNING MIXED PRINCIPALITIES
    Source offsets: [43763, 44563)
    Text: o was able to drive him, Louis, out
in turn.

The wish to acquire is in truth very natural and common, and men always
do so when they can, and for this they will be praised not blamed; but
when they cannot do so, yet wish to do so by any means, then there is
folly and blame. Therefore, if France could have attacked Naples with
her own forces she ought to have done so; if she could not, then she
ought not to have divided it. And if the partition which she made with
the Venetians in Lombardy was justified by the excuse that by it she
got a foothold in Italy, this other partition merited blame, for it had
not the excuse of that necessity.

Therefore Louis made these five errors: he destroyed the minor powers,
he increased the strength of one of the greater powers in Italy, he
brought in a for

Accepted answer evidence:
  None

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.
The local quote policy did not admit evidence; this does not prove the book lacks an answer.
Refusal reason: NO_ADMISSIBLE_SENTENCE

Refused: True
Citations: None
```

## Preserved homework CLI checks

### Outcome 1 / chunking

Command: `python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 140 --overlap 30 --top-k 2 --show-retrieval`

Observed output excerpt:

```text
Question:
Why are citations important in RAG?

Retrieved evidence:
  Rank: 1
    Chunk ID: tr-doc-1-chunk-0
    Score: 0.6667
    Source: RAG with Citations (tr-doc-1)
    Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare

Answer:
Grounded response based on retrieved context:
[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.

Corpus profile: training-rag

Refused: False
Citations: tr-doc-1-chunk-0
```

### Outcome 2 / top-k 2

Command: `python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 2 --show-retrieval`

Observed output excerpt:

```text
Question:
Why are citations important in RAG?

Retrieved evidence:
  Rank: 1
    Chunk ID: tr-doc-1-chunk-0
    Score: 0.6667
    Source: RAG with Citations (tr-doc-1)
    Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare

Answer:
Grounded response based on retrieved context:
[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.

Corpus profile: training-rag

Refused: False
Citations: tr-doc-1-chunk-0
```

### Outcome 2 / top-k 3

Command: `python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --top-k 3 --show-retrieval`

Observed output excerpt:

```text
Question:
Why are citations important in RAG?

Retrieved evidence:
  Rank: 1
    Chunk ID: tr-doc-1-chunk-0
    Score: 0.6667
    Source: RAG with Citations (tr-doc-1)
    Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transpare

Answer:
Grounded response based on retrieved context:
[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.

Corpus profile: training-rag

Refused: False
Citations: tr-doc-1-chunk-0
```

### Outcome 4 / refusal

Command: `python -m src.cli --corpus-profile training-rag --question "Who won the World Cup in 1958?" --show-retrieval`

Observed output excerpt:

```text
Question:
Who won the World Cup in 1958?

Retrieved evidence:
  None

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: training-rag

Refused: True
Citations: None
```

## Performance

- Machine: `Durut`; OS: `Windows-11-10.0.26300-SP0`; Python: `3.13.7`.
- Timed command: `python -m src.cli --corpus-file PATH --question "What were the five errors of Louis?" --chunk-size 800 --overlap 120 --top-k 3 --show-retrieval`.
- Elapsed time measured separately: 0.376 seconds on this machine, below the five-second target.

## Validation run

- Command: `RAG_PRINCE_FILE=PATH python -m pytest -q` (source path set in the environment).
- Result: 132 passed, 0 skipped, 0 failed; this includes the 32 inherited tests and all 48 real-source acceptance combinations.

## Limits

- `known-false-refusal` asks `What five errors did Louis XII make in Italy?`. The source contains the answer, but strict literal coverage has no aliases for `XII`/`make` and refused it in all four settings. This is a documented recall limitation, not evidence that the book lacks the answer.
- Refusal means the configured policy did not admit a complete sentence. It does not prove no possible answer exists.
- One-sentence lexical coverage, the 2,000-character limit, counted-list grammar, causal/date cues, simple sentence punctuation and this single fingerprinted edition limit recall and generality. Passing the specified gates does not establish universal semantic correctness.
