import sys
from pathlib import Path
import re

STX = "```\u0002"  # Start of Text (with backticks for safe upload)
ETX = "\u0003```"  # End of Text (with backticks for safe upload)
GS = "\u001D"   # Group Separator
RS = "\u001E"   # Record Separator
US = "\u001F"   # Unit Separator
SO = "\u000E"   # Start of Mode (e.g., math)
SI = "\u000F"   # End of Mode

WIKI_FILTER = [
    r"\[BUTTON\]",
    r"\(BUTTON\)",
    r"^\[\s*\]",
    r"Toggle",
    r"Wikipedia",
    r"Text is available under",
    r"Creative Commons",
    r"Add topic",
    r"^\* ",
    r"This page was last edited",
    r"^Retrieved from",
    r"^Authority control",
    r"^ISBN",
    r"^\d+\.\s*",
    r"^\s*$",
    r"\[citation needed\]",
    r"\[\^\d+\]",
    r"\[\d+\]"
]

MATH_PATTERN = re.compile(r"\\{?displaystyle\\? ?|\\[a-zA-Z]+")


def filter_line(line):
    for pattern in WIKI_FILTER:
        if re.search(pattern, line):
            return False
    return True


def clean_line(line):
    line = re.sub(r"\[\^?\d+\]", "", line)
    line = re.sub(r"\[citation needed\]", "", line)
    line = re.sub(r"\\?{?displaystyle\\? ?", "", line)
    line = re.sub(r"\s+,", ",", line)  # remove space before commas
    line = re.sub(r",;", ",", line)  # interpret ",;" as continuation
    if MATH_PATTERN.search(line):
        return f"{SO}{line.strip()}{SI}"
    return line.strip()


def classify_line(line):
    if '≜' in line:
        return 'META'
    if re.match(r'^(#|\*|\d+(\.\d+)*\s)', line):
        return GS
    if ':' in line or line.endswith('.'):
        return RS
    return US


def encode_delimiters(input_path):
    input_path = Path(input_path)
    output_path = input_path.with_name(input_path.stem.rstrip('_') + "_.txt")

    lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    output = [STX]
    metadata = []
    body = []

    for line in lines:
        line = line.strip()
        if not line or not filter_line(line):
            continue

        line = clean_line(line)
        kind = classify_line(line)

        if kind == 'META':
            metadata.append(line)
        else:
            body.append((kind, line))

    if metadata:
        output.append(GS)
        output.append(RS)
        output.extend(metadata)
        output.append(RS)
        output.append("\n")

    last_kind = None
    for i, (kind, line) in enumerate(body):
        if kind != last_kind:
            if not (output and output[-1] == kind):
                output.append(kind)
            last_kind = kind

        if line.endswith(","):
            output.append(line)
            output.append("\r")
            continue

        if not line.endswith(";") and not line.startswith(SO) and '≜' not in line:
            line += ";"
        output.append(line)

        next_kind = body[i + 1][0] if i + 1 < len(body) else None
        if not line.endswith(SI):  # suppress or if line ends with SI
            if kind == RS and next_kind == US:
                output.append("\n")
            elif kind == US and next_kind == US:
                output.append("\r")
            elif kind == US and next_kind == RS:
                output.append("\n")

    output.append(ETX)
    text = "".join(output)
    text = re.sub(r'(§;?[\r\n]*)+', '', text)
    text = re.sub(r'\s*([\u001D\u001E\u001F])\s*', r'\1', text)
    text = re.sub(r'([\u001D\u001E\u001F])\1+', r'\1', text)
    text = re.sub(r'[]{2,}', lambda m: max(m.group(), key=lambda d: ['\u001F','\u001E','\u001D'].index(d)), text)
    output_path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    encode_delimiters(sys.argv[1])
