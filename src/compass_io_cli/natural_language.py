"""
Natural Language Interface for Compass-io CLI

This module provides functionality to parse natural language descriptions
of ethical scenarios into structured data that can be processed by the
ethical reasoning engine.

Future Vision: This module will evolve to include research integration,
allowing the system to gather contextual data about locations, industries,
and specific scenarios to enhance ethical analysis.
"""

import re
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
from .models import Entity, EntityType, get_available_models
from .lenses import get_available_lenses
from .functions import ethical_functions


class ParsingMethod(Enum):
    """Methods for parsing natural language"""
    SIMPLE_KEYWORD = "simple_keyword"
    LLM_ASSISTED = "llm_assisted"
    INTERACTIVE = "interactive"


class EthicalScenario:
    """Represents a parsed ethical scenario from natural language"""
    
    def __init__(self):
        self.entities: List[Entity] = []
        self.model: str = "human_centric"  # default
        self.lenses: List[str] = []
        self.context: str = ""
        self.raw_text: str = ""
        self.parsing_method: ParsingMethod = ParsingMethod.SIMPLE_KEYWORD
        self.confidence: float = 0.7  # confidence in parsing
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
        
    def add_entity(self, entity_type: EntityType, count: int = 1, 
                   description: str = "", vulnerability: float = 1.0):
        """Add an entity to the scenario"""
        self.entities.append(Entity(
            entity_type=entity_type,
            count=count,
            description=description,
            vulnerability=vulnerability
        ))
    
    def set_model(self, model_name: str):
        """Set the ethical model"""
        if model_name in get_available_models():
            self.model = model_name
        else:
            self.warnings.append(f"Unknown model: {model_name}")
    
    def add_lens(self, lens_name: str):
        """Add a lens to the scenario"""
        if lens_name in get_available_lenses():
            if lens_name not in self.lenses:
                self.lenses.append(lens_name)
        else:
            self.warnings.append(f"Unknown lens: {lens_name}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "entities": [{
                "type": e.entity_type.name,
                "count": e.count,
                "description": e.description,
                "vulnerability": e.vulnerability
            } for e in self.entities],
            "model": self.model,
            "lenses": self.lenses,
            "context": self.context,
            "raw_text": self.raw_text,
            "parsing_method": self.parsing_method.value,
            "confidence": self.confidence,
            "warnings": self.warnings,
            "suggestions": self.suggestions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EthicalScenario':
        """Create from dictionary"""
        scenario = cls()
        scenario.raw_text = data.get("raw_text", "")
        scenario.context = data.get("context", "")
        scenario.model = data.get("model", "human_centric")
        scenario.lenses = data.get("lenses", [])
        scenario.parsing_method = ParsingMethod(data.get("parsing_method", "simple_keyword"))
        scenario.confidence = data.get("confidence", 0.7)
        scenario.warnings = data.get("warnings", [])
        scenario.suggestions = data.get("suggestions", [])
        
        # Parse entities
        for entity_data in data.get("entities", []):
            try:
                entity_type = EntityType[entity_data["type"]]
                scenario.add_entity(
                    entity_type=entity_type,
                    count=entity_data.get("count", 1),
                    description=entity_data.get("description", ""),
                    vulnerability=entity_data.get("vulnerability", 1.0)
                )
            except (KeyError, ValueError):
                scenario.warnings.append(f"Invalid entity data: {entity_data}")
        
        return scenario


