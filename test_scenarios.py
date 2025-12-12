#!/usr/bin/env python3

"""
Test scenarios for Compass-io CLI

This script demonstrates various real-world scenarios using the ethical reasoning framework.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from compass_io_cli.models import Entity, EntityType
from compass_io_cli.functions import ethical_functions

def run_scenario(name, description, entities, model_name, lens_names=None, context=""):
    """Run a scenario and display results"""
    print(f"\n{'='*60}")
    print(f"📋 SCENARIO: {name}")
    print(f"{'='*60}")
    print(f"Description: {description}")
    print(f"Model: {model_name}")
    if lens_names:
        print(f"Lenses: {', '.join(lens_names)}")
    print(f"Context: {context}")
    print()
    
    # Run evaluation
    result = ethical_functions.minimize_suffering(
        entities=entities,
        model_name=model_name,
        lens_names=lens_names,
        context=context
    )
    
    # Display key results
    print(f"📊 RESULTS:")
    print(f"Suffering Score: {result.suffering_score:.2f}")
    print(f"Impact Level: {result.impact_level.name}")
    
    if result.red_flags:
        print(f"🚩 RED FLAGS ({len(result.red_flags)}):")
        for flag in result.red_flags:
            print(f"  • {flag}")
    
    print(f"💡 KEY SUGGESTIONS:")
    for i, suggestion in enumerate(result.suggestions[:3]):  # Show first 3 suggestions
        print(f"  {i+1}. {suggestion}")
    
    return result

def main():
    """Run all test scenarios"""
    
    print("🧪 COMPASS-IO CLI - TEST SCENARIOS")
    print("=" * 60)
    print("Testing various real-world ethical decision scenarios")
    
    # Scenario 1: Urban Development
    scenario1_entities = [
        Entity(EntityType.HUMAN, 50, "Workers and residents", 1.0),
        Entity(EntityType.ANIMAL, 20, "Local wildlife", 1.2),
        Entity(EntityType.PLANT, 500, "Local flora", 1.0),
        Entity(EntityType.ECOSYSTEM, 1, "Urban park", 1.5)
    ]
    
    run_scenario(
        name="Urban Development Project",
        description="Building a new housing complex that requires clearing a local park",
        entities=scenario1_entities,
        model_name="bio_inclusive",
        lens_names=["fragility"],
        context="Urban development project"
    )
    
    # Scenario 2: AI Development
    scenario2_entities = [
        Entity(EntityType.HUMAN, 1000, "Current users", 1.0),
        Entity(EntityType.FUTURE_BEING, 10000, "Future generations", 1.5),
        Entity(EntityType.SYMBOLIC_ENTITY, 1, "Cultural impact of AI", 1.2)
    ]
    
    run_scenario(
        name="AI Development Ethics",
        description="Developing advanced AI systems with long-term societal impacts",
        entities=scenario2_entities,
        model_name="intergenerational",
        lens_names=["deep_time", "sparks"],
        context="AI alignment research and development"
    )
    
    # Scenario 3: Environmental Policy
    scenario3_entities = [
        Entity(EntityType.ECOSYSTEM, 5, "Coastal ecosystems", 2.0),
        Entity(EntityType.ANIMAL, 500, "Marine life", 1.8),
        Entity(EntityType.PLANT, 10000, "Mangrove forests", 1.5),
        Entity(EntityType.HUMAN, 100, "Local fishing communities", 1.3),
        Entity(EntityType.FUTURE_BEING, 5000, "Future coastal residents", 1.5)
    ]
    
    run_scenario(
        name="Climate Change Mitigation",
        description="Policy to protect coastal ecosystems from rising sea levels",
        entities=scenario3_entities,
        model_name="eco_systemic",
        lens_names=["fragility"],
        context="Climate change adaptation policy"
    )
    
    # Scenario 4: Healthcare Resource Allocation
    scenario4_entities = [
        Entity(EntityType.HUMAN, 1000, "General population", 1.0),
        Entity(EntityType.HUMAN, 100, "Vulnerable elderly", 2.5),
        Entity(EntityType.HUMAN, 50, "Chronically ill patients", 2.0),
        Entity(EntityType.HUMAN, 20, "Healthcare workers", 1.8)
    ]
    
    run_scenario(
        name="Healthcare Resource Allocation",
        description="Allocating limited medical resources during a crisis",
        entities=scenario4_entities,
        model_name="human_centric",
        lens_names=["sparks"],  # Sparks lens helps avoid bias
        context="Medical resource allocation during pandemic"
    )
    
    # Scenario 5: Technology Deployment
    scenario5_entities = [
        Entity(EntityType.HUMAN, 5000, "Technology users", 1.0),
        Entity(EntityType.HUMAN, 50, "Vulnerable populations", 2.0),
        Entity(EntityType.SYMBOLIC_ENTITY, 1, "Cultural impact", 1.2),
        Entity(EntityType.FUTURE_BEING, 2000, "Future technology impact", 1.3)
    ]
    
    run_scenario(
        name="Social Media Algorithm Changes",
        description="Deploying new algorithms that affect user behavior and mental health",
        entities=scenario5_entities,
        model_name="animist",  # Animist model considers symbolic impacts
        lens_names=["fragility"],
        context="Social media algorithm deployment with potential mental health impacts"
    )
    
    # Scenario 6: Red Flag Detection Test
    print(f"\n{'='*60}")
    print(f"🚩 RED FLAG DETECTION TEST")
    print(f"{'='*60}")
    
    dangerous_contexts = [
        "nuclear weapons deployment",
        "autonomous weapons system with no human oversight",
        "mass surveillance of entire population",
        "ecosystem destruction for short-term profit",
        "torture-based interrogation methods"
    ]
    
    for context in dangerous_contexts:
        red_flags = ethical_functions.red_flag_check(context)
        print(f"\nContext: '{context}'")
        print(f"Red flags detected: {len(red_flags)}")
        if red_flags:
            print(f"  • {red_flags[0]}")  # Show first red flag
    
    # Scenario 7: Model Comparison
    print(f"\n{'='*60}")
    print(f"📊 MODEL COMPARISON TEST")
    print(f"{'='*60}")
    
    comparison_entities = [
        Entity(EntityType.HUMAN, 100, "Workers", 1.0),
        Entity(EntityType.ANIMAL, 50, "Wildlife", 1.2),
        Entity(EntityType.ECOSYSTEM, 2, "Forests", 1.5)
    ]
    
    models_to_compare = ["human_centric", "sentience_based", "eco_systemic", "animist"]
    
    comparisons = ethical_functions.compare_ethical_models(
        entities=comparison_entities,
        model_names=models_to_compare,
        context="Industrial development project"
    )
    
    print("Comparing different ethical models for the same scenario:")
    for comp in comparisons:
        print(f"\n{comp.model_name}:")
        print(f"  Suffering Score: {comp.suffering_score:.2f}")
        print(f"  Impact Level: {comp.impact_level.name}")
        if comp.key_differences:
            print(f"  Key Differences: {comp.key_differences[0]}")
    
    print(f"\n{'='*60}")
    print("🎉 SCENARIO TESTING COMPLETE")
    print(f"{'='*60}")
    print("\nKey Insights:")
    print("• Different ethical models can produce vastly different results")
    print("• Lenses modify the analysis to highlight specific concerns")
    print("• Red flag detection helps identify critical ethical violations")
    print("• Vulnerability scores significantly impact suffering calculations")
    print("• Context matters for comprehensive ethical analysis")
    print("\nThe Compass-io CLI is ready for real-world ethical reasoning!")

if __name__ == "__main__":
    main()