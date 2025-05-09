
# File: cortex/interpreter/SigilParser.py

from cortex.interpreter.SECLInterpreter import SECLInterpreter

class SigilParser:
    '''
    Parses compressed .sigil-style symbolic expressions and expands them to SECL-compatible form.
    Example: ⊢⌶ %∂(⥀∘😭)
    '''
    def __init__(self):
        self.interpreter = SECLInterpreter()

    def parse(self, line: str) -> dict:
        # Interpret a full .sigil line, handling optional ⊢ axis lensing and % expressions.
        line = line.strip()
        focus = None
        if line.startswith("⊢"):
            focus = line[1]  # Axis glyph (e.g. ⌶)
            line = line[2:].strip()

        if line.startswith("%"):
            result = self.interpreter.interpret(line)
            if focus:
                result["lens"] = focus  # Placeholder: no evaluation logic for ⊢ yet
            return result

        return {"error": "Unsupported .sigil syntax."}

    def explain(self, line: str) -> str:
        # Explain a symbolic line with optional axis lens.
        if "%" in line:
            return self.interpreter.explain(line.strip())
        return "Unsupported .sigil explanation."
