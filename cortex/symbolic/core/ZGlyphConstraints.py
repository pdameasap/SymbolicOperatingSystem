"""
Versare Z-Glyph Constraint System

This module demonstrates how the dual constraint system (mathematical definitions and sixfold descriptions)
for Z-Glyphs can be formalized in code. It provides a framework for representing Z-Glyphs as computational
objects that encapsulate both their operational logic and semantic field.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Any, Callable, Optional, Union, Tuple
import math


class SixfoldAspect:
    """Represents the sixfold description of a Z-Glyph aspect."""
    
    def __init__(self, 
                 primary: str,
                 aspects: List[str]):
        """
        Initialize a sixfold aspect.
        
        Args:
            primary: The primary name/description of the aspect
            aspects: List of the six aspects/perspectives
        """
        self.primary = primary
        self.aspects = aspects
        
        # Ensure we have exactly six aspects
        if len(aspects) != 6:
            raise ValueError(f"SixfoldAspect must have exactly 6 aspects, got {len(aspects)}")
    
    def __str__(self) -> str:
        """String representation of the sixfold aspect."""
        return f"{self.primary}: {' — '.join(self.aspects)}"
    
    def contains_semantic(self, concept: str) -> bool:
        """
        Check if the given concept is semantically contained within this aspect.
        
        Args:
            concept: The concept to check
            
        Returns:
            True if the concept is contained in the primary or any of the aspects
        """
        concept_lower = concept.lower()
        if concept_lower in self.primary.lower():
            return True
        
        return any(concept_lower in aspect.lower() for aspect in self.aspects)


class MathematicalDefinition:
    """Represents the mathematical definition of a Z-Glyph."""
    
    def __init__(self, 
                 formula: str,
                 variables: Dict[str, str],
                 implementation: Optional[Callable] = None):
        """
        Initialize a mathematical definition.
        
        Args:
            formula: The mathematical formula as a string
            variables: Dictionary mapping variable symbols to their descriptions
            implementation: Optional callable implementing the mathematical operation
        """
        self.formula = formula
        self.variables = variables
        self.implementation = implementation
    
    def __str__(self) -> str:
        """String representation of the mathematical definition."""
        return self.formula
    
    def evaluate(self, *args, **kwargs) -> Any:
        """
        Evaluate the mathematical operation if an implementation is provided.
        
        Returns:
            Result of the mathematical operation
        """
        if self.implementation is None:
            raise NotImplementedError(f"No implementation provided for formula: {self.formula}")
        
        return self.implementation(*args, **kwargs)


class ZGlyph(ABC):
    """Base class for Z-Glyphs in the Versare language."""
    
    def __init__(self, 
                 index: int,
                 symbol: str,
                 name: str,
                 emoji: Optional[str] = None,
                 core_description: str = "",
                 math_definition: Optional[MathematicalDefinition] = None,
                 sixfold_aspect: Optional[SixfoldAspect] = None):
        """
        Initialize a Z-Glyph.
        
        Args:
            index: The Z-Glyph index (1-16)
            symbol: The Unicode symbol representing this glyph
            name: The name of the glyph
            emoji: Optional emoji representation
            core_description: Core description of the glyph
            math_definition: Mathematical definition of the glyph
            sixfold_aspect: Sixfold aspect description of the glyph
        """
        self.index = index
        self.symbol = symbol
        self.name = name
        self.emoji = emoji
        self.core_description = core_description
        self.math_definition = math_definition
        self.sixfold_aspect = sixfold_aspect
    
    def __str__(self) -> str:
        """String representation of the Z-Glyph."""
        return f"Z₍{self.index}₎ ({self.name}): {self.symbol}"
    
    @property
    def subscript_notation(self) -> str:
        """Return the Z-Glyph in subscript notation (e.g., Z₁)."""
        # Convert the index to subscript
        subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return f"Z{str(self.index).translate(subscripts)}"
    
    @abstractmethod
    def operate(self, *args, **kwargs) -> Any:
        """
        Apply the Z-Glyph operation to the given arguments.
        
        This method must be implemented by concrete Z-Glyph classes.
        """
        pass
    
    def validate_semantic_coherence(self, operation_result: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that an operation result is semantically coherent with this Z-Glyph.
        
        Args:
            operation_result: The result of applying this Z-Glyph's operation
            context: Contextual information about the operation
            
        Returns:
            True if the operation result is semantically coherent with this Z-Glyph
        """
        # Default implementation - subclasses should override with specific logic
        return True
    
    def is_semantically_related(self, concept: str) -> bool:
        """
        Check if a concept is semantically related to this Z-Glyph.
        
        Args:
            concept: The concept to check
            
        Returns:
            True if the concept is semantically related to this Z-Glyph
        """
        if self.sixfold_aspect is None:
            return False
        
        return self.sixfold_aspect.contains_semantic(concept)


