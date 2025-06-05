class SymbolicEcho:
    """Simple echo object used by ReflectiveFrameworkBase."""

    def __init__(self, event=None, z_trace=None, weight=1.0, foundational=False):
        self.event = event
        self.z_trace = z_trace or []
        self.weight = weight
        self.foundational = foundational

    def process(self, unit):
        """Return a basic analysis structure."""
        return {
            "input": unit,
            "weight": self.weight,
            "foundational": self.foundational,
            "trace": list(self.z_trace),
        }

