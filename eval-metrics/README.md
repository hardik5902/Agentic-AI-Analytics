# Eval Metrics

Demonstrates term overlap (Jaccard, Token F1), ROUGE (1, 2, L), and semantic similarity (spaCy word vectors) for evaluating candidate answers against a golden reference. Uses the Apollo 11 example from the evaluation lecture.

## Running

```bash
uv run main.py
```

The first run will download the spaCy `en_core_web_md` model (~31 MB).
