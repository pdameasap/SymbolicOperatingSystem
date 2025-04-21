from cortex.frameworks.EmojiFramework import EmojiFramework
from cortex.frameworks.SymbolicMathFramework import SymbolicMathFramework
from cortex.frameworks.engine.JsonFramework import JsonFramework  # fallback, if needed

class SymbolicExpressionResolver:
    '''
    Interprets symbolic math expressions involving Z-glyphs, emoji, and operators,
    routing to appropriate framework modules and composing resonance profiles.
    '''

    def __init__(self):
        self.math = SymbolicMathFramework()
        self.emoji = EmojiFramework()  # now routed through formal framework interface

    def resolve(self, expression: str) -> dict:
        '''
        Parses and resolves symbolic expressions with operators and evaluands.
        Example: "%∂(Z3 ∘ 😭)" or "%emoji|😭"
        '''
        try:
            if expression.startswith("emoji|"):
                raw = expression[len("emoji|"):].strip()
                return {"result": self.emoji.child_evaluate(raw)}

            if "(" not in expression or ")" not in expression:
                return {"error": "Malformed expression: missing parentheses."}

            operator, body = expression.split("(", 1)
            body = body.rstrip(")")

            args = [x.strip() for x in body.split(",")]
            resolved_zs = []

            for arg in args:
                if arg.startswith("Z"):
                    resolved_zs.append(arg)
                elif arg in self.emoji.list_supported():
                    emoji_eval = self.emoji.child_evaluate(arg)
                    if isinstance(emoji_eval, list):
                        resolved_zs.extend([z for obj in emoji_eval for z in obj.get("z_axis_profile", {}).keys()])
                    else:
                        resolved_zs.extend(emoji_eval.get("z_axis_profile", {}).keys())
                elif arg in self.math.framework.get("operators", {}):
                    resolved_zs.append(arg)
                else:
                    return {"error": f"Unrecognized argument: {arg}"}

            return self.math.evaluate_operator(operator, resolved_zs)

        except Exception as e:
            return {"error": str(e)}

    def explain(self, expression: str) -> str:
        try:
            if expression.startswith("emoji|"):
                raw = expression[len("emoji|"):].strip()
                eval_result = self.emoji.child_evaluate(raw)
                if isinstance(eval_result, list):
                    return ", ".join([e.get("description", "") for e in eval_result])
                return eval_result.get("description", "")

            operator, _ = expression.split("(", 1)
            return self.math.explain_operator(operator.strip())
        except:
            return "Invalid expression."

    def run_examples(self):
        return {
            "%emoji|😭": self.resolve("emoji|😭"),
            "%emoji|❤️🧠": self.resolve("emoji|❤️🧠"),
            "%∑(Z1, Z3, 😭)": self.resolve("∑(Z1, Z3, 😭)"),
            "%∂(Z5 ∘ 😭)": self.resolve("∂(Z5 ∘ 😭)")
        }
