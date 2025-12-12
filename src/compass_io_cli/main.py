
def show_detailed_help():
    """Show detailed help with examples."""
def show_detailed_help():
    """Show detailed help with examples.""""""
Main CLI interface for Compass-io

This module provides the command-line interface for the ethical reasoning framework.
"""

import click
import json
from typing import List, Optional, Dict, Any
from .models import Entity, EntityType, get_available_models
from .lenses import get_available_lenses
from .functions import ethical_functions, EthicalEvaluation
from .natural_language import ParsingMethod, ethical_analysis_from_text


@click.group()
@click.version_option(version="0.1.0", message="Compass-io CLI - Ethical Reasoning Framework")
def cli():
    """Compass-io CLI - A configurable ethical framework for decision-making."""
    pass


@cli.command()
@click.argument("entities", nargs=-1, required=True)
@click.option("--model", "-m", default="human_centric", 
              help="Ethical model to use", 
              type=click.Choice(get_available_models()))
@click.option("--lens", "-l", multiple=True, 
              help="Lenses to apply", 
              type=click.Choice(get_available_lenses()))
@click.option("--context", "-c", default="", 
              help="Additional context about the decision")
@click.option("--json", "-j", is_flag=True, 
              help="Output results in JSON format")
def evaluate(entities: List[str], model: str, lens: List[str], context: str, json: bool):
    """Evaluate the ethical impact of a decision."""
    
    try:
        # Parse entities from command line arguments
        parsed_entities = parse_entities(entities)
        
        # Perform ethical evaluation
        result = ethical_functions.minimize_suffering(
            entities=parsed_entities,
            model_name=model,
            lens_names=list(lens) if lens else None,
            context=context
        )
        
        # Output results
        if json:
            output_json_result(result)
        else:
            output_text_result(result)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("Use --help for usage information")


@cli.command()
@click.argument("entities", nargs=-1, required=True)
@click.option("--model", "-m", default="human_centric", 
              help="Ethical model to use", 
              type=click.Choice(get_available_models()))
@click.option("--lens", "-l", multiple=True, 
              help="Lenses to apply", 
              type=click.Choice(get_available_lenses()))
@click.option("--json", "-j", is_flag=True, 
              help="Output results in JSON format")
def consult(entities: List[str], model: str, lens: List[str], json: bool):
    """Consult stakeholders affected by a decision."""
    
    try:
        # Parse entities from command line arguments
        parsed_entities = parse_entities(entities)
        
        # Perform stakeholder consultation
        feedback = ethical_functions.consult_stakeholders(
            entities=parsed_entities,
            model_name=model,
            lens_names=list(lens) if lens else None
        )
        
        # Output results
        if json:
            output_json_stakeholder_feedback(feedback)
        else:
            output_text_stakeholder_feedback(feedback)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("Use --help for usage information")


@cli.command()
@click.argument("entities", nargs=-1, required=True)
@click.option("--models", "-m", multiple=True, 
              help="Ethical models to compare (default: all)", 
              type=click.Choice(get_available_models()))
@click.option("--lens", "-l", multiple=True, 
              help="Lenses to apply to all models", 
              type=click.Choice(get_available_lenses()))
@click.option("--context", "-c", default="", 
              help="Additional context about the decision")
@click.option("--json", "-j", is_flag=True, 
              help="Output results in JSON format")
def compare(entities: List[str], models: List[str], lens: List[str], context: str, json: bool):
    """Compare ethical impact across different models."""
    
    try:
        # Parse entities from command line arguments
        parsed_entities = parse_entities(entities)
        
        # Use all models if none specified
        if not models:
            models_to_compare = get_available_models()
        else:
            models_to_compare = list(models)
        
        # Perform model comparison
        comparisons = ethical_functions.compare_ethical_models(
            entities=parsed_entities,
            model_names=models_to_compare,
            lens_names=list(lens) if lens else None,
            context=context
        )
        
        # Output results
        if json:
            output_json_comparison(comparisons)
        else:
            output_text_comparison(comparisons)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("Use --help for usage information")


@cli.command()
@click.argument("context")
@click.option("--json", "-j", is_flag=True, 
              help="Output results in JSON format")
def redflags(context: str, json: bool):
    """Check for critical ethical red flags in a decision."""
    
    try:
        # Perform red flag check
        red_flags = ethical_functions.red_flag_check(context=context)
        
        # Output results
        if json:
            output_json_red_flags(red_flags)
        else:
            output_text_red_flags(red_flags)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("Use --help for usage information")