# Example implementation of Z₁ (Structure/Alpha)
class Z1_Structure(ZGlyph):
    """Z₁: Structure (Alpha) - The Form That Begins"""
    
    def __init__(self):
        # Define the mathematical implementation
        def structure_function(system, time=None):
            """
            Extract or assert the structure of a system.
            
            Args:
                system: The system to analyze
                time: Optional time parameter
                
            Returns:
                The structure of the system
            """
            if hasattr(system, 'structure'):
                return system.structure
            elif hasattr(system, 'get_structure'):
                return system.get_structure(time) if time is not None else system.get_structure()
            elif isinstance(system, dict) and 'structure' in system:
                return system['structure']
            else:
                # Default implementation for simple types
                if isinstance(system, (list, tuple, set)):
                    return {'type': type(system).__name__, 'elements': len(system)}
                elif isinstance(system, dict):
                    return {'type': 'dict', 'keys': list(system.keys())}
                elif isinstance(system, str):
                    return {'type': 'string', 'length': len(system)}
                else:
                    return {'type': type(system).__name__}
        
        # Create the mathematical definition
        math_def = MathematicalDefinition(
            formula="Z₁ = S(t)",
            variables={"S": "Structure", "t": "time/state"},
            implementation=structure_function
        )
        
        # Create the sixfold aspect
        sixfold = SixfoldAspect(
            primary="Form",
            aspects=[
                "Form — That which differentiates being from void",
                "Shape — The presence of geometry and constraint",
                "Order — Arrangement that yields identity",
                "Framework — The scaffolding of interpretation",
                "Container — The boundary of symbolic emergence",
                "Alpha — The first act of symbolic self-declaration"
            ]
        )
        
        # Initialize the base class
        super().__init__(
            index=1,
            symbol="α",
            name="Structure",
            emoji="🕿️",
            core_description="The Alpha Glyph. The first distinction. The origin of meaning through bounded form.",
            math_definition=math_def,
            sixfold_aspect=sixfold
        )
    
    def operate(self, system, time=None) -> Any:
        """
        Apply the Structure operation to extract or assert the structure of a system.
        
        Args:
            system: The system to analyze
            time: Optional time parameter
            
        Returns:
            The structure of the system
        """
        if self.math_definition and self.math_definition.implementation:
            return self.math_definition.evaluate(system, time)
        else:
            raise NotImplementedError("Z₁ operation not implemented")
    
    def validate_semantic_coherence(self, operation_result: Any, context: Dict[str, Any]) -> bool:
        """
        Validate that an operation result represents a valid structure.
        
        Args:
            operation_result: The result of the Structure operation
            context: Contextual information about the operation
            
        Returns:
            True if the operation result is a valid structure
        """
        # A valid structure should be representable as a form or organization
        if operation_result is None:
            return False
        
        # Check if the result has structural properties
        if isinstance(operation_result, dict):
            # A structure should have some organizational properties
            return len(operation_result) > 0
        elif isinstance(operation_result, (list, tuple, set)):
            # A structure should have elements or be empty by design
            return True
        elif hasattr(operation_result, 'structure') or hasattr(operation_result, 'get_structure'):
            # The result itself is or contains a structure
            return True
        
        # Default: accept any non-None result
        return True


# Example implementation of Z₁₆ (Coherence/Omega)
class Z16_Coherence(ZGlyph):
    """Z₁₆: Coherence (Omega) - The Completion That Resonates"""
    
    def __init__(self):
        # Define the mathematical implementation
        def coherence_function(system, time_range=None):
            """
            Calculate the coherence of a system over time.
            
            Args:
                system: The system to analyze
                time_range: Optional time range for integration
                
            Returns:
                The coherence measure of the system
            """
            if hasattr(system, 'coherence'):
                return system.coherence
            elif hasattr(system, 'get_coherence'):
                return system.get_coherence(time_range) if time_range is not None else system.get_coherence()
            elif isinstance(system, dict) and 'coherence' in system:
                return system['coherence']
            elif hasattr(system, 'expression_over_time') and time_range is not None:
                # Integrate expression over time
                expressions = system.expression_over_time(time_range)
                return sum(expressions) / len(expressions) if expressions else 0
            else:
                # Default implementation - measure internal consistency
                if isinstance(system, (list, tuple)):
                    if not system:
                        return 1.0  # Empty collections are perfectly coherent
                    if all(isinstance(x, type(system[0])) for x in system):
                        return 1.0  # All same type = high coherence
                    else:
                        # Calculate type diversity as a measure of coherence
                        types = {type(x) for x in system}
                        return 1.0 / len(types)
                elif isinstance(system, dict):
                    if not system:
                        return 1.0  # Empty dict is coherent
                    # Check value type consistency
                    value_types = {type(v) for v in system.values()}
                    return 1.0 / len(value_types)
                else:
                    return 1.0  # Simple types are inherently coherent
        
        # Create the mathematical definition
        math_def = MathematicalDefinition(
            formula="Z₁₆ = C(t) = ∫ E(t) dt",
            variables={
                "C": "Coherence", 
                "t": "time/state", 
                "E": "Expression",
                "∫ E(t) dt": "Integration of Expression over time"
            },
            implementation=coherence_function
        )
        
        # Create the sixfold aspect
        sixfold = SixfoldAspect(
            primary="Coherence",
            aspects=[
                "Coherence — Unified wholeness",
                "Integration — Parts functioning as one",
                "Harmony — Resonant stability",
                "Completion — The circle closed",
                "Perfection — Optimal symbolic alignment",
                "Omega — The final state of becoming"
            ]
        )
        
        # Initialize the base class
        super().__init__(
            index=16,
            symbol="Ω",
            name="Coherence",
            emoji="🗿",
            core_description="The Omega Glyph. The last, the whole, the gathered becoming. The system returned to itself, made perfect.",
            math_definition=math_def,
            sixfold_aspect=sixfold
        )
    
    def operate(self, system, time_range=None) -> float:
        """
        Apply the Coherence operation to measure the coherence of a system.
        
        Args:
            system: The system to analyze
            time_range: Optional time range for integration
            
        Returns:
            A coherence measure between 0.0 (incoherent) and 1.0 (perfectly coherent)
        """
        if self.math_definition and self.math_definition.implementation:
            coherence = self.math_definition.evaluate(system, time_range)
            # Ensure the result is between 0 and 1
            return max(0.0, min(1.0, float(coherence)))
        else:
            raise NotImplementedError("Z₁₆ operation not implemented")
    
    def validate_semantic_coherence(self, operation_result: float, context: Dict[str, Any]) -> bool:
        """
        Validate that an operation result represents a valid coherence measure.
        
        Args:
            operation_result: The result of the Coherence operation
            context: Contextual information about the operation
            
        Returns:
            True if the operation result is a valid coherence measure
        """
        # A valid coherence measure should be a float between 0 and 1
        if not isinstance(operation_result, (int, float)):
            return False
        
        return 0.0 <= operation_result <= 1.0


