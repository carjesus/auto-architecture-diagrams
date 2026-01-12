#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Refiner for Architecture Diagrams
Analyzes relationships and improves diagram quality
Inspired by TerraVision: https://github.com/patrickchugh/terravision
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class AIRefiner:
    """
    Refines diagrams using intelligent analysis:
    - Detects missing relationships between components
    - Improves labels and titles
    - Adds logical connections
    - Applies diagramming best practices
    """
    
    def __init__(self, analysis_file: str = None, repo_root: str = None):
        if analysis_file is None:
            analysis_file = Path(__file__).parent / "analysis_result.json"
        else:
            analysis_file = Path(analysis_file)
        
        if repo_root is None:
            # Try to find repository root
            current = Path(__file__).parent
            while current.parent != current:
                if (current / '.git').exists():
                    self.repo_root = current
                    break
                current = current.parent
            else:
                self.repo_root = Path(__file__).parent.parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        # Common source directories
        self.source_paths = [
            self.repo_root / "src",
            self.repo_root / "app", 
            self.repo_root / "api",
            self.repo_root / "backend",
            self.repo_root / "server",
        ]
        
        # Verify analysis file exists
        if not analysis_file.exists():
            raise FileNotFoundError(
                f"Analysis file not found: {analysis_file}\n"
                f"Run first: python analyze_repo.py"
            )
        
        with open(analysis_file, "r", encoding="utf-8") as f:
            self.analysis = json.load(f)
        
        self.components = self.analysis.get("components", {})
        self.relationships = {}
        self.suggestions = []
    
    def analyze_relationships(self) -> Dict:
        """Analyzes relationships between services, controllers and models"""
        print("🔗 Analyzing component relationships...")
        
        relationships = {
            "service_to_service": defaultdict(set),
            "controller_to_service": defaultdict(set),
            "service_to_database": defaultdict(set),
            "service_to_storage": defaultdict(set),
            "resolver_to_service": defaultdict(set),
            "service_to_queue": defaultdict(set),
        }
        
        # Analyze each source directory
        for source_path in self.source_paths:
            if not source_path.exists():
                continue
                
            print(f"   Analyzing: {source_path}")
            
            # Analyze services
            service_files = list(source_path.rglob("*service*.py")) + list(source_path.rglob("**/services/*.py"))
            for service_file in service_files:
                if service_file.stem != "__init__":
                    service_name = service_file.stem.replace("_service", "").replace("Service", "")
                    self._analyze_service_file(service_file, service_name, relationships)
            
            # Analyze controllers
            controller_patterns = ["**/controllers/*.py", "**/routes/*.py", "**/views/*.py", "**/handlers/*.py"]
            for pattern in controller_patterns:
                for controller_file in source_path.glob(pattern):
                    if controller_file.stem != "__init__":
                        controller_name = controller_file.stem.replace("_controller", "").replace("Controller", "")
                        self._analyze_controller_file(controller_file, controller_name, relationships)
            
            # Analyze GraphQL resolvers
            resolver_patterns = ["**/resolvers/*.py", "**/graphql/**/*.py"]
            for pattern in resolver_patterns:
                for resolver_file in source_path.glob(pattern):
                    if resolver_file.stem != "__init__":
                        resolver_name = resolver_file.stem.replace("_resolver", "").replace("Resolver", "")
                        self._analyze_resolver_file(resolver_file, resolver_name, relationships)
        
        # Show summary
        total_service_relations = sum(len(deps) for deps in relationships["service_to_service"].values())
        total_controller_relations = sum(len(deps) for deps in relationships["controller_to_service"].values())
        print(f"   ✅ Found {total_service_relations} service-service, {total_controller_relations} controller-service relationships")
        
        self.relationships = relationships
        return relationships
    
    def _analyze_service_file(self, file_path: Path, service_name: str, relationships: Dict):
        """Analyzes a service file to detect dependencies"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Service-to-service relationships
            service_patterns = [
                r"from (?:src\.)?(?:app\.)?(?:api\.)?services\.(\w+(?:_service)?) import",
                r"from (?:src\.)?(?:app\.)?(?:api\.)?(?:\w+\.)*(\w+_service) import",
                r"(\w+Service)\(",
                r"(\w+_service)\.",
            ]
            
            for pattern in service_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    imported_service = match.group(1).replace("_service", "").replace("Service", "")
                    if imported_service.lower() != service_name.lower():
                        relationships["service_to_service"][service_name].add(imported_service)
            
            # Database relationships
            db_patterns = {
                "MongoDB": [r"MongoClient", r"mongo", r"mongodb", r"MongoDBService"],
                "PostgreSQL": [r"psycopg2", r"asyncpg", r"sqlalchemy", r"Session", r"\.query\("],
                "MySQL": [r"mysql", r"pymysql", r"MySQLdb"],
                "Redis": [r"redis", r"Redis", r"redis_client"],
                "DynamoDB": [r"dynamodb", r"DynamoDB", r"boto3.*dynamodb"],
            }
            
            for db_name, patterns in db_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        relationships["service_to_database"][service_name].add(db_name)
                        break
            
            # Storage relationships
            storage_patterns = {
                "S3": [r"boto3.*s3", r"s3_client", r"\.s3\.", r"S3"],
                "Google Cloud Storage": [r"google.*storage", r"gcs"],
                "Azure Blob": [r"azure.*blob", r"BlobService"],
            }
            
            for storage_name, patterns in storage_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        relationships["service_to_storage"][service_name].add(storage_name)
                        break
            
            # Message queue relationships
            queue_patterns = {
                "SQS": [r"sqs", r"SQS", r"boto3.*sqs"],
                "SNS": [r"sns", r"SNS", r"boto3.*sns"],
                "RabbitMQ": [r"rabbitmq", r"pika", r"celery"],
                "Kafka": [r"kafka", r"confluent"],
                "Pub/Sub": [r"pubsub", r"google.*pubsub"],
            }
            
            for queue_name, patterns in queue_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        relationships["service_to_queue"][service_name].add(queue_name)
                        break
            
        except Exception as e:
            print(f"⚠️ Error analyzing {file_path}: {e}")
    
    def _analyze_controller_file(self, file_path: Path, controller_name: str, relationships: Dict):
        """Analyzes a controller file to detect services used"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Controller-to-service relationships
            service_patterns = [
                r"from (?:src\.)?(?:app\.)?(?:api\.)?services\.(\w+(?:_service)?) import",
                r"(\w+Service)\(",
                r"(\w+_service)\.",
            ]
            
            for pattern in service_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    imported_service = match.group(1).replace("_service", "").replace("Service", "")
                    relationships["controller_to_service"][controller_name].add(imported_service)
            
        except Exception as e:
            print(f"⚠️ Error analyzing {file_path}: {e}")
    
    def _analyze_resolver_file(self, file_path: Path, resolver_name: str, relationships: Dict):
        """Analyzes a GraphQL resolver file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Resolver-to-service relationships
            service_patterns = [
                r"from (?:src\.)?(?:app\.)?(?:api\.)?services\.(\w+(?:_service)?) import",
                r"(\w+Service)\(",
                r"(\w+_service)\.",
            ]
            
            for pattern in service_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    imported_service = match.group(1).replace("_service", "").replace("Service", "")
                    relationships["resolver_to_service"][resolver_name].add(imported_service)
            
        except Exception as e:
            print(f"⚠️ Error analyzing {file_path}: {e}")
    
    def generate_suggestions(self) -> List[Dict]:
        """Generates suggestions to improve the diagram"""
        suggestions = []
        
        # Suggest missing service connections
        for service, dependencies in self.relationships.get("service_to_service", {}).items():
            if dependencies:
                suggestions.append({
                    "type": "service_connection",
                    "from": service,
                    "to": list(dependencies),
                    "reason": f"Service {service} depends on other services",
                    "priority": "high"
                })
        
        # Suggest logical groupings
        service_groups = self._suggest_service_groups()
        if service_groups:
            suggestions.append({
                "type": "grouping",
                "groups": service_groups,
                "reason": "Related services can be grouped together",
                "priority": "medium"
            })
        
        # Suggest label improvements
        label_suggestions = self._suggest_label_improvements()
        suggestions.extend(label_suggestions)
        
        self.suggestions = suggestions
        return suggestions
    
    def _suggest_service_groups(self) -> Dict[str, List[str]]:
        """Suggests logical groupings of services"""
        groups = {
            "Core Services": [],
            "Data Processing": [],
            "Authentication": [],
            "Notification": [],
            "File Processing": [],
            "Analytics": [],
        }
        
        services = self.components.get("services", [])
        
        for service in services:
            service_lower = service.lower()
            
            # Authentication services
            if any(keyword in service_lower for keyword in ["auth", "user", "login", "token", "jwt"]):
                groups["Authentication"].append(service)
            # Notification services
            elif any(keyword in service_lower for keyword in ["notification", "email", "sms", "message"]):
                groups["Notification"].append(service)
            # File processing
            elif any(keyword in service_lower for keyword in ["file", "upload", "download", "storage", "document"]):
                groups["File Processing"].append(service)
            # Analytics
            elif any(keyword in service_lower for keyword in ["analytics", "report", "metric", "stat"]):
                groups["Analytics"].append(service)
            # Data processing
            elif any(keyword in service_lower for keyword in ["process", "transform", "etl", "data"]):
                groups["Data Processing"].append(service)
            # Core services (fallback)
            else:
                groups["Core Services"].append(service)
        
        # Filter empty groups
        return {k: v for k, v in groups.items() if v}
    
    def _suggest_label_improvements(self) -> List[Dict]:
        """Suggests improvements in labels and titles"""
        suggestions = []
        
        # Improve diagram title based on detected framework
        framework = self.components.get("framework", "Application")
        current_title = "Application Architecture"
        
        if framework != "Unknown":
            suggested_title = f"{framework} Application Architecture"
            suggestions.append({
                "type": "label",
                "component": "diagram_title",
                "current": current_title,
                "suggested": suggested_title,
                "reason": f"More specific title including {framework}",
                "priority": "low"
            })
        
        return suggestions
    
    def refine_architecture_code(self, architecture_code: str) -> str:
        """Refines the diagram code applying suggestions"""
        print("✨ Applying AI refinements...")
        
        # Apply grouping suggestions
        refined_code = self._apply_grouping_suggestions(architecture_code)
        
        # Apply connection suggestions
        refined_code = self._apply_connection_suggestions(refined_code)
        
        # Apply label suggestions
        refined_code = self._apply_label_suggestions(refined_code)
        
        return refined_code
    
    def _apply_grouping_suggestions(self, code: str) -> str:
        """Applies service grouping suggestions"""
        # For now, keep simple structure
        # Future: add specific service clusters
        return code
    
    def _apply_connection_suggestions(self, code: str) -> str:
        """Applies connection suggestions between components"""
        # Count total relationships for reporting
        total_relations = sum(len(deps) for deps in self.relationships.get("service_to_service", {}).values())
        
        if total_relations > 0:
            # Add informative comment about detected relationships
            comment = f"\n    # AI Detected {total_relations} service-to-service relationships\n"
            comment += "    # (Services shown as group; individual connections not displayed)\n"
            
            # Insert after FLOWS section
            flows_pos = code.find("# FLOWS")
            if flows_pos != -1:
                # Find end of flows section
                flows_end = code.find("\n    # Background", flows_pos)
                if flows_end == -1:
                    flows_end = len(code)
                code = code[:flows_end] + comment + code[flows_end:]
        
        return code
    
    def _apply_label_suggestions(self, code: str) -> str:
        """Applies label improvements"""
        for suggestion in self.suggestions:
            if suggestion["type"] == "label" and suggestion["component"] == "diagram_title":
                code = code.replace(
                    suggestion["current"],
                    suggestion["suggested"]
                )
        
        return code
    
    def save_refinement_report(self, output_file: str = None):
        """Saves refinement report"""
        if output_file is None:
            output_file = Path(__file__).parent / "ai_refinement_report.json"
        else:
            output_file = Path(output_file)
        
        report = {
            "relationships": {
                k: {key: list(val) if isinstance(val, set) else val 
                    for key, val in v.items()} 
                for k, v in self.relationships.items()
            },
            "suggestions": self.suggestions,
            "summary": {
                "total_relationships": sum(len(v) for v in self.relationships.values() if isinstance(v, dict)),
                "total_suggestions": len(self.suggestions),
                "high_priority_suggestions": len([s for s in self.suggestions if s.get("priority") == "high"])
            }
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Refinement report saved to: {output_file}")


if __name__ == "__main__":
    try:
        print("🤖 Starting AI relationship analysis...")
        refiner = AIRefiner()
        
        print("\n📊 Step 1: Analyzing relationships...")
        relationships = refiner.analyze_relationships()
        
        print("\n💡 Step 2: Generating suggestions...")
        suggestions = refiner.generate_suggestions()
        
        print("\n💾 Step 3: Saving report...")
        refiner.save_refinement_report()
        
        print(f"\n✅ AI relationship analysis completed:")
        print(f"  Services with dependencies: {len(relationships.get('service_to_service', {}))}")
        print(f"  Controllers with services: {len(relationships.get('controller_to_service', {}))}")
        total_db_relations = sum(len(deps) for deps in relationships.get('service_to_database', {}).values())
        print(f"  Database connections: {total_db_relations}")
        total_storage_relations = sum(len(deps) for deps in relationships.get('service_to_storage', {}).values())
        print(f"  Storage connections: {total_storage_relations}")
        print(f"  Generated suggestions: {len(suggestions)}")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("   Run first: python analyze_repo.py")
        exit(1)
    except Exception as e:
        import traceback
        print(f"\n❌ Unexpected error: {e}")
        print(f"   Details:\n{traceback.format_exc()}")
        exit(1)