@cli.command()
def models():
    """List available ethical models."""
    click.echo("Available Ethical Models:")
    click.echo("=" * 50)
    
    for model_name in get_available_models():
        model = __import__('compass_io_cli.models', fromlist=['create_model']).create_model(model_name)
        click.echo(f"• {model.name} ({model_name})")
        click.echo(f"  {model.description}")
        click.echo()


@cli.command()
def lenses():
    """List available lenses."""
    click.echo("Available Lenses:")
    click.echo("=" * 50)
    
    for lens_name in get_available_lenses():
        lens_class = __import__('compass_io_cli.lenses', fromlist=['create_lens']).create_lens(lens_name)
        click.echo(f"• {lens_class.name} ({lens_name})")
        click.echo(f"  {lens_class.description}")
        click.echo()


@cli.command()
@click.argument('scenario', nargs=-1)
@click.option('--method', '-m', default='simple', 
              help='Parsing method (simple, interactive, llm)',
              type=click.Choice(['simple', 'interactive', 'llm']))
@click.option('--json', '-j', is_flag=True, 
              help='Output results in JSON format')
def analyze(scenario, method, json):
    """Analyze a natural language ethical scenario."""
    
    try:
        text = ' '.join(scenario)
        if not text:
            raise ValueError("No scenario provided")
        
        # Map method string to ParsingMethod
        method_map = {
            'simple': ParsingMethod.SIMPLE_KEYWORD,
            'interactive': ParsingMethod.INTERACTIVE,
            'llm': ParsingMethod.LLM_ASSISTED
        }
        
        # For now, LLM method falls back to simple
        parsing_method = method_map.get(method, ParsingMethod.SIMPLE_KEYWORD)
        
        # Perform analysis
        result = ethical_analysis_from_text(text, parsing_method)
        
        # Output results
        if json:
            output_json_natural_language(result)
        else:
            output_text_natural_language(result)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        click.echo("Use 'compass help' for usage information")


@cli.command()
def help():
    """Show detailed help and examples."""
    show_detailed_help()


def parse_entities(entity_args: List[str]) -> List[Entity]:
    """Parse entity arguments from command line."""
    entities = []
    
    for arg in entity_args:
        # Format: type[:count[:vulnerability[:description]]]
        parts = arg.split(":")
        
        if len(parts) < 1:
            raise ValueError(f"Invalid entity format: {arg}")
        
        entity_type_str = parts[0].upper()
        count = int(parts[1]) if len(parts) > 1 else 1
        vulnerability = float(parts[2]) if len(parts) > 2 else 1.0
        description = parts[3] if len(parts) > 3 else ""
        
        # Map string to EntityType
        try:
            entity_type = EntityType[entity_type_str]
        except KeyError:
            raise ValueError(f"Unknown entity type: {entity_type_str}. Available types: {[e.name for e in EntityType]}")
        
        entities.append(Entity(
            entity_type=entity_type,
            count=count,
            vulnerability=vulnerability,
            description=description
        ))
    
    return entities


def output_text_result(result: EthicalEvaluation):
    """Output ethical evaluation in text format."""
    click.echo("=" * 60)
    click.echo("ETHICAL EVALUATION RESULTS")
    click.echo("=" * 60)
    
    click.echo(f"Suffering Score: {result.suffering_score:.2f}")
    click.echo(f"Impact Level: {result.impact_level.name}")
    click.echo()
    
    if result.red_flags:
        click.echo("🚩 RED FLAGS DETECTED:")
        for flag in result.red_flags:
            click.echo(f"  • {flag}")
        click.echo()
    
    click.echo("📊 AFFECTED ENTITIES:")
    for entity in result.affected_entities:
        entity_type_str = entity.entity_type.name.replace("_", " ").title()
        click.echo(f"  • {entity.count} {entity_type_str}")
        if entity.description:
            click.echo(f"    ({entity.description})")
    click.echo()
    
    click.echo("💡 SUGGESTIONS:")
    for suggestion in result.suggestions:
        click.echo(f"  • {suggestion}")
    click.echo()
    
    click.echo("📝 DETAILED EXPLANATION:")
    click.echo(result.explanation)