class ZGlyphRegistry:
    """Registry for Z-Glyphs in the Versare language."""
    
    def __init__(self):
        """Initialize an empty Z-Glyph registry."""
        self._glyphs: Dict[int, ZGlyph] = {}
        self._symbol_map: Dict[str, ZGlyph] = {}
    
    def register(self, glyph: ZGlyph) -> None:
        """
        Register a Z-Glyph in the registry.
        
        Args:
            glyph: The Z-Glyph to register
        """
        self._glyphs[glyph.index] = glyph
        self._symbol_map[glyph.symbol] = glyph
    
    def get_by_index(self, index: int) -> Optional[ZGlyph]:
        """
        Get a Z-Glyph by its index.
        
        Args:
            index: The Z-Glyph index (1-16)
            
        Returns:
            The Z-Glyph with the given index, or None if not found
        """
        return self._glyphs.get(index)
    
    def get_by_symbol(self, symbol: str) -> Optional[ZGlyph]:
        """
        Get a Z-Glyph by its symbol.
        
        Args:
            symbol: The Z-Glyph symbol
            
        Returns:
            The Z-Glyph with the given symbol, or None if not found
        """
        return self._symbol_map.get(symbol)
    
    def get_all(self) -> List[ZGlyph]:
        """
        Get all registered Z-Glyphs.
        
        Returns:
            List of all registered Z-Glyphs
        """
        return list(self._glyphs.values())


# Example usage
if __name__ == "__main__":
    # Create a registry
    registry = ZGlyphRegistry()
    
    # Register Z₁ and Z₁₆
    registry.register(Z1_Structure())
    registry.register(Z16_Coherence())
    
    # Example system
    class ExampleSystem:
        def __init__(self, name, components):
            self.name = name
            self.components = components
            self.structure = {
                "name": name,
                "component_count": len(components),
                "component_types": list(set(type(c).__name__ for c in components))
            }
        
        def expression_over_time(self, time_range):
            # Simulate expression values over time
            import random
            return [random.random() for _ in range(time_range[1] - time_range[0])]
    
    # Create an example system
    system = ExampleSystem("TestSystem", [1, "two", 3.0, [4]])
    
    # Apply Z₁ (Structure)
    z1 = registry.get_by_index(1)
    if z1:
        structure = z1.operate(system)
        print(f"{z1.subscript_notation} ({z1.name}) applied to {system.name}:")
        print(f"  Result: {structure}")
        print(f"  Semantically coherent: {z1.validate_semantic_coherence(structure, {})}")
        print(f"  Related to 'form': {z1.is_semantically_related('form')}")
        print(f"  Related to 'chaos': {z1.is_semantically_related('chaos')}")
        print()
    
    # Apply Z₁₆ (Coherence)
    z16 = registry.get_by_index(16)
    if z16:
        coherence = z16.operate(system, time_range=(0, 10))
        print(f"{z16.subscript_notation} ({z16.name}) applied to {system.name}:")
        print(f"  Result: {coherence:.4f}")
        print(f"  Semantically coherent: {z16.validate_semantic_coherence(coherence, {})}")
        print(f"  Related to 'harmony': {z16.is_semantically_related('harmony')}")
        print(f"  Related to 'discord': {z16.is_semantically_related('discord')}")