class NaturalLanguageParser:
    """Main class for parsing natural language ethical scenarios"""
    
    def __init__(self):
        self.entity_keywords = {
            "human": EntityType.HUMAN,
            "people": EntityType.HUMAN,
            "person": EntityType.HUMAN,
            "user": EntityType.HUMAN,
            "resident": EntityType.HUMAN,
            "worker": EntityType.HUMAN,
            "animal": EntityType.ANIMAL,
            "wildlife": EntityType.ANIMAL,
            "species": EntityType.ANIMAL,
            "plant": EntityType.PLANT,
            "tree": EntityType.PLANT,
            "flora": EntityType.PLANT,
            "vegetation": EntityType.PLANT,
            "ecosystem": EntityType.ECOSYSTEM,
            "environment": EntityType.ECOSYSTEM,
            "habitat": EntityType.ECOSYSTEM,
            "future": EntityType.FUTURE_BEING,
            "generation": EntityType.FUTURE_BEING,
            "descendant": EntityType.FUTURE_BEING,
            "cultural": EntityType.SYMBOLIC_ENTITY,
            "symbolic": EntityType.SYMBOLIC_ENTITY,
            "heritage": EntityType.SYMBOLIC_ENTITY
        }
        
        self.model_keywords = {
            "human": "human_centric",
            "people": "human_centric",
            "rights": "human_centric",
            "sentient": "sentience_based",
            "animal": "sentience_based",
            "welfare": "sentience_based",
            "bio": "bio_inclusive",
            "ecological": "bio_inclusive",
            "ecosystem": "eco_systemic",
            "environmental": "eco_systemic",
            "climate": "eco_systemic",
            "nature": "eco_systemic",
            "animist": "animist",
            "spiritual": "animist",
            "cultural": "animist",
            "future": "intergenerational",
            "generation": "intergenerational",
            "sustainable": "intergenerational",
            "long-term": "intergenerational",
            "object": "object_respect",
            "symbolic": "object_respect",
            "heritage": "object_respect",
            "deep": "deep_time",
            "time": "deep_time",
            "ancient": "deep_time"
        }
        
        self.lens_keywords = {
            "bias": "sparks",
            "fairness": "sparks",
            "diversity": "sparks",
            "inclusion": "sparks",
            "vulnerable": "fragility",
            "fragile": "fragility",
            "irreversible": "fragility",
            "delicate": "fragility",
            "long-term": "deep_time",
            "future": "deep_time",
            "legacy": "deep_time",
            "cultural": "cultural",
            "tradition": "cultural",
            "heritage": "cultural"
        }
        
        self.vulnerability_indicators = {
            "vulnerable": 1.5,
            "endangered": 2.0,
            "at-risk": 1.8,
            "marginalized": 1.7,
            "fragile": 1.6,
            "delicate": 1.4,
            "protected": 1.3,
            "sensitive": 1.4
        }
    
    def parse_simple(self, text: str) -> EthicalScenario:
        """Parse text using simple keyword matching"""
        scenario = EthicalScenario()
        scenario.raw_text = text
        scenario.context = text[:200]  # Use first part as context
        scenario.parsing_method = ParsingMethod.SIMPLE_KEYWORD
        
        text_lower = text.lower()
        
        # Extract entities
        self._extract_entities(text_lower, scenario)
        
        # Determine model
        self._determine_model(text_lower, scenario)
        
        # Determine lenses
        self._determine_lenses(text_lower, scenario)
        
        # Check for red flags in text
        self._check_text_red_flags(text_lower, scenario)
        
        # Add suggestions based on what was found
        self._add_suggestions(scenario)
        
        return scenario
    
    def _extract_entities(self, text: str, scenario: EthicalScenario):
        """Extract entities from text"""
        # Look for each entity type
        for keyword, entity_type in self.entity_keywords.items():
            if keyword in text:
                # Extract count if available
                count = self._extract_count_near_keyword(text, keyword)
                
                # Extract vulnerability
                vulnerability = self._extract_vulnerability_near_keyword(text, keyword)
                
                # Create description
                description = f"Affected by {keyword} scenario"
                
                scenario.add_entity(
                    entity_type=entity_type,
                    count=count,
                    description=description,
                    vulnerability=vulnerability
                )
    
    def _extract_count_near_keyword(self, text: str, keyword: str) -> int:
        """Extract numbers near a keyword"""
        # Find keyword position
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return 1
        
        # Look for numbers in surrounding text
        start_pos = max(0, keyword_pos - 50)
        end_pos = min(len(text), keyword_pos + len(keyword) + 50)
        surrounding_text = text[start_pos:end_pos]
        
        # Find all numbers
        numbers = re.findall(r'\d+', surrounding_text)
        
        if numbers:
            # Use first number found
            try:
                return int(numbers[0])
            except ValueError:
                pass
        
        # Default counts based on keyword
        if keyword in ["human", "people", "person", "user", "worker", "resident"]:
            return 10
        elif keyword in ["animal", "wildlife", "species"]:
            return 5
        elif keyword in ["plant", "tree", "flora", "vegetation"]:
            return 100
        elif keyword in ["ecosystem", "environment", "habitat"]:
            return 1
        elif keyword in ["future", "generation", "descendant"]:
            return 100
        else:
            return 1
    
    def _extract_vulnerability_near_keyword(self, text: str, keyword: str) -> float:
        """Extract vulnerability level near a keyword"""
        # Find keyword position
        keyword_pos = text.find(keyword)
        if keyword_pos == -1:
            return 1.0
        
        # Look for vulnerability indicators in surrounding text
        start_pos = max(0, keyword_pos - 100)
        end_pos = min(len(text), keyword_pos + len(keyword) + 100)
        surrounding_text = text[start_pos:end_pos]
        
        # Check for vulnerability indicators
        for indicator, vulnerability in self.vulnerability_indicators.items():
            if indicator in surrounding_text:
                return vulnerability
        
        return 1.0
    
    def _determine_model(self, text: str, scenario: EthicalScenario):
        """Determine the most appropriate ethical model"""
        model_scores = {model: 0 for model in get_available_models()}
        
        # Score each model based on keywords
        for keyword, model_name in self.model_keywords.items():
            if keyword in text:
                model_scores[model_name] += 1
        
        # Find model with highest score
        best_model = max(model_scores.items(), key=lambda x: x[1])[0]
        
        # Only change from default if we have some confidence
        if model_scores[best_model] > 0:
            scenario.set_model(best_model)
            scenario.confidence = min(0.9, scenario.confidence + 0.1)
        else:
            scenario.suggestions.append("Consider specifying the ethical model explicitly")
    
    def _determine_lenses(self, text: str, scenario: EthicalScenario):
        """Determine appropriate lenses"""
        # Check for each lens
        for keyword, lens_name in self.lens_keywords.items():
            if keyword in text:
                scenario.add_lens(lens_name)
                scenario.confidence = min(0.95, scenario.confidence + 0.05)
    
    def _check_text_red_flags(self, text: str, scenario: EthicalScenario):
        """Check for red flags in the text"""
        red_flag_keywords = [
            "nuclear", "torture", "genocide", "extinction",
            "mass surveillance", "autonomous weapons", "climate catastrophe",
            "systemic abuse", "irreversible harm", "dignity violation"
        ]
        
        for keyword in red_flag_keywords:
            if keyword in text:
                scenario.warnings.append(f"Potential red flag detected: {keyword}")
                scenario.confidence = max(0.5, scenario.confidence - 0.2)
    
    def _add_suggestions(self, scenario: EthicalScenario):
        """Add helpful suggestions based on the scenario"""
        if not scenario.entities:
            scenario.suggestions.append("Consider specifying who or what is affected by this scenario")
        
        if scenario.model == "human_centric" and any(e.entity_type != EntityType.HUMAN for e in scenario.entities):
            scenario.suggestions.append("Human-centric model may overlook non-human impacts")
        
        if not scenario.lenses and len(scenario.entities) > 2:
            scenario.suggestions.append("Consider adding lenses for more nuanced analysis")
    
    def parse_interactive(self, text: str) -> EthicalScenario:
        """Interactive parsing with user refinement"""
        # Start with simple parsing
        scenario = self.parse_simple(text)
        scenario.parsing_method = ParsingMethod.INTERACTIVE
        
        # In a real implementation, this would involve user interaction
        # For now, we'll just return the scenario with a note
        scenario.suggestions.insert(0, "Interactive refinement would allow you to adjust entities, model, and lenses")
        
        return scenario
    
    def parse_with_llm(self, text: str, llm_client: Any) -> EthicalScenario:
        """Parse using LLM (placeholder for future implementation)"""
        scenario = EthicalScenario()
        scenario.raw_text = text
        scenario.context = text[:200]
        scenario.parsing_method = ParsingMethod.LLM_ASSISTED
        scenario.warnings.append("LLM parsing not yet implemented - using simple parser")
        
        # For now, fall back to simple parsing
        simple_scenario = self.parse_simple(text)
        scenario.entities = simple_scenario.entities
        scenario.model = simple_scenario.model
        scenario.lenses = simple_scenario.lenses
        scenario.confidence = simple_scenario.confidence
        scenario.suggestions = simple_scenario.suggestions
        
        return scenario


