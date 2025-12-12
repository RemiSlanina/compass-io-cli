# Compass-io CLI - Usage Guide

Welcome to Compass-io CLI! This guide will help you get started with the ethical reasoning framework.

## 🚀 Quick Start

### Installation

First, make sure you have Python 3.8+ installed. Then install the required dependencies:

```bash
pip install click typing-extensions
```

### Basic Usage

The CLI provides several commands for ethical analysis:

```bash
# Show help
python -m compass_io_cli.main --help

# List available models
python -m compass_io_cli.main models

# List available lenses
python -m compass_io_cli.main lenses

# Show detailed help with examples
python -m compass_io_cli.main help
```

## 📖 Core Commands

### 1. Evaluate Ethical Impact

```bash
compass evaluate ENTITIES [OPTIONS]
```

Evaluate the ethical impact of a decision using a specific model and optional lenses.

**Example:**
```bash
compass evaluate HUMAN:10 ANIMAL:5 --model human_centric
```

**Options:**
- `--model, -m`: Ethical model to use (default: human_centric)
- `--lens, -l`: Lenses to apply (can specify multiple)
- `--context, -c`: Additional context about the decision
- `--json, -j`: Output results in JSON format

### 2. Consult Stakeholders

```bash
compass consult ENTITIES [OPTIONS]
```

Evaluate how different stakeholders might experience the outcome.

**Example:**
```bash
compass consult HUMAN:100 ECOSYSTEM:2 --model eco_systemic --lens fragility
```

### 3. Compare Ethical Models

```bash
compass compare ENTITIES [OPTIONS]
```

Compare outcomes across multiple ethical models.

**Example:**
```bash
compass compare HUMAN:50 ANIMAL:20 --models human_centric --models bio_inclusive
```

**Options:**
- `--models, -m`: Ethical models to compare (can specify multiple, default: all)
- `--lens, -l`: Lenses to apply to all models
- `--context, -c`: Additional context
- `--json, -j`: Output in JSON format

### 4. Check for Red Flags

```bash
compass redflags CONTEXT
```

Detect critical ethical violations in a decision.

**Example:**
```bash
compass redflags "deployment of autonomous weapons"
```

## 🎯 Entity Format

Entities are specified using the format:

```
TYPE[:COUNT[:VULNERABILITY[:DESCRIPTION]]]
```

**Available Entity Types:**
- `HUMAN` - Human beings
- `ANIMAL` - Animals (sentient beings)
- `PLANT` - Plant life
- `MICROBE` - Microorganisms
- `ECOSYSTEM` - Ecosystems and environmental systems
- `INANIMATE_OBJECT` - Non-living objects
- `FUTURE_BEING` - Future generations
- `SYMBOLIC_ENTITY` - Symbolic or cultural entities

**Examples:**
```bash
# Simple entity
HUMAN:10

# Entity with vulnerability
ANIMAL:5:1.5

# Entity with description
ECOSYSTEM:1:2.0:"Amazon Rainforest"

# Multiple entities
HUMAN:10 ANIMAL:5 PLANT:100
```

## 🔍 Available Ethical Models

| Model | Description | Best For |
|-------|-------------|----------|
| `human_centric` | Only humans matter | Human rights, policy drafts |
| `sentience_based` | All sentient beings | Animal ethics, welfare |
| `bio_inclusive` | All life forms | Ecosystem planning, biocentrism |
| `eco_systemic` | Includes ecosystems | Environmental policy, climate |
| `animist` | All entities have weight | Cultural respect, indigenous knowledge |
| `intergenerational` | Focus on future beings | Sustainability, long-term planning |
| `object_respect` | Symbolic/object consideration | Care ethics, symbolic systems |
| `deep_time` | Extreme long-term perspective | Climate policy, existential risk |

## 👓 Available Lenses

| Lens | Description | Effect |
|------|-------------|--------|
| `sparks` | Values all kinds of lives | Reduces human bias, increases consideration for overlooked entities |
| `fragility` | Focuses on vulnerability | Emphasizes fragile ecosystems and irreversible impacts |
| `deep_time` | Long-term perspective | Massively increases weight for future impacts |
| `cultural` | Custom cultural perspective | Can be customized for specific cultural views |

## 📝 Practical Examples

### Example 1: Urban Development Project

```bash
compass evaluate HUMAN:50 ANIMAL:20 PLANT:500 ECOSYSTEM:1 --model bio_inclusive --lens fragility
```

Evaluates an urban development project that affects:
- 50 humans (workers/residents)
- 20 animals (local wildlife)
- 500 plants (local flora)
- 1 ecosystem (local park)

### Example 2: AI Development Ethics

```bash
compass evaluate HUMAN:1000 FUTURE_BEING:10000 --model intergenerational --lens deep_time --context "AI alignment research"
```

