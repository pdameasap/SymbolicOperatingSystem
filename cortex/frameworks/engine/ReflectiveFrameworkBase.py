# cortex/frameworks/engine/ReflectiveFrameworkBase.py

import time

from .FrameworkBase import FrameworkBase
from ..SymbolicEcho import SymbolicEcho

class ReflectiveFrameworkBase(FrameworkBase):
    """
    v1.1.1 – Adds identity tracing, critique, audit logs,
    and homological mapping for JSON-defined frameworks.
    """

    def __init__(self, name="ReflectiveFramework", version="1.0.0", enable_echo=True, **kwargs):
        super().__init__(name, version)
        self.enable_echo = enable_echo
        self.echo_memory = []
        self.critique_log = []
        self.audit_log = []

        # Standardized symbolic fields
        self.identity_trace = kwargs.get("identity_trace", [])
        self.modulation_inputs = kwargs.get("modulation_inputs", {
            "emotion": {"theta": 0.0, "phi": 0.0, "intensity": 0.0},
            "social_fit": 0.0,
            "symbolic_resonance": 0.0
        })
        self.recursive_layer = kwargs.get("recursive_layer", 0)
        self.homological_map = kwargs.get("homological_map", {})

        # Merge in reflective capabilities
        base_caps = [
            "record_symbolic_echo",
            "self_critique",
            "evaluate_symbolic_resonance",
            "detect_symbolic_disruption",
            "report_resonance_profile"
        ]
        existing = getattr(self, "capabilities", [])
        self.capabilities = list(set(existing + base_caps))

    def introspection_available(self):
        return hasattr(self, "introspect")

    def introspect(self, question, unit=None, model="default"):
        import openai
        from openai.error import (
            OpenAIError, APIError, RateLimitError, Timeout,
            AuthenticationError, InvalidRequestError
        )

        response_obj = {"score": 0.0, "rationale": "Unknown error."}
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a reflective reasoning engine evaluating symbolic identity questions."
                    },
                    {"role": "user", "content": question}
                ],
                temperature=0.2,
                max_tokens=32
            )
            answer = response.choices[0].message["content"].strip()
            response_obj["score"] = (
                float(answer) if answer.replace(".", "", 1).isdigit() else 0.0
            )
            response_obj["rationale"] = answer

        except RateLimitError as rle:
            response_obj["rationale"] = f"Rate limit exceeded: {rle}"
        except Timeout as te:
            response_obj["rationale"] = f"Request timed out: {te}"
        except AuthenticationError as ae:
            response_obj["rationale"] = f"Authentication failed: {ae}"
        except InvalidRequestError as ire:
            response_obj["rationale"] = f"Invalid request: {ire}"
        except APIError as api_err:
            response_obj["rationale"] = f"API error: {api_err}"
        except OpenAIError as oe:
            response_obj["rationale"] = f"OpenAI error: {oe}"
        except Exception as e:
            response_obj["rationale"] = f"Unhandled error: {e}"
        finally:
            return response_obj

    def query(self, question, unit=None, defer=True, model="default", metadata=None):
        metadata = metadata or {}
        log_entry = {
            "question": question,
            "unit": unit,
            "model": model,
            "defer": defer,
            "timestamp": time.time(),
            "context": metadata
        }
        response_obj = {"score": 0.0, "rationale": "Deferred or unavailable."}

        try:
            if hasattr(self, "context_prefix") and self.context_prefix:
                question = f"{self.context_prefix.strip().rstrip('.')}. {question}"

            if defer or not self.introspection_available():
                self.log_deferred_question(log_entry)
            else:
                response_obj = self.introspect(question, unit, model=model)
                log_entry["response"] = response_obj
                self.audit_log.append(log_entry)

        except Exception as e:
            log_entry["error"] = str(e)
            self.audit_log.append(log_entry)
        finally:
            return response_obj

    def log_deferred_question(self, entry):
        self.audit_log.append({**entry, "status": "deferred"})

    def record_symbolic_echo(self, event, z_trace, weight=1.0, foundational=False):
        echo = SymbolicEcho(event, z_trace, weight=weight, foundational=foundational)
        self.echo_memory.append(echo)

    def self_critique(self, trace, expected_reference=None):
        evaluated = self.evaluate_identity_shell(trace)
        meta_score = self.calculate_meta_alignment(trace, evaluated, expected_reference)
        log = {
            "trace_id": id(trace),
            "evaluation": evaluated,
            "reference": expected_reference,
            "meta_score": meta_score,
            "timestamp": time.time()
        }
        self.critique_log.append(log)
        return log

    def calculate_meta_alignment(self, trace, evaluated, reference):
        if not reference:
            return 1.0
        deltas = [
            abs(evaluated.get(z, 0) - reference.get(z, 0))
            for z in evaluated
            if z in reference
        ]
        avg_div = sum(deltas) / len(deltas) if deltas else 0.0
        return round(1.0 - min(avg_div, 1.0), 3)

    def evaluate_symbolic_resonance(self, trace):
        if not trace:
            return {}
        return {
            z: round(sum(s.get(z, 0) for s in trace) / len(trace), 3)
            for z in trace[0].keys()
        }

    def detect_symbolic_disruption(self, trace):
        return [i for i, s in enumerate(trace) if s.get("Z14", 0) > 0.8]

    def report_resonance_profile(self, trace):
        return {
            "resonance_score": self.evaluate_symbolic_resonance(trace),
            "disruption_events": self.detect_symbolic_disruption(trace)
        }

    def report_self_coherence(self, trace):
        critique = self.self_critique(trace)
        return {
            "identity_lock": critique["meta_score"] >= 0.85,
            "coherence_score": critique["meta_score"],
            "evaluation": critique["evaluation"]
        }

    def child_evaluate(self, unit, z_values):
        if self.enable_echo:
            self.record_symbolic_echo(unit, z_values)
        return z_values

    def reflect(self, unit):
        """
        Perform a reflective pass over `unit`, returning the
        SymbolicEcho analysis.
        """
        echo = SymbolicEcho()
        return echo.process(unit)
