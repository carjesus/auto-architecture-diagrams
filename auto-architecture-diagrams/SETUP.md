# 🚀 Setup Guide

Complete setup guide for Auto Architecture Diagrams in your repository.

## 📋 Prerequisites

- Python 3.7 or higher
- Git repository
- GitHub repository (for automatic workflows)

## 🔧 Installation

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
1. Download Graphviz from: https://graphviz.org/download/
2. Install and add to PATH

### 2. Install Python Dependencies

```bash
pip install diagrams
```

Or add to your `requirements.txt`:
```
diagrams>=0.23.0
```

## 📁 Project Setup

### Option A: Copy Files Manually

1. **Create directory structure:**
```bash
mkdir -p .github/workflows
mkdir -p docs/diagrams
```

2. **Copy workflow files:**
```bash
cp auto-architecture-diagrams/workflows/* .github/workflows/
```

3. **Copy script files:**
```bash
cp auto-architecture-diagrams/scripts/* docs/diagrams/
```

### Option B: Use Setup Script

Create `setup_diagrams.sh`:
```bash
#!/bin/bash
echo "🚀 Setting up Auto Architecture Diagrams..."

# Create directories
mkdir -p .github/workflows
mkdir -p docs/diagrams

# Copy files (adjust paths as needed)
cp auto-architecture-diagrams/workflows/* .github/workflows/
cp auto-architecture-diagrams/scripts/* docs/diagrams/

# Make scripts executable
chmod +x docs/diagrams/*.py

echo "✅ Setup complete!"
echo "📝 Next steps:"
echo "   1. Configure GitHub Actions permissions"
echo "   2. Commit and push files"
echo "   3. Check Actions tab for first run"
```

Run it:
```bash
chmod +x setup_diagrams.sh
./setup_diagrams.sh
```

## ⚙️ GitHub Actions Configuration

### 1. Enable Workflow Permissions

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Actions** → **General**
3. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

### 2. Verify Workflow Files

Ensure these files exist in your repository:
```
.github/
└── workflows/
    ├── generate-diagram.yml          # Manual workflow
    └── generate-diagram-auto.yml     # Automatic workflow
```

## 🎯 Customization for Your Project

### 1. Adjust File Paths

If your project structure is different, update paths in workflows:

**In `.github/workflows/generate-diagram-auto.yml`:**
```yaml
# Change these paths to match your structure
paths:
  - 'src/**/*.py'          # Your source code location
  - 'app/**/*.py'          # Alternative location
  - 'your-app/**/*.py'     # Custom location
```

**In `docs/diagrams/analyze_repo.py`:**
```python
# Update source paths for your project
self.source_paths = [
    self.repo_root / "src",           # Default
    self.repo_root / "your-app",      # Your custom path
    self.repo_root / "backend",       # Alternative
]
```

### 2. Customize Diagram Output

**Change output location** in `generate_architecture.py`:
```python
# Change filename and location
filename="your_custom_diagram_name",
```

**Change diagram title:**
```python
title = f"Your Company - {framework} Architecture"
```

### 3. Add Custom Technology Detection

**In `analyze_repo.py`**, add patterns for your specific technologies:

```python
# Add your database
db_patterns = {
    "PostgreSQL": [r"psycopg2", r"asyncpg"],
    "YourCustomDB": [r"your_db_pattern"],  # Add this
}

# Add your cloud services
aws_patterns = {
    "S3": [r"boto3.*s3"],
    "YourService": [r"your_service_pattern"],  # Add this
}

# Add your framework
if "your_framework" in content.lower():
    self.components["framework"] = "YourFramework"
```

## 🧪 Testing Setup

### 1. Test Locally

```bash
cd docs/diagrams

# Test analysis
python analyze_repo.py

# Test AI refinement
python ai_refiner.py

# Test generation
python generate_architecture.py

# Test diagram creation
python architecture.py

# Verify everything works
python test_diagram.py
```

### 2. Test GitHub Actions

1. **Commit and push your changes:**
```bash
git add .github/workflows/ docs/diagrams/
git commit -m "feat: add auto architecture diagrams"
git push
```

2. **Check Actions tab:**
   - Go to your repository → **Actions**
   - Look for "Auto-Generate Architecture Diagram" workflow
   - It should run automatically

3. **Manual test:**
   - Go to **Actions** → **Auto-Generate Architecture Diagram**
   - Click **Run workflow** → **Run workflow**

## 🔍 Verification

After setup, you should see:

### Files Created
```
docs/diagrams/
├── analyze_repo.py
├── ai_refiner.py
├── generate_architecture.py
├── test_diagram.py
├── architecture.py              # Generated automatically
├── analysis_result.json         # Generated automatically
├── ai_refinement_report.json    # Generated automatically
└── architecture_diagram.png     # Generated automatically
```

### GitHub Actions
- ✅ Workflow runs without errors
- ✅ Diagram PNG is generated and committed
- ✅ Analysis JSON files are created

## 🚨 Troubleshooting

### Common Setup Issues

**1. Workflow doesn't run**
- Check file paths in workflow YAML
- Verify GitHub Actions permissions
- Ensure files are in `main`/`master` branch

**2. Permission denied errors**
- Enable "Read and write permissions" in repository settings
- Check that `GITHUB_TOKEN` has necessary permissions

**3. Graphviz not found**
- Install Graphviz system package
- Verify with `dot -V` command

**4. Python import errors**
- Install `diagrams` package: `pip install diagrams`
- Check Python version (3.7+ required)

**5. No diagram generated**
- Check if `architecture.py` was created
- Look for errors in GitHub Actions logs
- Test locally first

### Getting Help

1. **Check GitHub Actions logs:**
   - Go to Actions tab → Failed workflow → Click on job → Expand steps

2. **Test locally:**
   - Run each script individually
   - Check error messages

3. **Verify file structure:**
   - Ensure all files are in correct locations
   - Check file permissions

## 🎉 Success!

If everything is working:
- ✅ Workflows run automatically on code changes
- ✅ Diagrams are generated and committed
- ✅ Architecture stays up-to-date with your code

Your architecture diagrams will now update automatically every time you push code changes! 🚀