Evaluates AI development with long-term intergenerational impacts.

### Example 3: Environmental Policy

```bash
compass evaluate ECOSYSTEM:5 ANIMAL:500 PLANT:10000 --model eco_systemic --lens fragility --context "Climate change mitigation policy"
```

Evaluates environmental policy impacts on ecosystems.

### Example 4: Model Comparison

```bash
compass compare HUMAN:100 ANIMAL:50 --models human_centric --models sentience_based --models animist
```

Compares how different ethical models evaluate the same scenario.

## 💡 Tips for Effective Use

1. **Start simple**: Begin with `human_centric` model for basic analysis
2. **Add lenses**: Use lenses like `fragility` or `sparks` for nuanced perspectives
3. **Compare models**: Use `compare` to see how different ethical frameworks view your decision
4. **Check red flags early**: Run `redflags` command early in your decision process
5. **Use JSON output**: For programmatic use, add `--json` flag for machine-readable output
6. **Consider vulnerability**: Use vulnerability scores (>1.0) for at-risk populations
7. **Think long-term**: For major decisions, use `intergenerational` or `deep_time` models

## 🔧 Advanced Usage

### JSON Output

All commands support JSON output for integration with other tools:

```bash
compass evaluate HUMAN:10 ANIMAL:5 --model human_centric --json
```

### Multiple Lenses

Apply multiple lenses to get comprehensive analysis:

```bash
compass evaluate HUMAN:10 ECOSYSTEM:1 --model bio_inclusive --lens sparks --lens fragility
```

### Context Matters

Provide context for better red flag detection:

```bash
compass evaluate HUMAN:1000 --model human_centric --context "mass surveillance system deployment" --lens fragility
```

## 🎓 Understanding the Results

### Suffering Score

- **0**: No suffering detected
- **< 1.0**: Low impact
- **1.0 - 5.0**: Medium impact
- **5.0 - 10.0**: High impact
- **> 10.0**: Critical impact

### Impact Levels

- **NONE**: No significant ethical concerns
- **LOW**: Minimal concerns, proceed with caution
- **MEDIUM**: Moderate concerns, consider mitigation
- **HIGH**: Significant concerns, seek alternatives
- **CRITICAL**: Severe concerns, immediate action required

### Red Flags

When red flags are detected, the decision should be:
1. **Halted immediately** for critical review
2. **Completely redesigned** to eliminate the ethical violation
3. **Subject to oversight** by ethical review boards

## 🤖 Integration with Other Tools

The JSON output format makes it easy to integrate Compass-io with other tools:

```bash
# Pipe JSON output to jq for processing
compass evaluate HUMAN:10 --json | jq '.suffering_score'

# Use in scripts
result=$(compass evaluate HUMAN:5 --json)
echo "Suffering score: $(echo $result | jq '.suffering_score')"

# Integrate with decision-making pipelines
compass evaluate $ENTITIES --model $MODEL --json > ethical_analysis.json
```

## 📚 Learning Resources

To deepen your understanding of the ethical models:

```bash
# Read about all available models
compass models

# Read about all available lenses  
compass lenses

# Get detailed help with examples
compass help
```

## 🎯 Best Practices

1. **Start with multiple models**: Compare different ethical perspectives
2. **Use lenses appropriately**: Choose lenses that match your context
3. **Document your reasoning**: Keep records of ethical evaluations
4. **Iterate on decisions**: Use the tool throughout the decision process
5. **Combine with human judgment**: The tool assists, but doesn't replace, ethical reasoning
6. **Be transparent**: Share your ethical analysis with stakeholders

## 🚨 Ethical Considerations

Remember that Compass-io is a tool to assist ethical reasoning, not replace it. Always:

- Consider the limitations of quantitative ethical analysis
- Involve diverse stakeholders in decision-making
- Be transparent about your ethical framework choices
- Prioritize the reduction of actual suffering over theoretical scores
- Use the tool to expand your circle of moral consideration

The tool should never be used to justify actions that violate the dignity of conscious beings.

## 🐛 Troubleshooting

**Issue: Command not found**
- Make sure you're running from the correct directory
- Use `python -m compass_io_cli.main` instead of just `compass`
- Check your Python path settings

**Issue: Invalid entity format**
- Check that your entity types are valid (use uppercase)
- Verify the format: `TYPE[:COUNT[:VULNERABILITY[:DESCRIPTION]]]`
- Use quotes around descriptions with spaces

**Issue: Model/lens not found**
- Check available models with `compass models`
- Check available lenses with `compass lenses`
- Verify spelling (use underscores, not spaces)

## 📞 Support

For help and support:

1. Check the detailed help: `compass help`
2. Review the examples in this guide
3. Consult the ethical models documentation
4. Reach out to the Compass-io community

Happy ethical reasoning! 🧭✨