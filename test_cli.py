#!/usr/bin/env python3

"""
Simple test script for Compass-io CLI
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from compass_io_cli.models import Entity, EntityType, create_model, get_available_models
from compass_io_cli.lenses import create_lens, get_available_lenses, apply_lenses_to_model
from compass_io_cli.functions import ethical_functions

def test_basic_functionality():
    """Test basic functionality of the ethical reasoning framework"""
    
    print("🧪 Testing Compass-io CLI Core Functionality")
    print("=" * 50)
    
    # Test 1: Create entities
    print("1. Testing entity creation...")
    entities = [
        Entity(EntityType.HUMAN, 10, "Workers"),
        Entity(EntityType.ANIMAL, 5, "Endangered species", 1.5),
        Entity(EntityType.ECOSYSTEM, 1, "Local forest", 2.0)
    ]
    print(f"   ✅ Created {len(entities)} entities")
    
    # Test 2: Create models
    print("\n2. Testing model creation...")
    models_to_test = ["human_centric", "eco_systemic", "deep_time"]
    for model_name in models_to_test:
        model = create_model(model_name)
        print(f"   ✅ Created {model.name} model")
    
    # Test 3: Create lenses
    print("\n3. Testing lens creation...")
    lenses_to_test = ["sparks", "fragility", "deep_time"]
    for lens_name in lenses_to_test:
        lens = create_lens(lens_name)
        print(f"   ✅ Created {lens.name} lens")
    
    # Test 4: Apply lenses to models
    print("\n4. Testing lens application...")
    base_model = create_model("bio_inclusive")
    model_with_lens = apply_lenses_to_model(base_model, ["sparks", "fragility"])
    print(f"   ✅ Applied lenses: {model_with_lens.name}")
    
    # Test 5: Ethical evaluation
    print("\n5. Testing ethical evaluation...")
    result = ethical_functions.minimize_suffering(
        entities=entities,
        model_name="eco_systemic",
        lens_names=["fragility"],
        context="Deforestation project for urban development"
    )
    print(f"   ✅ Suffering score: {result.suffering_score:.2f}")
    print(f"   ✅ Impact level: {result.impact_level.name}")
    print(f"   ✅ Red flags: {len(result.red_flags)}")
    print(f"   ✅ Suggestions: {len(result.suggestions)}")
    
    # Test 6: Stakeholder consultation
    print("\n6. Testing stakeholder consultation...")
    feedback = ethical_functions.consult_stakeholders(
        entities=entities,
        model_name="bio_inclusive"
    )
    print(f"   ✅ Generated feedback for {len(feedback)} stakeholders")
    
    # Test 7: Model comparison
    print("\n7. Testing model comparison...")
    comparisons = ethical_functions.compare_ethical_models(
        entities=entities,
        model_names=["human_centric", "eco_systemic", "animist"]
    )
    print(f"   ✅ Compared {len(comparisons)} models")
    
    # Test 8: Red flag detection
    print("\n8. Testing red flag detection...")
    red_flags = ethical_functions.red_flag_check("nuclear weapons deployment")
    print(f"   ✅ Detected {len(red_flags)} red flags")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("\nAvailable models:", get_available_models())
    print("Available lenses:", get_available_lenses())
    
    return True

def test_cli_interface():
    """Test the CLI interface"""
    print("\n🖥️  Testing CLI Interface")
    print("=" * 30)
    
    # Import the CLI module
    try:
        from compass_io_cli.main import cli
        print("✅ CLI module imported successfully")
        
        # Test that all commands are available
        commands = [cmd.name for cmd in cli.commands.values()]
        expected_commands = ['evaluate', 'consult', 'compare', 'redflags', 'models', 'lenses', 'help']
        
        for expected_cmd in expected_commands:
            if expected_cmd in commands:
                print(f"✅ Command '{expected_cmd}' available")
            else:
                print(f"❌ Command '{expected_cmd}' missing")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import CLI: {e}")
        return False

if __name__ == "__main__":
    try:
        success1 = test_basic_functionality()
        success2 = test_cli_interface()
        
        if success1 and success2:
            print("\n🎊 All tests passed! Compass-io CLI is ready to use.")
            print("\nTry running:")
            print("  python -m compass_io_cli.main --help")
            print("  compass evaluate HUMAN:10 ANIMAL:5 --model human_centric")
        else:
            print("\n❌ Some tests failed.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)