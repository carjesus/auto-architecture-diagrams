# 🏗️ Auto Architecture Diagrams

**Generación automática de diagramas de arquitectura con análisis inteligente y refinamiento AI**

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.7%2B-green)](https://python.org)
[![Diagrams](https://img.shields.io/badge/Diagrams-Library-orange)](https://diagrams.mingrammer.com/)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple)](https://github.com)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema inteligente que analiza automáticamente tu repositorio y genera diagramas de arquitectura profesionales sin intervención manual. Incluye refinamiento con AI similar a [TerraVision](https://github.com/patrickchugh/terravision).

## ✨ Características

🤖 **Análisis Automático**: Detecta automáticamente componentes, servicios, bases de datos y dependencias  
🧠 **Refinamiento con AI**: Analiza relaciones entre servicios y mejora el diagrama inteligentemente  
⚡ **GitHub Actions**: Generación automática en cada push - sin configuración manual  
🎨 **Diagramas Profesionales**: Usa la librería `diagrams` para crear visualizaciones de calidad  
📊 **Múltiples Tecnologías**: Soporta FastAPI, Django, Flask, PostgreSQL, MongoDB, AWS, y más  
🔄 **Siempre Actualizado**: El diagrama se actualiza automáticamente cuando cambias el código  

## 🚀 Inicio Rápido

### 1. Copia los archivos a tu repositorio

```bash
# Crear estructura de carpetas
mkdir -p .github/workflows
mkdir -p docs/diagrams

# Descargar y copiar archivos
# Opción A: Descargar ZIP desde GitHub
# Opción B: Clonar y copiar
git clone https://github.com/tu-usuario/auto-architecture-diagrams.git
cp auto-architecture-diagrams/workflows/* .github/workflows/
cp auto-architecture-diagrams/scripts/* docs/diagrams/
```

### 2. Instalar dependencias

Agregar a tu `requirements.txt`:
```
diagrams>=0.23.0
```

O instalar directamente:
```bash
pip install diagrams
```

### 3. Configurar GitHub Actions

1. Ve a **Settings** → **Actions** → **General** en tu repositorio
2. Selecciona **Read and write permissions**
3. Marca **Allow GitHub Actions to create and approve pull requests**

### 4. ¡Listo! 🎉

El sistema se ejecutará automáticamente cuando:
- Hagas push de cambios en tu código
- Modifiques archivos de configuración
- Ejecutes manualmente desde GitHub Actions

## 📁 Estructura del Proyecto

```
tu-repositorio/
├── .github/
│   └── workflows/
│       ├── generate-diagram.yml          # Workflow manual
│       └── generate-diagram-auto.yml     # Workflow automático
├── docs/
│   └── diagrams/
│       ├── analyze_repo.py               # Analizador de repositorio
│       ├── ai_refiner.py                 # Refinamiento con AI
│       ├── generate_architecture.py      # Generador automático
│       ├── architecture.py               # Generado automáticamente
│       ├── test_diagram.py               # Script de pruebas
│       └── README.md                     # Documentación detallada
└── requirements.txt                      # Incluir: diagrams>=0.23.0
```

## 🔧 Configuración

### Para Proyectos Python

El sistema detecta automáticamente:
- **Frameworks**: FastAPI, Django, Flask, Starlette
- **Bases de datos**: PostgreSQL, MongoDB, MySQL, SQLite, Redis
- **Servicios AWS**: S3, RDS, Lambda, DynamoDB, SNS, SQS
- **Servicios GCP**: Cloud Storage, BigQuery, Pub/Sub
- **Servicios Azure**: Blob Storage, Service Bus, Functions
- **Estructura**: Controllers, Services, Models, APIs

### Personalización

Edita `docs/diagrams/analyze_repo.py` para:
- Agregar nuevos patrones de detección
- Personalizar la estructura de tu proyecto
- Incluir tecnologías específicas

## 🤖 Refinamiento con AI

El sistema incluye análisis inteligente que:

✅ **Detecta relaciones automáticamente**: Analiza qué servicios llaman a otros  
✅ **Mejora conexiones**: Identifica y sugiere conexiones lógicas  
✅ **Optimiza etiquetas**: Mejora títulos y descripciones  
✅ **Sugiere agrupaciones**: Propone clusters lógicos de componentes  
✅ **Aplica mejores prácticas**: Sigue estándares de diagramación  

## 📊 Ejemplo de Diagrama Generado

El sistema genera diagramas como este:

```
┌─────────────────────────────────────────────────────────────┐
│                    API Clients/Users                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Application Layer                            │
│  ┌─────────────────┐    ┌──────────────────────────────────┐ │
│  │ FastAPI App     │    │        API Endpoints             │ │
│  │ (Uvicorn)       │    │  ┌─────────────┐ ┌─────────────┐ │ │
│  └─────────────────┘    │  │ REST API    │ │ GraphQL API │ │ │
│                         │  │ Controllers │ │ Resolvers   │ │ │
│                         │  └─────────────┘ └─────────────┘ │ │
│                         └──────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                Business Logic                           │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │ Services    │ │ Data Models │ │ Background Jobs     │ │ │
│  │  │ Layer       │ │ SQLAlchemy  │ │ (Cron/Scheduler)    │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Data Layer                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ PostgreSQL  │ │ MongoDB     │ │ S3 Storage              │ │
│  │ Main DB     │ │ Results     │ │ Files/Documents         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Workflows Disponibles

### 1. Workflow Manual (`generate-diagram.yml`)
- Se ejecuta cuando modificas `architecture.py`
- Para casos donde quieres control manual del diagrama

### 2. Workflow Automático (`generate-diagram-auto.yml`)
- Se ejecuta automáticamente en cada push
- Analiza el código, genera el diagrama y hace commit automáticamente
- **Recomendado para la mayoría de proyectos**

## 📝 Uso

### Automático (Recomendado)
1. Haz push de tu código
2. El sistema analiza automáticamente los cambios
3. Genera/actualiza el diagrama
4. Hace commit del diagrama actualizado

### Manual
```bash
cd docs/diagrams

# 1. Analizar repositorio
python analyze_repo.py

# 2. Refinamiento con AI (opcional)
python ai_refiner.py

# 3. Generar código del diagrama
python generate_architecture.py

# 4. Crear imagen PNG
python architecture.py
```

## 🔍 Tecnologías Soportadas

### Frameworks Web
- FastAPI
- Django
- Flask
- Starlette
- Express.js (Node.js)

### Bases de Datos
- PostgreSQL
- MongoDB
- MySQL
- SQLite
- Redis

### Servicios Cloud

**AWS:**
- S3 (Storage)
- RDS (Database)
- Lambda (Functions)
- DynamoDB (NoSQL)
- SNS/SQS (Messaging)

**GCP:**
- Cloud Storage
- BigQuery
- Pub/Sub

**Azure:**
- Blob Storage
- Service Bus
- Functions

### Otros
- GraphQL (Strawberry, Graphene, Ariadne)
- Background Jobs (APScheduler, Celery)
- Docker containers
- Kubernetes orchestration

## 🎯 Casos de Uso

✅ **Documentación automática** de arquitectura  
✅ **Onboarding** de nuevos desarrolladores  
✅ **Revisiones de código** con contexto visual  
✅ **Presentaciones** a stakeholders  
✅ **Auditorías** de arquitectura  
✅ **Planificación** de refactoring  

## 🚨 Solución de Problemas

### Problemas Comunes

**1. Workflow no se ejecuta**
- Verifica que los archivos estén en la rama `main`/`master`
- Revisa los permisos de GitHub Actions
- Ejecuta manualmente desde la pestaña Actions

**2. Error "scripts not found"**
```bash
# Asegúrate de copiar los scripts
cp auto-architecture-diagrams/scripts/* docs/diagrams/
git add docs/diagrams/
git commit -m "add diagram scripts"
git push
```

**3. Error "graphviz not found"**
- El workflow instala Graphviz automáticamente
- Para uso local: `sudo apt-get install graphviz` (Linux) o `brew install graphviz` (macOS)

**4. Error "diagrams module not found"**
```bash
pip install diagrams
# O agregar a requirements.txt: diagrams>=0.23.0
```

## 📚 Documentación Adicional

- [📋 Guía de Instalación](SETUP.md) - Configuración paso a paso
- [🤝 Guía de Contribución](CONTRIBUTING.md) - Cómo contribuir al proyecto
- [📝 Documentación de Scripts](scripts/README.md) - Detalles técnicos

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Ve [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

MIT License - ve [LICENSE](LICENSE) para más detalles.

## 🙏 Inspiración

Este proyecto está inspirado en:
- [TerraVision](https://github.com/patrickchugh/terravision) - Professional Cloud Architecture Diagrams
- [Diagrams](https://diagrams.mingrammer.com/) - Diagram as Code library

## ⭐ ¿Te gusta el proyecto?

Si este proyecto te ayuda, ¡dale una estrella! ⭐

---

**¿Preguntas o problemas?** Abre un [issue](../../issues) y te ayudaremos.