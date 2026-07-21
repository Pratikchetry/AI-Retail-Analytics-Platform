"""
Phase 5.5 — AI Retail Intelligence Platform
Context Compressor Node.

Context engineering layer 1: what comes IN.
Re-ranks retrieved context blocks by keyword overlap with the question,
keeps only the top-3 most relevant, dedupes near-identical blocks, and
drops noise. Deterministic — no LLM call (free on rate limits).
"""

import re
from src.utils.logger import get_logger
from src.langgraph.state import AgentState

log = get_logger(__name__)

# Words that add noise, not signal (excluded from relevance scoring)
STOPWORDS = {
    "what", "which", "why", "how", "the", "was", "were", "did", "show",
    "give", "tell", "about", "from", "into", "with", "that", "this",
    "have", "has", "had", "will", "would", "should", "could", "for",
    "and", "are", "you", "our", "out", "any", "get", "see", "find",
}


def _question_keywords(question: str) -> set:
    """Extract meaningful keywords from the question."""
    words = re.findall(r"[a-zA-Z_]{3,}", question.lower())
    return {w for w in words if w not in STOPWORDS}


def _score_block(block: str, keywords: set) -> int:
    """Score a context block by how many question keywords it contains."""
    block_lower = block.lower()
    return sum(1 for kw in keywords if kw in block_lower)


def _dedupe(blocks: list) -> list:
    """Drop blocks that are near-duplicates (>80% text overlap with an earlier block)."""
    unique = []
    for block in blocks:
        is_dup = False
        for existing in unique:
            # Simple overlap check: shared signature words
            new_words = set(re.findall(r"[a-zA-Z_]{4,}", block.lower()))
            old_words = set(re.findall(r"[a-zA-Z_]{4,}", existing.lower()))
            if new_words and old_words:
                overlap = len(new_words & old_words) / len(new_words)
                if overlap > 0.8:
                    is_dup = True
                    break
        if not is_dup:
            unique.append(block)
    return unique


def compress_context_node(state: AgentState) -> dict:
    """Compress retrieved context to top-3 relevant, deduplicated blocks."""
    question = state.get("question", "")
    context = state.get("context", "")

    if not context or len(context) < 50:
        log.info("Compressor: minimal context, passing through")
        return {"context": context}

    keywords = _question_keywords(question)

    # Split the concatenated context into individual blocks
    # Each block starts with "— Context Block N —"
    raw_blocks = re.split(r"— Context Block \d+ —", context)
    raw_blocks = [b.strip() for b in raw_blocks if b.strip()]

    # Score each block
    scored = [(b, _score_block(b, keywords)) for b in raw_blocks]

    # Sort by relevance descending, keep top blocks
    scored.sort(key=lambda x: x[1], reverse=True)

    # Keep blocks with score > 0, max 3; fall back to top-1 if all scored 0
    relevant = [b for b, s in scored if s > 0][:3]
    if not relevant:
        relevant = [scored[0][0]] if scored else []

    # Dedupe near-identical blocks
    relevant = _dedupe(relevant)

    compressed = "\n\n".join(f"— Context Block {i+1} —\n{b}" for i, b in enumerate(relevant))

    original_len = len(context)
    compressed_len = len(compressed)
    reduction = (1 - compressed_len / original_len) * 100 if original_len else 0

    log.info("Compressor: %d blocks -> %d | %d chars -> %d chars (-%.0f%%)",
             len(raw_blocks), len(relevant), original_len, compressed_len, reduction)

    return {"context": compressed}