def output_json_result(result: EthicalEvaluation):
    """Output ethical evaluation in JSON format."""
    output = {
        "suffering_score": result.suffering_score,
        "impact_level": result.impact_level.name,
        "red_flags": result.red_flags,
        "suggestions": result.suggestions,
        "affected_entities": [{
            "type": entity.entity_type.name,
            "count": entity.count,
            "vulnerability": entity.vulnerability,
            "description": entity.description
        } for entity in result.affected_entities],
        "explanation": result.explanation
    }
    
    click.echo(json.dumps(output, indent=2))


def output_text_stakeholder_feedback(feedback: List):
    """Output stakeholder feedback in text format."""
    click.echo("=" * 60)
    click.echo("STAKEHOLDER CONSULTATION RESULTS")
    click.echo("=" * 60)
    
    for item in feedback:
        entity_type_str = item.entity_type.name.replace("_", " ").title()
        click.echo(f"📋 {entity_type_str} ({item.count} affected)")
        click.echo(f"Suffering Score: {item.suffering_score:.2f}")
        
        if item.concerns:
            click.echo("Concerns:")
            for concern in item.concerns:
                click.echo(f"  • {concern}")
        
        click.echo()


def output_json_stakeholder_feedback(feedback: List):
    """Output stakeholder feedback in JSON format."""
    output = [{
        "entity_type": item.entity_type.name,
        "count": item.count,
        "suffering_score": item.suffering_score,
        "concerns": item.concerns
    } for item in feedback]
    
    click.echo(json.dumps(output, indent=2))


def output_text_comparison(comparisons: List):
    """Output model comparison in text format."""
    click.echo("=" * 60)
    click.echo("ETHICAL MODEL COMPARISON")
    click.echo("=" * 60)
    
    for comparison in comparisons:
        click.echo(f"📊 {comparison.model_name}")
        click.echo(f"Suffering Score: {comparison.suffering_score:.2f}")
        click.echo(f"Impact Level: {comparison.impact_level.name}")
        
        if comparison.key_differences:
            click.echo("Key Differences:")
            for diff in comparison.key_differences:
                click.echo(f"  • {diff}")
        
        click.echo()


def output_json_comparison(comparisons: List):
    """Output model comparison in JSON format."""
    output = [{
        "model_name": comp.model_name,
        "suffering_score": comp.suffering_score,
        "impact_level": comp.impact_level.name,
        "key_differences": comp.key_differences
    } for comp in comparisons]
    
    click.echo(json.dumps(output, indent=2))


def output_text_red_flags(red_flags: List[str]):
    """Output red flags in text format."""
    if red_flags:
        click.echo("🚩 CRITICAL RED FLAGS DETECTED:")
        for flag in red_flags:
            click.echo(f"  • {flag}")
    else:
        click.echo("✅ No critical red flags detected")


def output_json_red_flags(red_flags: List[str]):
    """Output red flags in JSON format."""
    output = {"red_flags": red_flags, "critical": len(red_flags) > 0}
    click.echo(json.dumps(output, indent=2))


def output_text_natural_language(result: Dict):
    """Output natural language analysis in text format."""
    parsing = result.get('parsing', {})
    analysis = result.get('analysis', {})
    
    click.echo("=" * 60)
    click.echo("NATURAL LANGUAGE ETHICAL ANALYSIS")
    click.echo("=" * 60)
    
    # Parsing information
    click.echo("📋 PARSING RESULTS:")
    click.echo(f"Method: {parsing.get('parsing_method', 'unknown').replace('_', ' ').title()}")
    click.echo(f"Confidence: {parsing.get('confidence', 0.7):.1%}")
    
    if parsing.get('warnings'):
        click.echo(f"⚠️  Warnings: {len(parsing['warnings'])}")
        for warning in parsing['warnings']:
            click.echo(f"  • {warning}")
    
    click.echo(f"\n👥 EXTRACTED ENTITIES:")
    for entity in parsing.get('entities', []):
        entity_type = entity['type'].replace('_', ' ').title()
        click.echo(f"  • {entity['count']} {entity_type}")
        if entity.get('vulnerability') != 1.0:
            click.echo(f"    Vulnerability: {entity['vulnerability']:.1f}x")
        if entity.get('description'):
            click.echo(f"    Description: {entity['description']}")
    
    click.echo(f"\n🎯 SELECTED MODEL:")
    click.echo(f"  {parsing.get('model', 'human_centric').replace('_', ' ').title()}")
    
    if parsing.get('lenses'):
        click.echo(f"\n👓 SELECTED LENSES:")
        for lens in parsing['lenses']:
            click.echo(f"  • {lens.replace('_', ' ').title()}")
    
    if parsing.get('suggestions'):
        click.echo(f"\n💡 PARSING SUGGESTIONS:")
        for suggestion in parsing['suggestions']:
            click.echo(f"  • {suggestion}")
    
    # Analysis results
    click.echo(f"\n📊 ETHICAL ANALYSIS:")
    click.echo(f"Suffering Score: {analysis.get('suffering_score', 0):.2f}")
    click.echo(f"Impact Level: {analysis.get('impact_level', 'unknown')}")
    
    if analysis.get('red_flags'):
        click.echo(f"\n🚩 RED FLAGS:")
        for flag in analysis['red_flags']:
            click.echo(f"  • {flag}")
    
    if analysis.get('suggestions'):
        click.echo(f"\n💡 RECOMMENDATIONS:")
        for suggestion in analysis['suggestions']:
            click.echo(f"  • {suggestion}")
    
    click.echo(f"\n📝 DETAILED EXPLANATION:")
    click.echo(analysis.get('explanation', 'No explanation available'))


