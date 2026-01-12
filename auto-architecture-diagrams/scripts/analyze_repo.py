#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic Repository Analyzer for Auto Architecture Diagrams
Analyzes any repository structure and detects architectural components
"""
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

class RepositoryAnalyzer:
    def __init__(self, repo_root: str = None):
        if repo_root is None:
            # Try to find repository root from current location
            current = Path(__file__).parent
            while current.parent != current:
                if (current / '.git').exists():
                    self.repo_root = current
                    break
                current = current.parent
            else:
                # Fallback: assume we're in docs/diagrams
                self.repo_root = Path(__file__).parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        print(f"🔍 Analyzing repository: {self.repo_root}")
        
        # Common source directories to analyze
        self.source_paths = [
            self.repo_root / "src",
            self.repo_root / "app", 
            self.repo_root / "api",
            self.repo_root / "backend",
            self.repo_root / "server",
            self.repo_root,  # Root level files
        ]
        
        self.components = {
            "databases": set(),
            "services_aws": set(),
            "services_gcp": set(),
            "services_azure": set(),
            "controllers": [],
            "services": [],
            "graphql_resolvers": [],
            "models": [],
            "cron_jobs": [],
            "storage": set(),
            "message_queues": set(),
            "cache": set(),
        }
    
    def analyze(self) -> Dict:
        """Analyzes the complete repository"""
        print("🔍 Starting repository analysis...")
        
        # Analyze databases
        self._analyze_databases()
        
        # Analyze cloud services
        self._analyze_cloud_services()
        
        # Analyze application structure
        self._analyze_application_structure()
        
        # Analyze configuration files
        self._analyze_config_files()
        
        # Analyze Docker and deployment
        self._analyze_deployment()
        
        print("✅ Analysis completed")
        return self.components
    
    def _analyze_databases(self):
        """Detects databases used in the project"""
        db_patterns = {
            "PostgreSQL": [
                r"psycopg2", r"asyncpg", r"postgresql://", 
                r"postgres://", r"PostgreSQL", r"POSTGRES"
            ],
            "MySQL": [
                r"mysql", r"pymysql", r"mysql://", r"MySQL", r"MYSQL"
            ],
            "MongoDB": [
                r"pymongo", r"MongoClient", r"mongodb://", 
                r"MongoDB", r"mongo"
            ],
            "SQLite": [
                r"sqlite3", r"sqlite://", r"\.db$", r"\.sqlite$"
            ],
            "Redis": [
                r"redis", r"Redis", r"redis://", r"REDIS"
            ],
            "DynamoDB": [
                r"dynamodb", r"DynamoDB", r"boto3.*dynamodb"
            ],
        }
        
        for db_name, patterns in db_patterns.items():
            for pattern in patterns:
                if self._search_in_files(pattern):
                    self.components["databases"].add(db_name)
                    break
    
    def _analyze_cloud_services(self):
        """Detects cloud services used"""
        # AWS Services
        aws_patterns = {
            "S3": [r"boto3.*s3", r"s3_client", r"S3", r"\.s3\.", r"aws.*s3"],
            "Lambda": [r"lambda", r"Lambda", r"aws.*lambda"],
            "SNS": [r"sns", r"SNS", r"aws.*sns"],
            "SQS": [r"sqs", r"SQS", r"aws.*sqs"],
            "RDS": [r"rds", r"RDS", r"aws.*rds"],
            "DynamoDB": [r"dynamodb", r"DynamoDB", r"aws.*dynamodb"],
            "CloudWatch": [r"cloudwatch", r"CloudWatch"],
            "API Gateway": [r"apigateway", r"API.*Gateway"],
        }
        
        for service_name, patterns in aws_patterns.items():
            for pattern in patterns:
                if self._search_in_files(pattern):
                    self.components["services_aws"].add(service_name)
                    break
        
        # GCP Services
        gcp_patterns = {
            "Cloud Storage": [r"google.*storage", r"gcs", r"Cloud.*Storage"],
            "BigQuery": [r"bigquery", r"BigQuery"],
            "Pub/Sub": [r"pubsub", r"Pub.*Sub"],
            "Cloud Functions": [r"cloud.*functions", r"gcp.*functions"],
        }
        
        for service_name, patterns in gcp_patterns.items():
            for pattern in patterns:
                if self._search_in_files(pattern):
                    self.components["services_gcp"].add(service_name)
                    break
        
        # Azure Services
        azure_patterns = {
            "Blob Storage": [r"azure.*blob", r"BlobService"],
            "Service Bus": [r"azure.*servicebus", r"ServiceBus"],
            "Functions": [r"azure.*functions", r"AzureFunctions"],
        }
        
        for service_name, patterns in azure_patterns.items():
            for pattern in patterns:
                if self._search_in_files(pattern):
                    self.components["services_azure"].add(service_name)
                    break
    
    def _analyze_application_structure(self):
        """Analyzes application structure"""
        for source_path in self.source_paths:
            if not source_path.exists():
                continue
                
            # Controllers/Routes
            controller_patterns = [
                "**/controllers/*.py", "**/controller/*.py",
                "**/routes/*.py", "**/route/*.py", 
                "**/views/*.py", "**/view/*.py",
                "**/handlers/*.py", "**/handler/*.py",
                "**/endpoints/*.py", "**/endpoint/*.py"
            ]
            
            controllers = []
            for pattern in controller_patterns:
                for file in source_path.glob(pattern):
                    if file.stem != "__init__":
                        controllers.append(file.stem)
            self.components["controllers"].extend(controllers)
            
            # Services
            service_patterns = [
                "**/services/*.py", "**/service/*.py",
                "**/*_service.py", "**/*Service.py"
            ]
            
            services = []
            for pattern in service_patterns:
                for file in source_path.glob(pattern):
                    if file.stem != "__init__" and "service" in file.stem.lower():
                        services.append(file.stem)
            self.components["services"].extend(services)
            
            # GraphQL Resolvers
            resolver_patterns = [
                "**/resolvers/*.py", "**/resolver/*.py",
                "**/graphql/**/*.py", "**/*_resolver.py"
            ]
            
            resolvers = []
            for pattern in resolver_patterns:
                for file in source_path.glob(pattern):
                    if file.stem != "__init__":
                        resolvers.append(file.stem)
            self.components["graphql_resolvers"].extend(resolvers)
            
            # Models
            model_patterns = [
                "**/models/*.py", "**/model/*.py",
                "**/*_model.py", "**/*Model.py"
            ]
            
            models = []
            for pattern in model_patterns:
                for file in source_path.glob(pattern):
                    if file.stem != "__init__":
                        models.append(file.stem)
            self.components["models"].extend(models)
            
            # Background Jobs/Cron
            job_patterns = [
                "**/jobs/*.py", "**/job/*.py",
                "**/tasks/*.py", "**/task/*.py",
                "**/cron/*.py", "**/workers/*.py",
                "**/*_job.py", "**/*_task.py"
            ]
            
            jobs = []
            for pattern in job_patterns:
                for file in source_path.glob(pattern):
                    if file.stem != "__init__":
                        jobs.append(file.stem)
            self.components["cron_jobs"].extend(jobs)
        
        # Remove duplicates and sort
        for key in ["controllers", "services", "graphql_resolvers", "models", "cron_jobs"]:
            self.components[key] = sorted(list(set(self.components[key])))
    
    def _analyze_config_files(self):
        """Analyzes configuration files to detect frameworks and tools"""
        # Python requirements
        req_files = [
            self.repo_root / "requirements.txt",
            self.repo_root / "pyproject.toml",
            self.repo_root / "Pipfile"
        ]
        
        for req_file in req_files:
            if req_file.exists():
                content = req_file.read_text().lower()
                
                # Web frameworks
                if any(fw in content for fw in ["fastapi", "fast-api"]):
                    self.components["framework"] = "FastAPI"
                elif "django" in content:
                    self.components["framework"] = "Django"
                elif "flask" in content:
                    self.components["framework"] = "Flask"
                elif "starlette" in content:
                    self.components["framework"] = "Starlette"
                
                # GraphQL
                if "strawberry" in content:
                    self.components["graphql"] = "Strawberry"
                elif "graphene" in content:
                    self.components["graphql"] = "Graphene"
                elif "ariadne" in content:
                    self.components["graphql"] = "Ariadne"
                
                # Servers
                if "uvicorn" in content:
                    self.components["server"] = "Uvicorn"
                elif "gunicorn" in content:
                    self.components["server"] = "Gunicorn"
                
                # Schedulers
                if "apscheduler" in content:
                    self.components["scheduler"] = "APScheduler"
                elif "celery" in content:
                    self.components["scheduler"] = "Celery"
                
                # ORM
                if "sqlalchemy" in content:
                    self.components["orm"] = "SQLAlchemy"
                elif "django" in content:
                    self.components["orm"] = "Django ORM"
                elif "peewee" in content:
                    self.components["orm"] = "Peewee"
        
        # Node.js package.json
        package_json = self.repo_root / "package.json"
        if package_json.exists():
            try:
                import json as json_lib
                content = json_lib.loads(package_json.read_text())
                dependencies = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
                
                # Node.js frameworks
                if "express" in dependencies:
                    self.components["framework"] = "Express.js"
                elif "fastify" in dependencies:
                    self.components["framework"] = "Fastify"
                elif "koa" in dependencies:
                    self.components["framework"] = "Koa.js"
                elif "next" in dependencies:
                    self.components["framework"] = "Next.js"
                elif "nuxt" in dependencies:
                    self.components["framework"] = "Nuxt.js"
                
            except:
                pass
    
    def _analyze_deployment(self):
        """Analyzes deployment configuration"""
        # Docker
        if (self.repo_root / "Dockerfile").exists():
            self.components["containerization"] = "Docker"
        
        if (self.repo_root / "docker-compose.yml").exists():
            self.components["orchestration"] = "Docker Compose"
        
        # Kubernetes
        k8s_files = list(self.repo_root.glob("**/*.yaml")) + list(self.repo_root.glob("**/*.yml"))
        for file in k8s_files:
            try:
                content = file.read_text()
                if "apiVersion:" in content and "kind:" in content:
                    self.components["orchestration"] = "Kubernetes"
                    break
            except:
                continue
    
    def _search_in_files(self, pattern: str) -> bool:
        """Searches for a pattern in all relevant files"""
        pattern_re = re.compile(pattern, re.IGNORECASE)
        
        # Search in Python files
        for source_path in self.source_paths:
            if not source_path.exists():
                continue
                
            for py_file in source_path.rglob("*.py"):
                try:
                    content = py_file.read_text(encoding='utf-8')
                    if pattern_re.search(content):
                        return True
                except:
                    continue
        
        # Search in config files
        config_files = [
            "requirements.txt", "pyproject.toml", "Pipfile",
            "package.json", "yarn.lock", "package-lock.json",
            "Dockerfile", "docker-compose.yml", ".env"
        ]
        
        for config_file in config_files:
            file_path = self.repo_root / config_file
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if pattern_re.search(content):
                        return True
                except:
                    continue
        
        return False
    
    def get_summary(self) -> Dict:
        """Returns analysis summary"""
        return {
            "databases": sorted(list(self.components["databases"])),
            "aws_services": sorted(list(self.components["services_aws"])),
            "gcp_services": sorted(list(self.components["services_gcp"])),
            "azure_services": sorted(list(self.components["services_azure"])),
            "controllers_count": len(self.components["controllers"]),
            "services_count": len(self.components["services"]),
            "graphql_resolvers_count": len(self.components["graphql_resolvers"]),
            "models_count": len(self.components["models"]),
            "cron_jobs_count": len(self.components["cron_jobs"]),
            "framework": self.components.get("framework", "Unknown"),
            "graphql": self.components.get("graphql"),
            "server": self.components.get("server", "Unknown"),
            "orm": self.components.get("orm"),
            "scheduler": self.components.get("scheduler"),
            "containerization": self.components.get("containerization"),
            "orchestration": self.components.get("orchestration"),
        }


if __name__ == "__main__":
    analyzer = RepositoryAnalyzer()
    components = analyzer.analyze()
    summary = analyzer.get_summary()
    
    # Save results to JSON
    output_file = Path(__file__).parent / "analysis_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "components": {k: list(v) if isinstance(v, set) else v for k, v in components.items()},
            "summary": summary
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Repository Analysis Summary:")
    print(f"  📁 Repository: {analyzer.repo_root}")
    print(f"  🗄️  Databases: {', '.join(summary['databases']) or 'None detected'}")
    print(f"  ☁️  AWS Services: {', '.join(summary['aws_services']) or 'None detected'}")
    if summary['gcp_services']:
        print(f"  🌐 GCP Services: {', '.join(summary['gcp_services'])}")
    if summary['azure_services']:
        print(f"  🔷 Azure Services: {', '.join(summary['azure_services'])}")
    print(f"  🎮 Controllers: {summary['controllers_count']}")
    print(f"  ⚙️  Services: {summary['services_count']}")
    print(f"  🔗 GraphQL Resolvers: {summary['graphql_resolvers_count']}")
    print(f"  📊 Models: {summary['models_count']}")
    print(f"  ⏰ Background Jobs: {summary['cron_jobs_count']}")
    print(f"  🚀 Framework: {summary['framework']}")
    if summary['graphql']:
        print(f"  📡 GraphQL: {summary['graphql']}")
    if summary['orm']:
        print(f"  🗃️  ORM: {summary['orm']}")
    if summary['scheduler']:
        print(f"  📅 Scheduler: {summary['scheduler']}")
    if summary['containerization']:
        print(f"  📦 Container: {summary['containerization']}")
    if summary['orchestration']:
        print(f"  🎼 Orchestration: {summary['orchestration']}")
    
    print(f"\n💾 Results saved to: {output_file}")