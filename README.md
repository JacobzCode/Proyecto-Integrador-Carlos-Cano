# MoodKeeper 🧠💚

**Plataforma web para monitorear el estado emocional y mental de jóvenes en contextos vulnerables**

MoodKeeper es un sistema integral de monitoreo emocional que permite a usuarios registrar su estado anímico diario, analizar tendencias, recibir alertas de riesgo y obtener recomendaciones personalizadas. Desarrollado como proyecto integrador académico.

---

## 🎯 Características Principales

### Funcionalidades Core
- ✅ **Autenticación JWT** - Registro, login y logout seguro
- ✅ **Encuestas Emocionales** - Registro de mood (1-10) con campos extendidos
- ✅ **Dashboard Interactivo** - Visualizaciones con Chart.js y matplotlib
- ✅ **Análisis Inteligente** - Algoritmo de riesgo compuesto multi-factor
- ✅ **Alertas de Riesgo** - Detección automática con análisis de tendencias
- ✅ **Recomendaciones Personalizadas** - Sistema basado en nivel de riesgo
- ✅ **Análisis de Correlaciones** - Insights entre variables (mood, sueño, apetito)

### Campos de Encuesta
- **Mood** (1-10): Estado de ánimo general
- **Sleep Hours** (0-24): Horas de sueño última noche
- **Appetite** (1-10): Nivel de apetito
- **Concentration** (1-10): Capacidad de concentración
- **Comment**: Notas adicionales (opcional)

### Algoritmo de Riesgo
- Score compuesto (0-100) con pesos configurables
- Detección de tendencias negativas (últimas 3 entradas)
- Clasificación en 3 niveles: **ALTO** 🚨, **MODERADO** ⚠️, **BAJO** ✅

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

**Backend:**
- Python 3.11+
- FastAPI 0.104.1 (framework web async)
- Uvicorn (servidor ASGI)
- Pydantic (validación de datos)
- passlib + python-jose (seguridad)
- pandas + matplotlib + seaborn (analytics)

**Frontend:**
- HTML5 + CSS3 + JavaScript vanilla
- Bootstrap 5.3.2 (UI framework)
- Chart.js (gráficos interactivos)

**Persistencia:**
- CSV files (desarrollo)
- Planificado: SQLite/PostgreSQL (producción)

### Estructura de Proyecto

```
mood-keeper/
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias core
├── requirements-insights.txt  # Dependencias analytics
├── CHANGELOG.md              # Registro de cambios
├── README.md                 # Este archivo
├── EXAMPLES.md               # Ejemplos de uso API
│
├── app/                      # Código fuente backend
│   ├── __init__.py
│   ├── server.py            # FastAPI routes (endpoints)
│   ├── security.py          # Autenticación JWT
│   ├── storage.py           # Persistencia CSV
│   ├── dto.py               # Modelos Pydantic
│   ├── insights.py          # Análisis y visualizaciones
│   └── utils.py             # Utilidades comunes
│
├── data/                     # Datos persistentes
│   ├── accounts.csv         # Usuarios registrados
│   ├── entries.csv          # Encuestas emocionales
│   └── recommendations.csv  # Recomendaciones por nivel
│
├── documentation/           # Documentación formal
│   ├── project_plan.md     # Plan del proyecto
│   ├── TECHNICAL_REPORT.md # Decisiones técnicas
│   ├── DELIVERY_CHECKLIST.md # Checklist de entregas
│   └── DATA_DICTIONARY.md  # Diccionario de datos
│
├── EVIDENCE/                # Evidencia visual/técnica
│   ├── screenshots/        # Capturas de pantalla
│   ├── diagrams/           # Diagramas técnicos
│   └── git-history/        # Historial Git
│
└── frontend/               # Aplicación web
    ├── index.html         # Página principal
    ├── login.html         # Inicio de sesión
    ├── register.html      # Registro
    ├── dashboard.html     # Dashboard principal
    ├── profile.html       # Perfil de usuario
    ├── app.js            # Lógica frontend
    └── styles.css        # Estilos personalizados
```

---

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.11 o superior
- pip (gestor de paquetes)
- Navegador web moderno

### 1. Clonar Repositorio
```powershell
cd c:\Users\car\Desktop\INTEGRADORCARLOSCANO
# Si hay repositorio Git:
# git clone <url>
```

### 2. Crear Entorno Virtual
```powershell
cd mood-keeper
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependencias

**Instalación Mínima (Core):**
```powershell
pip install -r requirements.txt
```

**Instalación Completa (con Analytics):**
```powershell
pip install -r requirements.txt
pip install -r requirements-insights.txt
```

### 4. Iniciar Servidor Backend
```powershell
python main.py
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5. Abrir Frontend

**Opción A - VS Code Live Server:**
1. Abrir `frontend/index.html` en VS Code
2. Click derecho → "Open with Live Server"
3. Navegar a http://127.0.0.1:5500/frontend/

**Opción B - Abrir directamente:**
1. Abrir `frontend/index.html` en navegador
2. Configurar CORS si es necesario

### 6. Probar API con Swagger
Visitar: **http://127.0.0.1:8001/docs**

---

## 📡 API Endpoints

### Autenticación

**POST** `/api/accounts` - Crear cuenta
```json
{
  "handle": "usuario123",
  "email": "usuario@example.com",
  "secret": "password123"
}
```

