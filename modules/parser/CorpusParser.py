# File: modules/parser/CorpusParser.py

from SymbolicOperatingSystem.modules.parser.SemanticParser import SemanticParser

class CorpusParser(SemanticParser):
    def __init__(self):
        super().__init__()

    def parse_lines(self, lines):
        parsed_lines = []
        z_summary = {}

        for i, line in enumerate(lines):
            parsed = self.parse_sentence(line)
            glosses = [
                {"word": w, "Z": g["Z"], "tag": g["tag"]}
                for w, g in zip(parsed["tokens"], parsed["gloss"])
            ]
            z_tags = [g["Z"] for g in parsed["gloss"] if g["Z"]]

            for z in z_tags:
                z_summary[z] = z_summary.get(z, 0) + 1

            parsed_lines.append({
                "line_number": i + 1,
                "text": line,
                "z_tags": z_tags,
                "glosses": glosses
            })

        return {
            "lines": parsed_lines,
            "z_summary": z_summary
        }
