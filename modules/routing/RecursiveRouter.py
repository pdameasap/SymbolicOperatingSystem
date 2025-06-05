
# RecursiveRouter v1.0.0
# Symbolic switchboard for routing symbolic units to the correct ConvergenceEngine

from cortex.frameworks.engine.ReflectiveFrameworkBase import ReflectiveFrameworkBase

class RecursiveRouter(ReflectiveFrameworkBase):
    # Routes symbolic units not to frameworks, but to convergence routers

    def __init__(self):
        super().__init__(name="RecursiveRouter", version="1.0.0")
        self.router_mesh = {}

    def register_router(self, tag_or_field, convergence_engine):
        self.router_mesh[tag_or_field] = convergence_engine

    def route(self, symbolic_unit):
        result = {}

        # Try routing by tag first
        for tag in symbolic_unit.get("tags", []):
            if tag in self.router_mesh:
                result[tag] = self.router_mesh[tag].route(symbolic_unit)

        # Then by Z-rule dominance
        if "Z_dominant" in symbolic_unit:
            z_dom = symbolic_unit["Z_dominant"]
            if z_dom in self.router_mesh:
                result[z_dom] = self.router_mesh[z_dom].route(symbolic_unit)

        # Or by echo span, if known
        if "echo_span" in symbolic_unit:
            span = symbolic_unit["echo_span"]
            if span in self.router_mesh:
                result[span] = self.router_mesh[span].route(symbolic_unit)

        return result or {"unrouted": symbolic_unit}

    def snapshot(self):
        return {
            "routers": list(self.router_mesh.keys()),
            "active": [r.name for r in self.router_mesh.values()]
        }