**POST** `/api/sessions` - Iniciar sesión
```json
{
  "handle": "usuario123",
  "secret": "password123"
}
```

**POST** `/api/sessions/logout` - Cerrar sesión
- Requiere: `Authorization: Bearer <token>`

### Encuestas

**POST** `/api/entries` - Crear encuesta
```json
{
  "mood": 7,
  "comment": "Me siento bien hoy",
  "sleep_hours": 8.0,
  "appetite": 8,
  "concentration": 9
}
```

**GET** `/api/entries` - Listar todas las encuestas

### Insights & Analytics

**GET** `/api/insights/summary` - Resumen estadístico

**GET** `/api/insights/average` - Promedio por usuario

**GET** `/api/insights/alerts?threshold=3&days=30` - Alertas de riesgo

**GET** `/api/insights/correlations` - Correlaciones entre variables

**GET** `/api/insights/plot/{plot_name}?type={type}` - Generar gráfico PNG
- `plot_name`: `hist`, `by_handle`, `ts`
- `type`: `bar`, `pie`, `scatter`, etc.

### Recomendaciones

**GET** `/api/recommendations?risk_level=ALTO` - Obtener recomendaciones
- `risk_level`: `ALTO`, `MODERADO`, `BAJO`

---

## 🧪 Testing

### Manual Testing

**1. Registro y Login:**
```powershell
# Crear cuenta
curl -X POST http://127.0.0.1:8001/api/accounts `
  -H "Content-Type: application/json" `
  -d '{"handle":"testuser","email":"test@example.com","secret":"pass123"}'

# Login
curl -X POST http://127.0.0.1:8001/api/sessions `
  -H "Content-Type: application/json" `
  -d '{"handle":"testuser","secret":"pass123"}'
```

**2. Crear Encuesta:**
```powershell
curl -X POST http://127.0.0.1:8001/api/entries `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer <TOKEN>" `
  -d '{"mood":7,"sleep_hours":8.0,"appetite":8,"concentration":9}'
```

**3. Ver Alertas:**
```powershell
curl http://127.0.0.1:8001/api/insights/alerts?threshold=3&days=30
```

### Automated Testing (Futuro)
- Implementar tests con `pytest`
- Crear fixtures de datos de prueba
- Tests de integración con TestClient de FastAPI

---

## 📊 Análisis de Riesgo

### Algoritmo Compuesto

El sistema calcula un **score compuesto (0-100)** basado en:

| Factor | Peso | Rango | Normalización |
|--------|------|-------|---------------|
| Mood | 40% | 1-10 | Lineal |
| Sleep | 20% | 0-24h | Curva (óptimo: 7-9h) |
| Appetite | 20% | 1-10 | Lineal |
| Concentration | 20% | 1-10 | Lineal |

### Clasificación de Riesgo

```python
if composite_score < 40 or (composite_score < 60 and trend_negative):
    risk = 'ALTO'  # 🚨 Requiere atención inmediata
elif composite_score < 70 or (composite_score < 80 and trend_negative):
    risk = 'MODERADO'  # ⚠️ Monitoreo recomendado
else:
    risk = 'BAJO'  # ✅ Estado saludable
```

### Detección de Tendencias

- Analiza últimas **3 entradas** por usuario
- Detecta declive consistente en mood
- Ajusta nivel de riesgo si hay tendencia negativa

---

## 📚 Documentación Adicional

- **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios detallado
- **[EXAMPLES.md](EXAMPLES.md)** - Ejemplos de uso de API
- **[documentation/project_plan.md](documentation/project_plan.md)** - Plan completo del proyecto
- **[documentation/TECHNICAL_REPORT.md](documentation/TECHNICAL_REPORT.md)** - Informe técnico
- **[documentation/DATA_DICTIONARY.md](documentation/DATA_DICTIONARY.md)** - Esquemas de datos

---

## 🔧 Configuración Avanzada

### Variables de Entorno (Futuro)

```bash
# .env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///moodkeeper.db
DEBUG=False
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500
```

### Migración a Base de Datos

Ver [DATA_DICTIONARY.md](documentation/DATA_DICTIONARY.md) para esquemas SQL recomendados.

---

## 🤝 Contribución

Este es un proyecto académico. Para mejoras:

1. Fork el repositorio
2. Crear branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "feat: agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abrir Pull Request

### Estilo de Código

- **Python:** PEP 8
- **JavaScript:** StandardJS
- **Commits:** Conventional Commits

---

## 📝 Licencia

Proyecto académico - Universidad XYZ  
Todos los derechos reservados © 2025

---

## 👤 Autor

**Carlos Cano**  
Proyecto Integrador - Ingeniería de Sistemas  
Universidad XYZ - 2025

---

## 📞 Soporte

- **Documentación:** Ver carpeta `documentation/`
- **Issues:** Reportar en repositorio Git
- **Email:** carlos@example.com

---

## 🎯 Estado del Proyecto

**Versión:** 1.1.0  
**Estado:** ✅ Desarrollo Activo  
**Cumplimiento:** 85% (ver [DELIVERY_CHECKLIST.md](documentation/DELIVERY_CHECKLIST.md))

**Última Actualización:** 7 de noviembre de 2025

---

## 🌟 Agradecimientos

- Proyecto de referencia: EmoTrack (análisis de patrones)
- FastAPI Team por excelente framework
- Bootstrap Team por componentes UI
- Chart.js por visualizaciones interactivas
