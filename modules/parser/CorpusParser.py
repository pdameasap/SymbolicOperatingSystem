import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

document = [
    "I am in need of a programmer and a grammarian.",
    "A theoretical physicist would also be nice.",
    "Perhaps a language designer, too.",
    "Warmth and elegance are especially important."
]

cp = CorpusParser()
parsed = cp.parse_lines(document)

for line in parsed["lines"]:
    print(f"\nLine {line['line_number']}: {line['text']}")
    print("Z-Tags:", line["z_tags"])
    for gloss in line["glosses"]:
        print(f"  {gloss['word']:12} → Z: {gloss['Z'] or '-'} | Tag: {gloss['tag'] or '-'}")

print("\n📊 Total Z-Summary:")
for z, count in parsed["z_summary"].items():
    print(f"  {z}: {count}")
