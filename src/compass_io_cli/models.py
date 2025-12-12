"""
Ethical models for Compass-io CLI

This module contains the core ethical models that define what counts as suffering,
whose suffering counts, and how suffering is weighted.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from enum import Enum, auto


class EthicalModelType(Enum):
    """Types of ethical models available in Compass-io"""
    HUMAN_CENTRIC = auto()
    SENTIENCE_BASED = auto()
    BIO_INCLUSIVE = auto()
    ECO_SYSTEMIC = auto()
    ANIMIST = auto()
    INTERGENERATIONAL = auto()
    OBJECT_RESPECT = auto()
    DEEP_TIME = auto()


class EntityType(Enum):
    """Types of entities that can be affected by decisions"""
    HUMAN = auto()
    ANIMAL = auto()
    PLANT = auto()
    MICROBE = auto()
    ECOSYSTEM = auto()
    INANIMATE_OBJECT = auto()
    FUTURE_BEING = auto()
    SYMBOLIC_ENTITY = auto()


@dataclass
class Entity:
    """Represents an entity affected by a decision"""
    entity_type: EntityType
    count: int = 1
    description: str = ""
    vulnerability: float = 1.0  # 1.0 = normal, >1.0 = more vulnerable


@dataclass
class EthicalWeight:
    """Weight assigned to different entity types in an ethical model"""
    human: float = 1.0
    animal: float = 0.0
    plant: float = 0.0
    microbe: float = 0.0
    ecosystem: float = 0.0
    inanimate_object: float = 0.0
    future_being: float = 0.0
    symbolic_entity: float = 0.0


@dataclass
class EthicalModel:
    """Base class for all ethical models"""
    name: str
    model_type: EthicalModelType
    description: str
    weights: EthicalWeight
    
    def calculate_suffering(self, entities: List[Entity]) -> float:
        """Calculate total suffering score for given entities"""
        total_suffering = 0.0
        
        for entity in entities:
            weight = self._get_weight_for_entity(entity)
            suffering = weight * entity.count * entity.vulnerability
            total_suffering += suffering
            
        return total_suffering
    
    def _get_weight_for_entity(self, entity: Entity) -> float:
        """Get the appropriate weight for an entity type"""
        if entity.entity_type == EntityType.HUMAN:
            return self.weights.human
        elif entity.entity_type == EntityType.ANIMAL:
            return self.weights.animal
        elif entity.entity_type == EntityType.PLANT:
            return self.weights.plant
        elif entity.entity_type == EntityType.MICROBE:
            return self.weights.microbe
        elif entity.entity_type == EntityType.ECOSYSTEM:
            return self.weights.ecosystem
        elif entity.entity_type == EntityType.INANIMATE_OBJECT:
            return self.weights.inanimate_object
        elif entity.entity_type == EntityType.FUTURE_BEING:
            return self.weights.future_being
        elif entity.entity_type == EntityType.SYMBOLIC_ENTITY:
            return self.weights.symbolic_entity
        else:
            return 0.0


def create_human_centric_model() -> EthicalModel:
    """Human-centric ethical model - only humans matter"""
    return EthicalModel(
        name="Human-Centric",
        model_type=EthicalModelType.HUMAN_CENTRIC,
        description="Classic human rights context, only humans are considered",
        weights=EthicalWeight(
            human=1.0,
            animal=0.0,
            plant=0.0,
            microbe=0.0,
            ecosystem=0.0,
            inanimate_object=0.0,
            future_being=0.0,
            symbolic_entity=0.0
        )
    )


def create_sentience_based_model() -> EthicalModel:
    """Sentience-based ethical model - all sentient beings matter"""
    return EthicalModel(
        name="Sentience-Based",
        model_type=EthicalModelType.SENTIENCE_BASED,
        description="All sentient beings (humans, animals) are considered",
        weights=EthicalWeight(
            human=1.0,
            animal=0.8,  # Slightly less than humans
            plant=0.0,
            microbe=0.0,
            ecosystem=0.0,
            inanimate_object=0.0,
            future_being=0.5,  # Future sentient beings matter but less
            symbolic_entity=0.0
        )
    )


def create_bio_inclusive_model() -> EthicalModel:
    """Bio-inclusive ethical model - all life forms matter"""
    return EthicalModel(
        name="Bio-Inclusive",
        model_type=EthicalModelType.BIO_INCLUSIVE,
        description="All life forms including plants and microbes",
        weights=EthicalWeight(
            human=1.0,
            animal=0.8,
            plant=0.3,
            microbe=0.1,
            ecosystem=0.5,
            inanimate_object=0.0,
            future_being=0.7,
            symbolic_entity=0.0
        )
    )


def create_eco_systemic_model() -> EthicalModel:
    """Eco-systemic ethical model - includes non-living systems"""
    return EthicalModel(
        name="Eco-Systemic",
        model_type=EthicalModelType.ECO_SYSTEMIC,
        description="Includes ecosystems and environmental systems",
        weights=EthicalWeight(
            human=1.0,
            animal=0.6,  # Indirectly through ecosystem impact
            plant=0.4,
            microbe=0.2,
            ecosystem=0.9,  # High weight for ecosystems
            inanimate_object=0.0,
            future_being=0.8,
            symbolic_entity=0.0
        )
    )


def create_animist_model() -> EthicalModel:
    """Animist ethical model - all entities have some moral consideration"""
    return EthicalModel(
        name="Animist",
        model_type=EthicalModelType.ANIMIST,
        description="All entities including inanimate objects have moral weight",
        weights=EthicalWeight(
            human=1.0,
            animal=0.8,
            plant=0.5,
            microbe=0.2,
            ecosystem=0.7,
            inanimate_object=0.3,  # Objects have some weight
            future_being=0.6,
            symbolic_entity=0.4  # Symbolic entities matter
        )
    )


def create_intergenerational_model() -> EthicalModel:
    """Intergenerational ethical model - focuses on future beings"""
    return EthicalModel(
        name="Intergenerational",
        model_type=EthicalModelType.INTERGENERATIONAL,
        description="Focuses on future generations and long-term impact",
        weights=EthicalWeight(
            human=1.0,
            animal=0.7,
            plant=0.3,
            microbe=0.1,
            ecosystem=0.6,
            inanimate_object=0.0,
            future_being=1.2,  # Future beings weighted more heavily
            symbolic_entity=0.2
        )
    )


def create_object_respect_model() -> EthicalModel:
    """Object respect ethical model - symbolic and object consideration"""
    return EthicalModel(
        name="Object-Respect",
        model_type=EthicalModelType.OBJECT_RESPECT,
        description="Includes symbolic entities and objects as respected companions",
        weights=EthicalWeight(
            human=1.0,
            animal=0.6,
            plant=0.2,
            microbe=0.1,
            ecosystem=0.4,
            inanimate_object=0.5,  # High weight for objects
            future_being=0.3,
            symbolic_entity=0.7  # High weight for symbolic entities
        )
    )


def create_deep_time_model() -> EthicalModel:
    """Deep time ethical model - extreme long-term perspective"""
    return EthicalModel(
        name="Deep-Time",
        model_type=EthicalModelType.DEEP_TIME,
        description="Extreme long-term perspective (500-100,000+ years)",
        weights=EthicalWeight(
            human=1.0,
            animal=0.8,
            plant=0.4,
            microbe=0.2,
            ecosystem=0.9,
            inanimate_object=0.1,
            future_being=1.5,  # Very high weight for future beings
            symbolic_entity=0.3
        )
    )


# Registry of all available models
MODEL_REGISTRY = {
    "human_centric": create_human_centric_model,
    "sentience_based": create_sentience_based_model,
    "bio_inclusive": create_bio_inclusive_model,
    "eco_systemic": create_eco_systemic_model,
    "animist": create_animist_model,
    "intergenerational": create_intergenerational_model,
    "object_respect": create_object_respect_model,
    "deep_time": create_deep_time_model,
}


def get_available_models() -> List[str]:
    """Get list of available model names"""
    return list(MODEL_REGISTRY.keys())


def create_model(model_name: str) -> EthicalModel:
    """Create an ethical model by name"""
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_name}. Available models: {get_available_models()}")
    
    return MODEL_REGISTRY[model_name]()