# Singleton instance for easy access
natural_language_parser = NaturalLanguageParser()


def analyze_natural_language(text: str, method: ParsingMethod = ParsingMethod.SIMPLE_KEYWORD, 
                           llm_client: Any = None) -> EthicalScenario:
    """
    Main function to analyze natural language ethical scenarios
    
    Args:
        text: Natural language description of the scenario
        method: Parsing method to use
        llm_client: Optional LLM client for advanced parsing
        
    Returns:
        EthicalScenario object with parsed data
    """
    if method == ParsingMethod.LLM_ASSISTED and llm_client:
        return natural_language_parser.parse_with_llm(text, llm_client)
    elif method == ParsingMethod.INTERACTIVE:
        return natural_language_parser.parse_interactive(text)
    else:
        return natural_language_parser.parse_simple(text)


def ethical_analysis_from_text(text: str, method: ParsingMethod = ParsingMethod.SIMPLE_KEYWORD,
                              llm_client: Any = None) -> Dict[str, Any]:
    """
    Complete ethical analysis from natural language text
    
    Args:
        text: Natural language description
        method: Parsing method
        llm_client: Optional LLM client
        
    Returns:
        Dictionary with full ethical analysis results
    """
    # Parse the scenario
    scenario = analyze_natural_language(text, method, llm_client)
    
    # Run ethical analysis
    result = ethical_functions.minimize_suffering(
        entities=scenario.entities,
        model_name=scenario.model,
        lens_names=scenario.lenses,
        context=scenario.context
    )
    
    # Combine results
    full_result = {
        "parsing": scenario.to_dict(),
        "analysis": {
            "suffering_score": result.suffering_score,
            "impact_level": result.impact_level.name,
            "red_flags": result.red_flags,
            "suggestions": result.suggestions,
            "explanation": result.explanation
        }
    }
    
    return full_result


