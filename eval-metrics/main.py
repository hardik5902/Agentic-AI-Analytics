import re
from collections import Counter

import numpy as np
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_md")

_WORD_RE = re.compile(r"[a-z0-9']+")


# --- Tokenization ---


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens for overlap metrics."""
    return _WORD_RE.findall(text.lower())


def tokenize_no_stop(text: str) -> list[str]:
    """Lowercase content-word tokens (no stopwords or punctuation)."""
    return [t.lower_ for t in nlp(text) if not t.is_stop and not t.is_punct]


# --- Term Overlap Metrics ---


def jaccard(a_tokens: list[str], b_tokens: list[str]) -> float:
    a, b = set(a_tokens), set(b_tokens)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def token_f1(pred_tokens: list[str], ref_tokens: list[str]) -> float:
    if not pred_tokens and not ref_tokens:
        return 1.0
    if not pred_tokens or not ref_tokens:
        return 0.0
    pc, rc = Counter(pred_tokens), Counter(ref_tokens)
    overlap = sum((pc & rc).values())
    precision = overlap / sum(pc.values())
    recall = overlap / sum(rc.values())
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


# --- ROUGE ---


def _ngrams(tokens: list[str], n: int) -> list[tuple]:
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _f1(precision: float, recall: float) -> float:
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def rouge_n(candidate: str, reference: str, n: int, tok=tokenize) -> float:
    c_tok, r_tok = tok(candidate), tok(reference)
    if not c_tok and not r_tok:
        return 1.0
    if not c_tok or not r_tok:
        return 0.0
    c_ngr, r_ngr = Counter(_ngrams(c_tok, n)), Counter(_ngrams(r_tok, n))
    overlap = sum((c_ngr & r_ngr).values())
    return _f1(overlap / sum(c_ngr.values()), overlap / sum(r_ngr.values()))


def _lcs_length(a: list[str], b: list[str]) -> int:
    m, n = len(a), len(b)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            tmp = dp[j]
            dp[j] = prev + 1 if a[i - 1] == b[j - 1] else max(dp[j], dp[j - 1])
            prev = tmp
    return dp[n]


def rouge_l(candidate: str, reference: str, tok=tokenize) -> float:
    c_tok, r_tok = tok(candidate), tok(reference)
    if not c_tok and not r_tok:
        return 1.0
    if not c_tok or not r_tok:
        return 0.0
    lcs = _lcs_length(c_tok, r_tok)
    return _f1(lcs / len(c_tok), lcs / len(r_tok))


# --- Semantic Similarity (spaCy word vectors) ---


def text_vector(text: str, content_only: bool = False) -> np.ndarray:
    """Average word vector. If content_only, skip stopwords and punctuation."""
    doc = nlp(text)
    if content_only:
        tokens = [t for t in doc if t.has_vector and not t.is_stop and not t.is_punct]
    else:
        tokens = [t for t in doc if t.has_vector]
    if not tokens:
        return np.zeros(nlp.vocab.vectors_length)
    return np.mean([t.vector for t in tokens], axis=0)


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    denom = np.linalg.norm(u) * np.linalg.norm(v)
    if denom == 0:
        return 0.0
    return float(np.dot(u, v) / denom)


# --- Scoring ---


def score_candidates(
    reference: str,
    candidates: dict[str, str],
    tok=tokenize,
    content_only: bool = False,
) -> pd.DataFrame:
    ref_tokens = tok(reference)
    ref_vec = text_vector(reference, content_only)

    rows = []
    for name, cand in candidates.items():
        cand_tokens = tok(cand)
        rows.append(
            {
                "candidate": name,
                "jaccard": jaccard(cand_tokens, ref_tokens),
                "token_f1": token_f1(cand_tokens, ref_tokens),
                "rouge1": rouge_n(cand, reference, 1, tok),
                "rouge2": rouge_n(cand, reference, 2, tok),
                "rougeL": rouge_l(cand, reference, tok),
                "semantic": cosine_similarity(
                    text_vector(cand, content_only), ref_vec
                ),
            }
        )

    return pd.DataFrame(rows).sort_values("semantic", ascending=False)


# --- Apollo 11 Example ---

reference = (
    "The Apollo 11 mission's primary purpose was to achieve the national goal "
    "of landing humans on the Moon and returning them safely to Earth. Key outcomes "
    "included astronauts Neil Armstrong and Buzz Aldrin collecting the first lunar "
    "samples, deploying scientific experiments on the lunar surface, and demonstrating "
    "U.S. technological supremacy during the Cold War."
)

candidates = {
    "A (inaccurate)": (
        "The Apollo 11 mission's primary purpose was to land humans on Mars. "
        "Key outcomes included astronauts Neil Armstrong and Buzz Aldrin collecting "
        "the first Martian samples and deploying scientific experiments on the Martian surface."
    ),
    "B (correct paraphrase)": (
        "The main goal of Apollo 11 was to successfully land a crew on the Moon "
        "and ensure their safe return. During the mission, the astronauts gathered "
        "moon rocks and set up science equipment, which was a major victory for "
        "the U.S. in the Cold War."
    ),
    "C (incomplete)": (
        "The Apollo 11 mission landed Neil Armstrong and Buzz Aldrin on the Moon."
    ),
    "D (irrelevant)": (
        "The Apollo 11 mission was a landmark achievement in aeronautics, leading "
        "to significant advancements in aircraft design and commercial airline safety "
        "protocols that are still in use today."
    ),
}

print("=== All tokens ===")
df = score_candidates(reference, candidates)
print(df.round(4).to_string(index=False))

print()
print("=== Stopwords removed ===")
df_no_stop = score_candidates(
    reference, candidates, tok=tokenize_no_stop, content_only=True
)
print(df_no_stop.round(4).to_string(index=False))
