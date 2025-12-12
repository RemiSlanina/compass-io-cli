#!/usr/bin/env python3
"""
Compass-io CLI - API Server

This provides a REST API for the ethical analysis functionality,
allowing integration with web interfaces and other applications.
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from compass_io_cli.natural_language import ethical_analysis_from_text, ParsingMethod
from compass_io_cli.models import get_available_models
from compass_io_cli.lenses import get_available_lenses

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'name': 'Compass-io CLI API',
        'version': '0.1.0',
        'description': 'Ethical decision-making API',
        'endpoints': {
            '/analyze': 'POST - Analyze ethical scenario',
            '/models': 'GET - List available ethical models',
            '/lenses': 'GET - List available lenses',
            '/health': 'GET - Health check'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/models', methods=['GET'])
def list_models():
    """List available ethical models"""
    models = []
    for model_name in get_available_models():
        try:
            from compass_io_cli.models import create_model
            model = create_model(model_name)
            models.append({
                'name': model_name,
                'display_name': model.name,
                'description': model.description,
                'type': model.model_type.name
            })
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
    
    return jsonify({'models': models, 'count': len(models)})

@app.route('/lenses', methods=['GET'])
def list_lenses():
    """List available lenses"""
    lenses = []
    for lens_name in get_available_lenses():
        try:
            from compass_io_cli.lenses import create_lens
            lens = create_lens(lens_name)
            lenses.append({
                'name': lens_name,
                'display_name': lens.name,
                'description': lens.description,
                'type': lens.lens_type.name
            })
        except Exception as e:
            print(f"Error loading lens {lens_name}: {e}")
    
    return jsonify({'lenses': lenses, 'count': len(lenses)})

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze an ethical scenario from natural language"""
    
    # Validate input
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    scenario = data.get('scenario', '')
    
    if not scenario:
        return jsonify({'error': 'No scenario provided'}), 400
    
    # Get optional parameters
    method = data.get('method', 'simple')
    
    # Map method to ParsingMethod
    method_map = {
        'simple': ParsingMethod.SIMPLE_KEYWORD,
        'interactive': ParsingMethod.INTERACTIVE,
        'llm': ParsingMethod.LLM_ASSISTED
    }
    
    parsing_method = method_map.get(method, ParsingMethod.SIMPLE_KEYWORD)
    
    try:
        # Perform ethical analysis
        result = ethical_analysis_from_text(scenario, parsing_method)
        
        # Add API metadata
        result['api'] = {
            'version': '0.1.0',
            'method': method,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to analyze scenario',
            'scenario': scenario,
            'method': method
        }), 500

@app.route('/analyze/structured', methods=['POST'])
def analyze_structured():
    """Analyze using structured input (entities, model, lenses)"""
    
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    
    # Validate required fields
    if 'entities' not in data:
        return jsonify({'error': 'Entities are required'}), 400
    
    try:
        from compass_io_cli.models import Entity, EntityType
        from compass_io_cli.functions import ethical_functions
        
        # Parse entities
        entities = []
        for entity_data in data['entities']:
            entity = Entity(
                entity_type=EntityType[entity_data['type']],
                count=entity_data.get('count', 1),
                description=entity_data.get('description', ''),
                vulnerability=entity_data.get('vulnerability', 1.0)
            )
            entities.append(entity)
        
        # Get model and lenses
        model = data.get('model', 'human_centric')
        lenses = data.get('lenses', [])
        context = data.get('context', '')
        
        # Perform analysis
        result = ethical_functions.minimize_suffering(
            entities=entities,
            model_name=model,
            lens_names=lenses,
            context=context
        )
        
        # Convert to dict for JSON serialization
        analysis_result = {
            'suffering_score': result.suffering_score,
            'impact_level': result.impact_level.name,
            'red_flags': result.red_flags,
            'suggestions': result.suggestions,
            'explanation': result.explanation,
            'entities': [{
                'type': e.entity_type.name,
                'count': e.count,
                'description': e.description,
                'vulnerability': e.vulnerability
            } for e in result.affected_entities],
            'model': model,
            'lenses': lenses,
            'context': context
        }
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to analyze structured scenario'
        }), 500

@app.route('/compare', methods=['POST'])
def compare_models():
    """Compare ethical impact across multiple models"""
    
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    
    if 'entities' not in data or 'models' not in data:
        return jsonify({'error': 'Entities and models are required'}), 400
    
    try:
        from compass_io_cli.models import Entity, EntityType
        from compass_io_cli.functions import ethical_functions
        
        # Parse entities
        entities = []
        for entity_data in data['entities']:
            entity = Entity(
                entity_type=EntityType[entity_data['type']],
                count=entity_data.get('count', 1),
                description=entity_data.get('description', ''),
                vulnerability=entity_data.get('vulnerability', 1.0)
            )
            entities.append(entity)
        
        # Get models and optional parameters
        models = data['models']
        lenses = data.get('lenses', [])
        context = data.get('context', '')
        
        # Perform comparison
        comparisons = ethical_functions.compare_ethical_models(
            entities=entities,
            model_names=models,
            lens_names=lenses,
            context=context
        )
        
        # Convert to dict
        comparison_result = {
            'comparisons': [{
                'model_name': comp.model_name,
                'suffering_score': comp.suffering_score,
                'impact_level': comp.impact_level.name,
                'key_differences': comp.key_differences
            } for comp in comparisons],
            'entity_count': len(entities),
            'models_compared': len(models),
            'lenses_used': lenses,
            'context': context
        }
        
        return jsonify(comparison_result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to compare models'
        }), 500

@app.route('/redflags', methods=['POST'])
def check_redflags():
    """Check for ethical red flags in a scenario"""
    
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.json
    context = data.get('context', '')
    
    if not context:
        return jsonify({'error': 'Context is required'}), 400
    
    try:
        from compass_io_cli.functions import ethical_functions
        
        red_flags = ethical_functions.red_flag_check(context)
        
        return jsonify({
            'context': context,
            'red_flags': red_flags,
            'critical': len(red_flags) > 0,
            'count': len(red_flags)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Failed to check red flags'
        }), 500

if __name__ == '__main__':
    # Add datetime import for timestamp
    from datetime import datetime
    
    print("🚀 Starting Compass-io CLI API server...")
    print("📊 API will be available at http://localhost:5000")
    print("📖 Documentation: http://localhost:5000")
    print("✨ Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)