# Future Vision: Research Integration Framework
class ResearchIntegrationFramework:
    """
    Future: Framework for integrating external research and data
    
    This class outlines the vision for how the system could gather
    contextual data to enhance ethical analysis.
    """
    
    def __init__(self):
        self.data_sources = {
            "environmental": ["EPA databases", "Local ecosystem reports", "Climate data"],
            "demographic": ["Census data", "Community profiles", "Vulnerability indices"],
            "economic": ["Local economic reports", "Industry data", "Employment statistics"],
            "cultural": ["Heritage databases", "Indigenous knowledge sources", "Historical records"],
            "technological": ["Tech impact assessments", "AI ethics databases", "Automation studies"]
        }
        
        self.research_capabilities = [
            "location_analysis",
            "industry_impact_assessment", 
            "ecosystem_vulnerability",
            "demographic_analysis",
            "cultural_impact",
            "technological_risk"
        ]
    
    def analyze_location(self, location_description: str) -> Dict[str, Any]:
        """
        Future: Analyze a location for environmental and social factors
        
        Example: "building in Portland, Oregon near the Willamette River"
        Would return data on:
        - Local ecosystems
        - Protected species
        - Environmental regulations
        - Community demographics
        - Historical context
        """
        return {
            "status": "not_implemented",
            "message": "Location analysis would provide environmental and social context data",
            "example_data": {
                "ecosystems": ["Willamette River ecosystem", "Urban wetlands"],
                "protected_species": ["Chinook salmon", "Bald eagles"],
                "community_impact": "Medium - mixed residential and commercial area",
                "regulations": ["Clean Water Act", "Local zoning laws"]
            }
        }
    
    def assess_industry_impact(self, industry: str) -> Dict[str, Any]:
        """
        Future: Assess typical impacts of an industry
        
        Example: "apartment building construction"
        Would return data on:
        - Typical environmental impacts
        - Common social effects
        - Regulatory considerations
        - Best practices
        """
        return {
            "status": "not_implemented",
            "message": "Industry impact assessment would provide sector-specific insights",
            "example_data": {
                "environmental_impacts": ["Habitat disruption", "Water usage", "Construction waste"],
                "social_effects": ["Housing availability", "Gentrification risk", "Community displacement"],
                "mitigation_strategies": ["Green building practices", "Community consultation", "Affordable housing quotas"]
            }
        }
    
    def get_ecosystem_data(self, ecosystem_type: str, location: str) -> Dict[str, Any]:
        """
        Future: Get detailed ecosystem data
        
        Example: get_ecosystem_data("urban wetland", "Portland, OR")
        Would return:
        - Species present
        - Ecological value
        - Threats and vulnerabilities
        - Protection status
        """
        return {
            "status": "not_implemented",
            "message": "Ecosystem data would provide detailed environmental context",
            "example_data": {
                "species": ["Red-legged frog", "Western pond turtle", "Migratory birds"],
                "ecological_value": "High - supports biodiversity and flood control",
                "threats": ["Urban development", "Pollution", "Invasive species"],
                "protection": "Partially protected under local wetlands ordinance"
            }
        }
    
    def enhanced_ethical_analysis(self, scenario_text: str, location: str = "", 
                                  industry: str = "") -> Dict[str, Any]:
        """
        Future: Enhanced analysis with research integration
        
        This would combine:
        1. Natural language parsing
        2. Location-based research
        3. Industry-specific data
        4. Ethical analysis
        """
        result = {
            "status": "future_vision",
            "current_capabilities": "Natural language parsing and ethical analysis",
            "future_enhancements": [
                "Automatic location research",
                "Industry impact databases",
                "Real-time environmental data",
                "Community impact modeling",
                "Regulatory compliance checking"
            ],
            "example_workflow": {
                "input": "building a 200-unit apartment complex in Portland near the Willamette River",
                "steps": [
                    "1. Parse natural language to extract entities and context",
                    "2. Research Portland location (ecosystems, regulations, demographics)",
                    "3. Analyze apartment construction industry impacts",
                    "4. Assess specific site characteristics",
                    "5. Run enhanced ethical analysis with contextual data",
                    "6. Generate comprehensive report with mitigation suggestions"
                ],
                "output": "Detailed ethical impact assessment with actionable recommendations"
            }
        }
        
        return result


# Singleton instance for research framework
research_framework = ResearchIntegrationFramework()