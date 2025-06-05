import sys
from pathlib import Path
import re
from statistics import mean


def measure_coherence(lines):
    scores = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            scores.append(-1.0)
            continue

        tokens = re.findall(r'\b\w+\b', line)
        unique_ratio = len(set(tokens)) / (len(tokens) + 1)

        symbol_weights = {
            '≜': 1.0, '⊢': 0.8, '%': 0.5, '◐': 0.5, '□': 0.7, '◇': 0.7,
            ';': 0.3, ':': 0.2, '.': 0.1, '—': 0.2, '→': 0.3
        }
        symbol_score = sum(symbol_weights.get(c, 0) for c in line) / (len(line) + 1)

        recursion_signals = ['if', 'then', 'therefore', 'hence', 'thus', 'implies']
        recursive_boost = sum(1 for t in tokens if t.lower() in recursion_signals) * 0.3

        coherence = unique_ratio + symbol_score + recursive_boost
        scores.append(coherence)
    return scores


def extract_clean_content(lines, scores):
    avg_score = mean([s for s in scores if s >= 0])
    clean_lines = []
    last_score = 0.0

    for line, score in zip(lines, scores):
        if score < avg_score * 1.05:
            last_score = score
            continue

        # Insert delimiter if this is a jump in signal strength
        if clean_lines and score - last_score > 0.5:
            clean_lines.append("§")
        clean_lines.append(line.strip())
        last_score = score

    return clean_lines


def analyze_signal(input_path):
    input_path = Path(input_path)
    output_path = input_path.parent / f"_{input_path.name}"

    lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    scores = measure_coherence(lines)
    clean_lines = extract_clean_content(lines, scores)

    output_path.write_text("\n".join(clean_lines), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    analyze_signal(sys.argv[1])