def output_json_natural_language(result: Dict):
    """Output natural language analysis in JSON format."""
def output_text_natural_language(result: Dict):
    """Output natural language analysis in text format."""
    parsing = result.get('parsing', {})
    analysis = result.get('analysis', {})
    
    click.echo("=" * 60)
    click.echo("NATURAL LANGUAGE ETHICAL ANALYSIS")
    click.echo("=" * 60)
    
    # Parsing information
    click.echo("📋 PARSING RESULTS:")
    click.echo(f"Method: {parsing.get('parsing_method', 'unknown').replace('_', ' ').title()}")
    click.echo(f"Confidence: {parsing.get('confidence', 0.7):.1%}")
    
    if parsing.get('warnings'):
        click.echo(f"⚠️  Warnings: {len(parsing['warnings'])}")
        for warning in parsing['warnings']:
            click.echo(f"  • {warning}")
    
    click.echo(f"\n👥 EXTRACTED ENTITIES:")
    for entity in parsing.get('entities', []):
        entity_type = entity['type'].replace('_', ' ').title()
        click.echo(f"  • {entity['count']} {entity_type}")
        if entity.get('vulnerability') != 1.0:
            click.echo(f"    Vulnerability: {entity['vulnerability']:.1f}x")
        if entity.get('description'):
            click.echo(f"    Description: {entity['description']}")
    
    click.echo(f"\n🎯 SELECTED MODEL:")
    click.echo(f"  {parsing.get('model', 'human_centric').replace('_', ' ').title()}")
    
    if parsing.get('lenses'):
        click.echo(f"\n👓 SELECTED LENSES:")
        for lens in parsing['lenses']:
            click.echo(f"  • {lens.replace('_', ' ').title()}")
    
    if parsing.get('suggestions'):
        click.echo(f"\n💡 PARSING SUGGESTIONS:")
        for suggestion in parsing['suggestions']:
            click.echo(f"  • {suggestion}")
    
    # Analysis results
    click.echo(f"\n📊 ETHICAL ANALYSIS:")
    click.echo(f"Suffering Score: {analysis.get('suffering_score', 0):.2f}")
    click.echo(f"Impact Level: {analysis.get('impact_level', 'unknown')}")
    
    if analysis.get('red_flags'):
        click.echo(f"\n🚩 RED FLAGS:")
        for flag in analysis['red_flags']:
            click.echo(f"  • {flag}")
    
    if analysis.get('suggestions'):
        click.echo(f"\n💡 RECOMMENDATIONS:")
        for suggestion in analysis['suggestions']:
            click.echo(f"  • {suggestion}")
    
    click.echo(f"\n📝 DETAILED EXPLANATION:")
    click.echo(analysis.get('explanation', 'No explanation available'))


def output_json_natural_language(result: Dict):
    """Output natural language analysis in JSON format."""
    click.echo(json.dumps(result, indent=2))


