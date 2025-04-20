from cortex.frameworks.engine.JsonFramework import JsonFramework

class EmojiFramework(JsonFramework):
    '''
    EmojiFramework v1.0.0
    Symbolic evaluator for emoji, based on Z-axis profiles loaded from JSON.
    Inherits from JsonFramework for file loading and evaluation structure.
    Supports string, list, and recursive emoji event expansion.
    '''

    def get_z_profile(self, emoji: str) -> dict:
        return self.framework.get("emoji_map", {}).get(emoji, {}).get("z_axis_profile", {})

    def explain(self, emoji: str) -> str:
        return self.framework.get("emoji_map", {}).get(emoji, {}).get("description", "Unknown emoji.")

    def get_symbolic_type(self, emoji: str) -> str:
        return self.framework.get("emoji_map", {}).get(emoji, {}).get("symbolic_type", "unknown")

    def list_supported(self) -> list:
        return list(self.framework.get("emoji_map", {}).keys())

    def _evaluate_one(self, emoji: str) -> dict:
        result = {
            "emoji": emoji,
            "description": "",
            "symbolic_type": "null",
            "z_axis_profile": {"Z14": 1.0}
        }

        entry = self.framework.get("emoji_map", {}).get(emoji)
        if entry:
            result["description"] = entry.get("description", "")
            result["symbolic_type"] = entry.get("symbolic_type", "unknown")
            result["z_axis_profile"] = entry.get("z_axis_profile", {})

        return result

    def child_evaluate(self, evaluand, context=None):
        if isinstance(evaluand, list):
            return [self.child_evaluate(e) for e in evaluand]
        elif isinstance(evaluand, str):
            emoji_map = self.framework.get("emoji_map", {})
            if evaluand in emoji_map:
                return [self._evaluate_one(evaluand)]
            # If string contains only supported emoji, split and evaluate
            if all(char in emoji_map for char in evaluand):
                return [self._evaluate_one(char) for char in evaluand]
        # Fallback to null resonance
        return [{
            "emoji": evaluand,
            "description": "Undefined symbol",
            "symbolic_type": "null",
            "z_axis_profile": {"Z14": 1.0}
        }]
