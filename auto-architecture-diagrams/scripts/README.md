# Scripts Documentation

This directory contains the core scripts for automatic architecture diagram generation.

## 📁 Files Overview

### Core Scripts

- **`analyze_repo.py`** - Repository analyzer that detects components and technologies
- **`ai_refiner.py`** - AI-powered refinement engine for improving diagrams
- **`generate_architecture.py`** - Automatic generator for architecture.py code
- **`test_diagram.py`** - Test script to verify diagram generation

### Generated Files

- **`architecture.py`** - Auto-generated diagram code (DO NOT edit manually)
- **`analysis_result.json`** - Repository analysis results
- **`ai_refinement_report.json`** - AI refinement report with relationships
- **`*.png`** - Generated diagram images

## 🔄 Execution Flow

```
1. analyze_repo.py     → Scans repository structure
2. ai_refiner.py       → Analyzes relationships (optional)
3. generate_architecture.py → Creates architecture.py
4. architecture.py     → Generates PNG diagram
5. test_diagram.py     → Validates generation (optional)
```

## 🛠️ Manual Usage

### Full Process
```bash
# 1. Analyze repository
python analyze_repo.py

# 2. AI refinement (optional)
python ai_refiner.py

# 3. Generate architecture code
python generate_architecture.py

# 4. Create diagram
python architecture.py

# 5. Test (optional)
python test_diagram.py
```

### Quick Generation
```bash
# Generate without AI refinement
python generate_architecture.py --no-ai
python architecture.py
```

## 📊 Output Files

### analysis_result.json
Contains detected components:
```json
{
  "components": {
    "databases": ["PostgreSQL", "MongoDB"],
    "services_aws": ["S3", "RDS"],
    "controllers": ["user_controller", "auth_controller"],
    "services": ["user_service", "auth_service"],
    "models": ["user_model", "auth_model"]
  },
  "summary": {
    "framework": "FastAPI",
    "controllers_count": 15,
    "services_count": 20
  }
}
```

### ai_refinement_report.json
Contains relationship analysis:
```json
{
  "relationships": {
    "service_to_service": {
      "user_service": ["auth_service", "notification_service"]
    },
    "controller_to_service": {
      "user_controller": ["user_service"]
    }
  },
  "suggestions": [
    {
      "type": "service_connection",
      "from": "user_service",
      "to": ["auth_service"],
      "priority": "high"
    }
  ]
}
```

## 🎯 Customization

### Adding New Technology Detection

Edit `analyze_repo.py`:

```python
# Add new database pattern
db_patterns = {
    "PostgreSQL": [r"psycopg2", r"asyncpg"],
    "YourDB": [r"yourdb", r"your_db_client"],  # Add this
}

# Add new cloud service
aws_patterns = {
    "S3": [r"boto3.*s3", r"s3_client"],
    "YourService": [r"your_service_pattern"],  # Add this
}
```

### Customizing Diagram Layout

Edit `generate_architecture.py`:

```python
def _generate_diagram_config(self) -> str:
    return '''graph_attr = {
        "fontsize": "20",        # Larger font
        "bgcolor": "lightblue",  # Different background
        "direction": "LR",       # Left-to-right layout
        # ... other attributes
    }'''
```

### Adding New Relationship Types

Edit `ai_refiner.py`:

```python
relationships = {
    "service_to_service": defaultdict(set),
    "your_new_relation": defaultdict(set),  # Add this
}

# Add detection logic
def _analyze_your_relation(self, file_path, relationships):
    # Your detection logic here
    pass
```

## 🔍 Troubleshooting

### Common Issues

**1. "analysis_result.json not found"**
```bash
# Solution: Run analyzer first
python analyze_repo.py
```

**2. "No PNG generated"**
```bash
# Check if Graphviz is installed
dot -V

# Install if missing (Ubuntu/Debian)
sudo apt-get install graphviz

# Install if missing (macOS)
brew install graphviz
```

**3. "Import errors"**
```bash
# Install required packages
pip install diagrams
```

**4. "AI refinement failed"**
```bash
# Run without AI refinement
python generate_architecture.py --no-ai
```

### Debug Mode

Add debug prints to any script:

```python
import json

# Debug analysis results
with open("analysis_result.json") as f:
    data = json.load(f)
    print("DEBUG:", json.dumps(data, indent=2))
```

## 📈 Performance Tips

1. **Large repositories**: The analyzer might be slow on very large codebases
2. **Skip AI refinement**: Use `--no-ai` flag for faster generation
3. **Selective analysis**: Modify source paths in analyzer to focus on specific directories

## 🤝 Contributing

When adding new features:

1. Update detection patterns in `analyze_repo.py`
2. Add relationship analysis in `ai_refiner.py` 
3. Update diagram generation in `generate_architecture.py`
4. Test with `test_diagram.py`
5. Update this documentation