def output_text_natural_language(result: Dict):
    """Output natural language analysis in text format."""
    parsing = result.get('parsing', {})
    analysis = result.get('analysis', {})
    
    click.echo("=" * 60)
    click.echo("NATURAL LANGUAGE ETHICAL ANALYSIS")
    click.echo("=" * 60)
    
    # Parsing information
    click.echo("📋 PARSING RESULTS:")
    click.echo(f"Method: {parsing.get('parsing_method', 'unknown').replace('_', ' ').title()}")
    click.echo(f"Confidence: {parsing.get('confidence', 0.7):.1%}")
    
    if parsing.get('warnings'):
        click.echo(f"⚠️  Warnings: {len(parsing['warnings'])}")
        for warning in parsing['warnings']:
            click.echo(f"  • {warning}")
    
    click.echo(f"\n👥 EXTRACTED ENTITIES:")
    for entity in parsing.get('entities', []):
        entity_type = entity['type'].replace('_', ' ').title()
        click.echo(f"  • {entity['count']} {entity_type}")
        if entity.get('vulnerability') != 1.0:
            click.echo(f"    Vulnerability: {entity['vulnerability']:.1f}x")
        if entity.get('description'):
            click.echo(f"    Description: {entity['description']}")
    
    click.echo(f"\n🎯 SELECTED MODEL:")
    click.echo(f"  {parsing.get('model', 'human_centric').replace('_', ' ').title()}")
    
    if parsing.get('lenses'):
        click.echo(f"\n👓 SELECTED LENSES:")
        for lens in parsing['lenses']:
            click.echo(f"  • {lens.replace('_', ' ').title()}")
    
    if parsing.get('suggestions'):
        click.echo(f"\n💡 PARSING SUGGESTIONS:")
        for suggestion in parsing['suggestions']:
            click.echo(f"  • {suggestion}")
    
    # Analysis results
    click.echo(f"\n📊 ETHICAL ANALYSIS:")
    click.echo(f"Suffering Score: {analysis.get('suffering_score', 0):.2f}")
    click.echo(f"Impact Level: {analysis.get('impact_level', 'unknown')}")
    
    if analysis.get('red_flags'):
        click.echo(f"\n🚩 RED FLAGS:")
        for flag in analysis['red_flags']:
            click.echo(f"  • {flag}")
    
    if analysis.get('suggestions'):
        click.echo(f"\n💡 RECOMMENDATIONS:")
        for suggestion in analysis['suggestions']:
            click.echo(f"  • {suggestion}")
    
    click.echo(f"\n📝 DETAILED EXPLANATION:")
    click.echo(analysis.get('explanation', 'No explanation available'))


def output_json_natural_language(result: Dict):
    """Output natural language analysis in JSON format."""
    click.echo(json.dumps(result, indent=2))


def show_detailed_help():
    """Show detailed help with examples."""
def output_text_natural_language(result: Dict):
    """Output natural language analysis in text format."""
    parsing = result.get('parsing', {})
    analysis = result.get('analysis', {})
    
    click.echo("=" * 60)
    click.echo("NATURAL LANGUAGE ETHICAL ANALYSIS")
    click.echo("=" * 60)
    
    # Parsing information
    click.echo("📋 PARSING RESULTS:")
    click.echo(f"Method: {parsing.get('parsing_method', 'unknown').replace('_', ' ').title()}")
    click.echo(f"Confidence: {parsing.get('confidence', 0.7):.1%}")
    
    if parsing.get('warnings'):
        click.echo(f"⚠️  Warnings: {len(parsing['warnings'])}")
        for warning in parsing['warnings']:
            click.echo(f"  • {warning}")
    
    click.echo(f"\n👥 EXTRACTED ENTITIES:")
    for entity in parsing.get('entities', []):
        entity_type = entity['type'].replace('_', ' ').title()
        click.echo(f"  • {entity['count']} {entity_type}")
        if entity.get('vulnerability') != 1.0:
            click.echo(f"    Vulnerability: {entity['vulnerability']:.1f}x")
        if entity.get('description'):
            click.echo(f"    Description: {entity['description']}")
    
    click.echo(f"\n🎯 SELECTED MODEL:")
    click.echo(f"  {parsing.get('model', 'human_centric').replace('_', ' ').title()}")
    
    if parsing.get('lenses'):
        click.echo(f"\n👓 SELECTED LENSES:")
        for lens in parsing['lenses']:
            click.echo(f"  • {lens.replace('_', ' ').title()}")
    
    if parsing.get('suggestions'):
        click.echo(f"\n💡 PARSING SUGGESTIONS:")
        for suggestion in parsing['suggestions']:
            click.echo(f"  • {suggestion}")
    
    # Analysis results
    click.echo(f"\n📊 ETHICAL ANALYSIS:")
    click.echo(f"Suffering Score: {analysis.get('suffering_score', 0):.2f}")
    click.echo(f"Impact Level: {analysis.get('impact_level', 'unknown')}")
    
    if analysis.get('red_flags'):
        click.echo(f"\n🚩 RED FLAGS:")
        for flag in analysis['red_flags']:
            click.echo(f"  • {flag}")
    
    if analysis.get('suggestions'):
        click.echo(f"\n💡 RECOMMENDATIONS:")
        for suggestion in analysis['suggestions']:
            click.echo(f"  • {suggestion}")
    
    click.echo(f"\n📝 DETAILED EXPLANATION:")
    click.echo(analysis.get('explanation', 'No explanation available'))


