# 🤝 Contributing to Auto Architecture Diagrams

Thank you for your interest in contributing! This project aims to make architecture documentation automatic and accessible for all developers.

## 🎯 How to Contribute

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include steps to reproduce
- Provide sample repository structure if possible
- Include error messages and logs

### 💡 Feature Requests
- Open an issue with the "enhancement" label
- Describe the use case and expected behavior
- Consider if it fits the project's scope

### 🔧 Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and create a Pull Request

## 🏗️ Development Setup

### Prerequisites
- Python 3.7+
- Graphviz installed
- Git

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/auto-architecture-diagrams.git
cd auto-architecture-diagrams

# Install dependencies
pip install diagrams

# Test the scripts
cd scripts
python analyze_repo.py
python generate_architecture.py
python architecture.py
```

## 📝 Code Style

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Include type hints where appropriate

### Example:
```python
def analyze_service_file(self, file_path: Path, service_name: str, relationships: Dict) -> None:
    """
    Analyzes a service file to detect dependencies.
    
    Args:
        file_path: Path to the service file
        service_name: Name of the service
        relationships: Dictionary to store found relationships
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        # ... implementation
    except Exception as e:
        print(f"⚠️ Error analyzing {file_path}: {e}")
```

### Documentation
- Update README.md for new features
- Add examples for new functionality
- Keep documentation clear and concise

## 🧪 Testing

### Before Submitting
1. **Test with different project structures:**
   - FastAPI projects
   - Django projects
   - Flask projects
   - Node.js projects (if applicable)

2. **Test the workflows:**
   - Manual workflow (`generate-diagram.yml`)
   - Automatic workflow (`generate-diagram-auto.yml`)

3. **Verify generated diagrams:**
   - Check that PNG files are created
   - Ensure diagrams are readable and accurate

### Test Cases to Consider
```bash
# Test with minimal project
mkdir test-minimal && cd test-minimal
git init
echo "print('hello')" > app.py
# Run analyzer and verify it doesn't crash

# Test with complex project
# Clone a real FastAPI/Django project
# Run full analysis pipeline
```

## 🎨 Adding New Technology Support

### 1. Update Repository Analyzer

In `scripts/analyze_repo.py`, add detection patterns:

```python
# Add new framework detection
if "your_framework" in content.lower():
    self.components["framework"] = "YourFramework"

# Add new database detection
db_patterns = {
    "PostgreSQL": [r"psycopg2", r"asyncpg"],
    "YourDB": [r"your_db_pattern", r"YourDB"],  # Add this
}

# Add new cloud service detection
aws_patterns = {
    "S3": [r"boto3.*s3", r"s3_client"],
    "YourService": [r"your_service_pattern"],  # Add this
}
```

### 2. Update Diagram Generator

In `scripts/generate_architecture.py`, add diagram components:

```python
# Add import for new service
if "YourService" in self.summary["aws_services"]:
    imports.append("from diagrams.aws.yourservice import YourService")

# Add component to diagram
if "YourService" in self.summary.get("aws_services", []):
    code += '        your_service = YourService("Your Service\\nDescription")\n'
```

### 3. Update AI Refiner

In `scripts/ai_refiner.py`, add relationship detection:

```python
# Add new relationship patterns
your_service_patterns = {
    "YourService": [r"your_service", r"YourServiceClient"],
}

for service_name, patterns in your_service_patterns.items():
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            relationships["service_to_your_service"][service_name].add(service_name)
            break
```

## 📋 Pull Request Guidelines

### PR Title Format
- `feat: add support for Django framework`
- `fix: resolve PostgreSQL detection issue`
- `docs: update setup guide`
- `refactor: improve service detection logic`

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Tested with sample projects
- [ ] Workflows run successfully
- [ ] Generated diagrams are accurate

## Screenshots (if applicable)
Include before/after diagram images

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
```

## 🌟 Areas for Contribution

### High Priority
- **More framework support**: Django, Flask, Express.js, Spring Boot
- **Better cloud detection**: GCP, Azure services
- **Improved relationship analysis**: More accurate service dependencies
- **Docker/Kubernetes support**: Container orchestration detection

### Medium Priority
- **Custom styling options**: Different diagram themes
- **Multiple output formats**: SVG, PDF support
- **Performance optimization**: Faster analysis for large repositories
- **Configuration files**: Allow customization via config files

### Low Priority
- **Interactive diagrams**: Clickable components
- **Diagram versioning**: Track changes over time
- **Integration with other tools**: Confluence, Notion export

## 🏆 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Given credit in documentation

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Issues**: Use GitHub Issues
- **Ideas**: Start a Discussion in the Ideas category

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make architecture documentation automatic for everyone!** 🚀