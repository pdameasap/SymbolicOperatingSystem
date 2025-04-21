from cortex.interpreter.SymbolicExpressionResolver import SymbolicExpressionResolver

class SECLInterpreter:
    '''
    Top-level interpreter for SECL (Symbolic
    Expressive Command Language) Routes
    symbolic commands to appropriate evaluators.
    '''

    def __init__(self):
        self.resolver = SymbolicExpressionResolver()

    def interpret(self, command: str) -> dict:
        '''
        Interpret a SECL expression like
        "%∂(Z3 ∘ 😭)" or "%emoji|😭"
        '''
        if command.startswith("%"):
            body = command[1:].strip()
            return self.resolver.resolve(body)

        if command.startswith("⊢"):
            # Lensing or axis selection not implemented here
            return {"note": "Axis focus detected (⊢), but interpretation logic not included in this module."}
        
        return {"error": "Unrecognized SECL command."}

    def explain(self, command: str) -> str:
        '''
        Provide a symbolic explanation for
        an expression.
        '''
        if command.startswith("%"):
            body = command[1:].strip()
            return self.resolver.explain(body)
        return "Invalid or unsupported expression for explanation."
