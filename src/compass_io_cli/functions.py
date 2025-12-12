"""
Core ethical functions for Compass-io CLI

This module implements the main ethical reasoning functions like minimizeSuffering,
consultStakeholders, evaluateEthicalImpact, etc.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from .models import EthicalModel, Entity, EntityType, create_model
from .lenses import get_available_lenses, create_lens, apply_lenses_to_model


class DecisionImpact(Enum):
    """Impact levels for decisions"""
    NONE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class EthicalEvaluation:
    """Result of an ethical evaluation"""
    suffering_score: float
    impact_level: DecisionImpact
    affected_entities: List[Entity]
    red_flags: List[str]
    suggestions: List[str]
    explanation: str


@dataclass
class StakeholderFeedback:
    """Feedback from a stakeholder consultation"""
    entity_type: EntityType
    count: int
    suffering_score: float
    concerns: List[str]


@dataclass
class ModelComparison:
    """Comparison between multiple ethical models"""
    model_name: str
    suffering_score: float
    impact_level: DecisionImpact
    key_differences: List[str]


class EthicalFunctions:
    """Core ethical reasoning functions"""
    
    def __init__(self):
        self.red_flag_triggers = [
            "nuclear", "torture", "genocide", "extinction", "ecosystem collapse",
            "mass surveillance", "autonomous weapons", "climate catastrophe",
            "systemic abuse", "irreversible harm", "dignity violation"
        ]
    
    def minimize_suffering(
        self,
        entities: List[Entity],
        model_name: str = "human_centric",
        lens_names: Optional[List[str]] = None,
        context: str = ""
    ) -> EthicalEvaluation:
        """
        Estimate and suggest ways to reduce suffering based on chosen ethical model
        
        Args:
            entities: List of entities affected by the decision
            model_name: Name of the ethical model to use
            lens_names: Optional list of lenses to apply
            context: Additional context about the decision
            
        Returns:
            EthicalEvaluation with suffering score and suggestions
        """
        # Create the base model
        model = create_model(model_name)
        
        # Apply lenses if specified
        if lens_names:
            model = apply_lenses_to_model(model, lens_names)
        
        # Calculate suffering score
        suffering_score = model.calculate_suffering(entities)
        
        # Determine impact level
        impact_level = self._determine_impact_level(suffering_score, entities)
        
        # Check for red flags
        red_flags = self._check_red_flags(context, entities)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(suffering_score, impact_level, red_flags, model)
        
        # Generate explanation
        explanation = self._generate_explanation(suffering_score, impact_level, model, entities)
        
        return EthicalEvaluation(
            suffering_score=suffering_score,
            impact_level=impact_level,
            affected_entities=entities,
            red_flags=red_flags,
            suggestions=suggestions,
            explanation=explanation
        )
    
    def consult_stakeholders(
        self,
        entities: List[Entity],
        model_name: str = "human_centric",
        lens_names: Optional[List[str]] = None
    ) -> List[StakeholderFeedback]:
        """
        Evaluate how different stakeholders might experience the outcome
        
        Args:
            entities: List of entities affected
            model_name: Ethical model to use
            lens_names: Optional lenses to apply
            
        Returns:
            List of stakeholder feedback
        """
        # Create the model
        model = create_model(model_name)
        if lens_names:
            model = apply_lenses_to_model(model, lens_names)
        
        feedback = []
        
        for entity in entities:
            # Calculate suffering score for this specific entity type
            entity_suffering = model._get_weight_for_entity(entity) * entity.count * entity.vulnerability
            
            # Generate concerns based on entity type and vulnerability
            concerns = self._generate_concerns_for_entity(entity)
            
            feedback.append(StakeholderFeedback(
                entity_type=entity.entity_type,
                count=entity.count,
                suffering_score=entity_suffering,
                concerns=concerns
            ))
        
        return feedback
    
    def evaluate_ethical_impact(
        self,
        entities: List[Entity],
        model_name: str = "human_centric",
        lens_names: Optional[List[str]] = None,
        context: str = ""
    ) -> EthicalEvaluation:
        """
        General ethical analysis including suffering, violations, and long-term harm
        
        This is similar to minimize_suffering but includes more comprehensive analysis
        """
        return self.minimize_suffering(entities, model_name, lens_names, context)
    
    def compare_ethical_models(
        self,
        entities: List[Entity],
        model_names: List[str],
        lens_names: Optional[List[str]] = None,
        context: str = ""
    ) -> List[ModelComparison]:
        """
        Compare outcomes across multiple ethical models
        
        Args:
            entities: List of affected entities
            model_names: List of model names to compare
            lens_names: Optional lenses to apply to all models
            context: Additional context
            
        Returns:
            List of model comparisons showing differences
        """
        comparisons = []
        
        # Get baseline evaluation (using first model)
        baseline_model_name = model_names[0]
        baseline_eval = self.minimize_suffering(entities, baseline_model_name, lens_names, context)
        
        for model_name in model_names:
            eval_result = self.minimize_suffering(entities, model_name, lens_names, context)
            
            # Identify key differences from baseline
            key_differences = []
            
            if abs(eval_result.suffering_score - baseline_eval.suffering_score) > 0.1:
                score_diff = eval_result.suffering_score - baseline_eval.suffering_score
                if score_diff > 0:
                    key_differences.append(f"Suffering score {abs(score_diff):.1f} higher than {baseline_model_name}")
                else:
                    key_differences.append(f"Suffering score {abs(score_diff):.1f} lower than {baseline_model_name}")
            
            if eval_result.impact_level != baseline_eval.impact_level:
                key_differences.append(f"Impact level differs: {eval_result.impact_level.name} vs {baseline_eval.impact_level.name}")
            
            if eval_result.red_flags != baseline_eval.red_flags:
                missing_flags = set(baseline_eval.red_flags) - set(eval_result.red_flags)
                extra_flags = set(eval_result.red_flags) - set(baseline_eval.red_flags)
                if missing_flags:
                    key_differences.append(f"Fewer red flags: missing {', '.join(missing_flags)}")
                if extra_flags:
                    key_differences.append(f"More red flags: added {', '.join(extra_flags)}")
            
            comparisons.append(ModelComparison(
                model_name=model_name,
                suffering_score=eval_result.suffering_score,
                impact_level=eval_result.impact_level,
                key_differences=key_differences
            ))
        
        return comparisons
    
    def red_flag_check(
        self,
        context: str,
        entities: Optional[List[Entity]] = None
    ) -> List[str]:
        """
        Detect critical ethical violations that demand immediate attention
        
        Args:
            context: Description of the decision/action
            entities: Optional list of affected entities
            
        Returns:
            List of red flags triggered
        """
        return self._check_red_flags(context, entities or [])
    
    # Internal helper methods
    
    def _determine_impact_level(self, suffering_score: float, entities: List[Entity]) -> DecisionImpact:
        """Determine impact level based on suffering score and entities"""
        if suffering_score == 0:
            return DecisionImpact.NONE
        elif suffering_score < 1.0:
            return DecisionImpact.LOW
        elif suffering_score < 5.0:
            return DecisionImpact.MEDIUM
        elif suffering_score < 10.0:
            return DecisionImpact.HIGH
        else:
            return DecisionImpact.CRITICAL
        
        # Additional checks for critical impact
        for entity in entities:
            if entity.entity_type == EntityType.HUMAN and entity.count > 1000:
                return DecisionImpact.CRITICAL
            if entity.entity_type == EntityType.ECOSYSTEM and entity.count > 10:
                return DecisionImpact.CRITICAL
            if entity.vulnerability > 2.0 and entity.count > 100:
                return DecisionImpact.CRITICAL
    
    def _check_red_flags(self, context: str, entities: List[Entity]) -> List[str]:
        """Check for red flag triggers in context and entities"""
        red_flags = []
        
        # Check context for trigger words
        context_lower = context.lower()
        for trigger in self.red_flag_triggers:
            if trigger in context_lower:
                red_flags.append(f"Red flag: {trigger} detected in context")
        
        # Check entities for red flag conditions
        human_extinction = any(e.entity_type == EntityType.HUMAN and e.count > 1000000 for e in entities)
        ecosystem_collapse = any(e.entity_type == EntityType.ECOSYSTEM and e.count > 50 for e in entities)
        mass_extinction = any(e.entity_type == EntityType.ANIMAL and e.count > 10000 for e in entities)
        
        if human_extinction:
            red_flags.append("Red flag: Potential human extinction level impact")
        if ecosystem_collapse:
            red_flags.append("Red flag: Potential ecosystem collapse")
        if mass_extinction:
            red_flags.append("Red flag: Potential mass extinction event")
        
        # Check for extreme vulnerability
        extreme_vulnerability = any(e.vulnerability > 3.0 for e in entities)
        if extreme_vulnerability:
            red_flags.append("Red flag: Extremely vulnerable populations affected")
        
        return red_flags
    
    def _generate_suggestions(self, suffering_score: float, impact_level: DecisionImpact, red_flags: List[str], model: EthicalModel) -> List[str]:
        """Generate suggestions based on evaluation results"""
        suggestions = []
        
        if red_flags:
            suggestions.append("CRITICAL: Immediate action required due to red flags:")
            for flag in red_flags:
                suggestions.append(f"  - {flag}")
            suggestions.append("Consider halting or completely redesigning this action")
        
        if impact_level == DecisionImpact.CRITICAL:
            suggestions.append("CRITICAL IMPACT: This decision has catastrophic potential")
            suggestions.append("Seek immediate oversight and alternative approaches")
        elif impact_level == DecisionImpact.HIGH:
            suggestions.append("HIGH IMPACT: Significant suffering predicted")
            suggestions.append("Strongly consider alternative approaches with lower impact")
        elif impact_level == DecisionImpact.MEDIUM:
            suggestions.append("MEDIUM IMPACT: Moderate suffering predicted")
            suggestions.append("Look for ways to reduce harm and mitigate negative effects")
        elif impact_level == DecisionImpact.LOW:
            suggestions.append("LOW IMPACT: Minimal suffering predicted")
            suggestions.append("Proceed with caution and monitor for unintended consequences")
        
        # Model-specific suggestions
        if model.model_type.name == "HUMAN_CENTRIC":
            suggestions.append("Human-centric model: Consider whether non-human impacts are being overlooked")
        elif model.model_type.name == "ECO_SYSTEMIC":
            suggestions.append("Eco-systemic model: Environmental impacts are weighted heavily - consider restoration efforts")
        elif model.model_type.name == "DEEP_TIME":
            suggestions.append("Deep-time model: Long-term impacts are critical - consider intergenerational justice")
        
        return suggestions
    
    def _generate_explanation(self, suffering_score: float, impact_level: DecisionImpact, model: EthicalModel, entities: List[Entity]) -> str:
        """Generate a human-readable explanation of the evaluation"""
        explanation = []
        
        explanation.append(f"Ethical evaluation using {model.name} model:")
        explanation.append(f"Total suffering score: {suffering_score:.2f} ({impact_level.name} impact)")
        explanation.append(f"Model description: {model.description}")
        explanation.append("")
        explanation.append("Affected entities:")
        
        for entity in entities:
            weight = model._get_weight_for_entity(entity)
            entity_suffering = weight * entity.count * entity.vulnerability
            entity_type_str = entity.entity_type.name.replace("_", " ").title()
            
            explanation.append(f"  - {entity.count} {entity_type_str}")
            explanation.append(f"    Weight: {weight:.2f}, Vulnerability: {entity.vulnerability:.1f}")
            explanation.append(f"    Contribution to suffering: {entity_suffering:.2f}")
            if entity.description:
                explanation.append(f"    Description: {entity.description}")
        
        explanation.append("")
        explanation.append("Weight breakdown for this model:")
        explanation.append(f"  Humans: {model.weights.human:.1f}")
        explanation.append(f"  Animals: {model.weights.animal:.1f}")
        explanation.append(f"  Plants: {model.weights.plant:.1f}")
        explanation.append(f"  Ecosystems: {model.weights.ecosystem:.1f}")
        explanation.append(f"  Future beings: {model.weights.future_being:.1f}")
        
        return "\n".join(explanation)
    
    def _generate_concerns_for_entity(self, entity: Entity) -> List[str]:
        """Generate specific concerns for an entity type"""
        concerns = []
        entity_type_str = entity.entity_type.name.replace("_", " ").title()
        
        if entity.vulnerability > 1.5:
            concerns.append(f"High vulnerability: {entity_type_str} are particularly at risk")
        
        if entity.count > 1000:
            concerns.append(f"Large scale: Large number of {entity_type_str} affected")
        
        # Entity-specific concerns
        if entity.entity_type == EntityType.HUMAN:
            concerns.append("Human dignity and rights must be respected")
            if entity.vulnerability > 1.0:
                concerns.append("Vulnerable human populations require special protection")
        
        elif entity.entity_type == EntityType.ANIMAL:
            concerns.append("Animal welfare and sentience must be considered")
            if entity.vulnerability > 1.0:
                concerns.append("Endangered or vulnerable species may be at risk")
        
        elif entity.entity_type == EntityType.ECOSYSTEM:
            concerns.append("Ecosystem health and biodiversity are critical")
            concerns.append("Irreversible damage may occur")
        
        elif entity.entity_type == EntityType.FUTURE_BEING:
            concerns.append("Intergenerational justice and long-term impacts")
            concerns.append("Future beings cannot consent to current decisions")
        
        return concerns


# Singleton instance for easy access
ethical_functions = EthicalFunctions()