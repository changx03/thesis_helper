# Helper functions for my thesis

## Feature 1: Merge multiple LaTex bibliography files

LaTex will report error when bibliography contains multiple entries with the same key.
`merge.py` merges multiple `*.bib` files into one.

### Use case

When `./data/bib` contains multiple bib files. The file name doesn't matter, as long as the extension uses `.bib`.

```python
python3 ./merge.py -i "./data/bib/" -o "bibliography.bib"
```

Where `-i` is the input directory (not the actual bib file), and `-o` is the output file (default value is `bibliography.bib`).
