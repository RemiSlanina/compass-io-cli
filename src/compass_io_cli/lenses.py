"""
Lenses for Compass-io CLI

Lenses are modifiers that adjust ethical model behavior and weighting.
They provide additional perspectives on suffering and moral consideration.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum, auto
from .models import EthicalModel, Entity, EthicalWeight


class LensType(Enum):
    """Types of lenses available"""
    SPARKS = auto()
    FRAGILITY = auto()
    DEEP_TIME = auto()
    CULTURAL = auto()


@dataclass
class Lens:
    """Base class for all lenses"""
    name: str
    lens_type: LensType
    description: str
    
    def apply(self, model: EthicalModel) -> EthicalModel:
        """Apply this lens to an ethical model, returning a modified version"""
        # Create a copy of the model with adjusted weights
        new_weights = self._adjust_weights(model.weights)
        
        return EthicalModel(
            name=f"{model.name} + {self.name}",
            model_type=model.model_type,
            description=f"{model.description} (with {self.name} lens)",
            weights=new_weights
        )
    
    def _adjust_weights(self, weights: EthicalWeight) -> EthicalWeight:
        """Adjust the weights based on this lens"""
        return weights  # Base implementation does nothing


class SparksLens(Lens):
    """Sparks Lens - weights inherent worth and avoids bias"""
    
    def __init__(self):
        super().__init__(
            name="Sparks",
            lens_type=LensType.SPARKS,
            description="Values all kinds of lives, avoids biased decisions by weighting worth before deserving or utility"
        )
    
    def _adjust_weights(self, weights: EthicalWeight) -> EthicalWeight:
        """Adjust weights to give more consideration to vulnerable and overlooked entities"""
        # Increase weights for typically overlooked entities
        return EthicalWeight(
            human=weights.human * 0.9,  # Slightly reduce human bias
            animal=min(weights.animal * 1.2, 1.0),  # Increase animal consideration
            plant=min(weights.plant * 1.3, 0.8),  # Increase plant consideration
            microbe=min(weights.microbe * 1.5, 0.5),  # Increase microbe consideration
            ecosystem=min(weights.ecosystem * 1.1, 1.0),  # Slightly increase ecosystem
            inanimate_object=min(weights.inanimate_object * 1.2, 0.6),  # Increase object consideration
            future_being=min(weights.future_being * 1.1, 1.5),  # Increase future consideration
            symbolic_entity=min(weights.symbolic_entity * 1.3, 0.8)  # Increase symbolic consideration
        )


class FragilityLens(Lens):
    """Fragility Lens - weights vulnerability and irreversibility"""
    
    def __init__(self):
        super().__init__(
            name="Fragility",
            lens_type=LensType.FRAGILITY,
            description="Focuses on vulnerability and irreversibility, values what might be gone for good"
        )
    
    def _adjust_weights(self, weights: EthicalWeight) -> EthicalWeight:
        """Adjust weights to emphasize fragile and irreversible impacts"""
        # Increase weights for entities that are fragile or represent irreversible loss
        return EthicalWeight(
            human=weights.human * 1.0,  # Keep human weight same
            animal=min(weights.animal * 1.3, 1.0),  # Animals are vulnerable
            plant=min(weights.plant * 1.5, 0.9),  # Plants can be fragile ecosystems
            microbe=min(weights.microbe * 1.2, 0.6),  # Microbes in fragile ecosystems
            ecosystem=min(weights.ecosystem * 1.5, 1.2),  # Ecosystems are highly fragile
            inanimate_object=weights.inanimate_object * 1.0,  # Objects less affected by fragility
            future_being=min(weights.future_being * 1.3, 1.8),  # Future is vulnerable
            symbolic_entity=min(weights.symbolic_entity * 1.4, 1.0)  # Symbolic entities can be fragile
        )


class DeepTimeLens(Lens):
    """Deep Time Lens - emphasizes long-term impact"""
    
    def __init__(self):
        super().__init__(
            name="Deep-Time",
            lens_type=LensType.DEEP_TIME,
            description="Extreme long-term perspective, weights long-term impact heavily"
        )
    
    def _adjust_weights(self, weights: EthicalWeight) -> EthicalWeight:
        """Adjust weights to emphasize long-term and future impacts"""
        # Significantly increase weights for future and long-lasting impacts
        return EthicalWeight(
            human=weights.human * 0.8,  # Reduce present human bias
            animal=weights.animal * 0.9,  # Slight reduction for present animals
            plant=weights.plant * 1.0,  # Keep plant weight same
            microbe=weights.microbe * 1.0,  # Keep microbe weight same
            ecosystem=min(weights.ecosystem * 1.3, 1.2),  # Ecosystems matter for long-term
            inanimate_object=weights.inanimate_object * 0.7,  # Reduce object importance
            future_being=min(weights.future_being * 1.8, 2.0),  # Massively increase future weight
            symbolic_entity=min(weights.symbolic_entity * 1.2, 0.9)  # Increase symbolic for long-term
        )


class CulturalLens(Lens):
    """Cultural Lens - can be customized for specific cultural perspectives"""
    
    def __init__(self, name: str = "Cultural", description: str = "Custom cultural perspective"):
        super().__init__(
            name=name,
            lens_type=LensType.CULTURAL,
            description=description
        )
        self.weight_adjustments = EthicalWeight()  # Default no adjustments
    
    def set_weight_adjustments(self, adjustments: EthicalWeight):
        """Set custom weight adjustments for this cultural lens"""
        self.weight_adjustments = adjustments
    
    def _adjust_weights(self, weights: EthicalWeight) -> EthicalWeight:
        """Apply custom cultural weight adjustments"""
        return EthicalWeight(
            human=weights.human * self.weight_adjustments.human,
            animal=weights.animal * self.weight_adjustments.animal,
            plant=weights.plant * self.weight_adjustments.plant,
            microbe=weights.microbe * self.weight_adjustments.microbe,
            ecosystem=weights.ecosystem * self.weight_adjustments.ecosystem,
            inanimate_object=weights.inanimate_object * self.weight_adjustments.inanimate_object,
            future_being=weights.future_being * self.weight_adjustments.future_being,
            symbolic_entity=weights.symbolic_entity * self.weight_adjustments.symbolic_entity
        )


# Registry of available lenses
LENS_REGISTRY = {
    "sparks": SparksLens,
    "fragility": FragilityLens,
    "deep_time": DeepTimeLens,
    "cultural": CulturalLens,
}


def get_available_lenses() -> List[str]:
    """Get list of available lens names"""
    return list(LENS_REGISTRY.keys())


def create_lens(lens_name: str) -> Lens:
    """Create a lens by name"""
    if lens_name not in LENS_REGISTRY:
        raise ValueError(f"Unknown lens: {lens_name}. Available lenses: {get_available_lenses()}")
    
    return LENS_REGISTRY[lens_name]()


def apply_lenses_to_model(model: EthicalModel, lens_names: List[str]) -> EthicalModel:
    """Apply multiple lenses to an ethical model"""
    current_model = model
    
    for lens_name in lens_names:
        lens = create_lens(lens_name)
        current_model = lens.apply(current_model)
    
    return current_model