def output_json_natural_language(result: Dict):
    """Output natural language analysis in JSON format."""
    click.echo(json.dumps(result, indent=2))


def show_detailed_help():
    """Show detailed help with examples."""
    click.echo("=" * 60)
    click.echo("COMPASS-IO CLI - DETAILED HELP")
    click.echo("=" * 60)
    click.echo()
    
    click.echo("Compass-io is a configurable ethical framework for decision-making.")
    click.echo("It helps evaluate the ethical impact of decisions across different models.")
    click.echo()
    
    click.echo("📖 BASIC USAGE:")
    click.echo()
    click.echo("1. Evaluate a decision (structured):")
    click.echo("   compass evaluate HUMAN:10 ANIMAL:5 --model human_centric")
    click.echo()
    click.echo("2. Analyze natural language:")
    click.echo("   compass analyze \"building an apartment complex affecting 100 residents and local wildlife\"")
    click.echo()
    click.echo("3. Consult stakeholders:")
    click.echo("   compass consult HUMAN:100 ECOSYSTEM:2 --model eco_systemic")
    click.echo()
    click.echo("4. Compare models:")
    click.echo("   compass compare HUMAN:50 ANIMAL:20 --models human_centric --models bio_inclusive")
    click.echo()
    click.echo("5. Check for red flags:")
    click.echo("   compass redflags \"deployment of autonomous weapons\"")
    click.echo()
    
    click.echo("🎯 ENTITY FORMAT:")
    click.echo("Entities are specified as: TYPE[:COUNT[:VULNERABILITY[:DESCRIPTION]]]")
    click.echo()
    click.echo("Available entity types:")
    for entity_type in EntityType:
        click.echo(f"  • {entity_type.name}")
    click.echo()
    click.echo("Examples:")
    click.echo("  • HUMAN:100                  # 100 humans")
    click.echo("  • ANIMAL:50:1.5              # 50 animals with 1.5x vulnerability")
    click.echo("  • ECOSYSTEM:5:2.0:\"Rainforest\"  # 5 ecosystems (rainforests) with 2x vulnerability")
    click.echo()
    
    click.echo("🔍 AVAILABLE MODELS:")
    click.echo("Use 'compass models' to see all available ethical models")
    click.echo()
    
    click.echo("👓 AVAILABLE LENSES:")
    click.echo("Use 'compass lenses' to see all available lenses")
    click.echo()
    
    click.echo("📝 EXAMPLE SCENARIOS:")
    click.echo()
    click.echo("Structured format:")
    click.echo("1. Deforestation project:")
    click.echo("   compass evaluate HUMAN:10 ANIMAL:100 PLANT:1000 ECOSYSTEM:1 --model eco_systemic --lens fragility")
    click.echo()
    click.echo("2. AI development:")
    click.echo("   compass evaluate HUMAN:1000 FUTURE_BEING:10000 --model intergenerational --lens deep_time")
    click.echo()
    click.echo("Natural language format:")
    click.echo("3. Urban planning:")
    click.echo('   compass analyze "building 500 housing units that may affect 200 local animals and 5000 plants"')
    click.echo()
    click.echo("4. Technology deployment:")
    click.echo('   compass analyze "deploying AI system impacting 1000 users and future generations with cultural implications"')
    click.echo()
    
    click.echo("💡 TIPS:")
    click.echo("• Use --json flag for machine-readable output")
    click.echo("• Combine multiple lenses for nuanced analysis")
    click.echo("• Start with human_centric model for basic analysis")
    click.echo("• Use eco_systemic or deep_time for environmental decisions")
    click.echo("• Check for red flags early in the decision process")


if __name__ == "__main__":
    cli()