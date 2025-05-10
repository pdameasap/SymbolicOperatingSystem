
# File: cortex/frameworks/engine/EvaluativeFrameworkBase.py

from ReflectiveFrameworkBase import ReflectiveFrameworkBase

class EvaluativeFrameworkBase(ReflectiveFrameworkBase):
    '''
    SymbolicOperatingSystem v1.0.0
    EvaluativeFrameworkBase: Z₁–Z₁₅ symbolic evaluation for cognitive operating systems.
    Inherit from this class to gain universal symbolic recursion and reflection.
    '''

    def evaluate(self, evaluand):
        z_values = {}
        for i in range(1, 16):
            rule = f"Z{i}"
            question_attr = f"queryZ{i}"
            question = getattr(self, question_attr, f"No question defined for {rule}")
            contextual_question = f"In the context of {self.name}, {question}"
            z_values[rule] = self.query(contextual_question, evaluand, metadata={"rule": rule})

        return self.child_evaluate(evaluand, z_values)
