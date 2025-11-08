# EVIDENCE — MoodKeeper

Este directorio contiene evidencia visual y técnica del proyecto MoodKeeper.

## Estructura de Carpetas

```
EVIDENCE/
├── screenshots/          # Capturas de pantalla de la aplicación
│   ├── 01_landing_page.png
│   ├── 02_login.png
│   ├── 03_register.png
│   ├── 04_dashboard.png
│   ├── 05_profile.png
│   ├── 06_swagger_api.png
│   ├── 07_chart_mood_trend.png
│   ├── 08_chart_distribution.png
│   └── 09_alerts_view.png
│
├── diagrams/             # Diagramas técnicos
│   ├── architecture.png
│   ├── data_flow.png
│   └── er_diagram.png
│
└── git-history/          # Evidencia de Git
    ├── commits.txt
    ├── branches.txt
    └── contributors.txt
```

## Screenshots Requeridos

### 1. Frontend

**Archivo:** `01_landing_page.png`
- **Descripción:** Página inicial (index.html)
- **URL:** http://127.0.0.1:5500/frontend/index.html
- **Elementos clave:** Header, descripción del proyecto, botones de acción

**Archivo:** `02_login.png`
- **Descripción:** Formulario de inicio de sesión
- **URL:** http://127.0.0.1:5500/frontend/login.html
- **Elementos clave:** Campo username, password, botón login

**Archivo:** `03_register.png`
- **Descripción:** Formulario de registro
- **URL:** http://127.0.0.1:5500/frontend/register.html
- **Elementos clave:** Campos username, email, password, botón register

**Archivo:** `04_dashboard.png`
- **Descripción:** Dashboard principal con gráficos
- **URL:** http://127.0.0.1:5500/frontend/dashboard.html
- **Elementos clave:** Estadísticas, gráfico Chart.js, lista de encuestas

**Archivo:** `05_profile.png`
- **Descripción:** Página de perfil de usuario
- **URL:** http://127.0.0.1:5500/frontend/profile.html
- **Elementos clave:** Información del usuario, formulario de nueva encuesta

### 2. Backend

**Archivo:** `06_swagger_api.png`
- **Descripción:** Documentación interactiva de API (Swagger UI)
- **URL:** http://127.0.0.1:8001/docs
- **Elementos clave:** Lista de endpoints, schemas, Try it out

**Archivo:** `07_chart_mood_trend.png`
- **Descripción:** Gráfico de tendencia de mood (matplotlib)
- **URL:** http://127.0.0.1:8001/api/insights/plot.png?handle=carlos
- **Elementos clave:** Línea temporal, ejes, título

**Archivo:** `08_chart_distribution.png`
- **Descripción:** Gráfico de distribución de mood
- **URL:** Dashboard o análisis exploratorio
- **Elementos clave:** Barras o histograma, distribución 1-10

### 3. Funcionalidades Avanzadas

**Archivo:** `09_alerts_view.png`
- **Descripción:** Vista de alertas de riesgo (futuro)
- **URL:** Dashboard o endpoint /api/alerts
- **Elementos clave:** Lista de alertas, niveles de riesgo, recomendaciones

## Diagramas Técnicos

### 1. Arquitectura del Sistema

**Archivo:** `architecture.png`

```
┌──────────────┐
│   Frontend   │  (HTML/CSS/JS)
│  Bootstrap 5 │
└──────┬───────┘
       │ HTTP/REST
       │
┌──────▼───────┐
│   FastAPI    │  (Python 3.11+)
│   Backend    │
├──────────────┤
│ - server.py  │
│ - security   │
│ - storage    │
│ - insights   │
└──────┬───────┘
       │
┌──────▼───────┐
│  CSV Files   │
│ (accounts,   │
│  entries)    │
└──────────────┘
```

### 2. Flujo de Datos

**Archivo:** `data_flow.png`

```
Usuario → Login → JWT Token → Dashboard → API Calls → CSV Storage
                                    ↓
                              Insights/Charts
```

### 3. Diagrama ER

**Archivo:** `er_diagram.png`

```
┌──────────────┐         ┌──────────────┐
│   accounts   │1      N │   entries    │
├──────────────┤─────────┤──────────────┤
│ id (PK)      │         │ id (PK)      │
│ handle       │         │ account_id   │
│ email        │         │ mood         │
│ hashed       │         │ comment      │
│ created      │         │ created      │
└──────────────┘         └──────────────┘
```

## Git History Evidence

### commits.txt

Lista de commits realizados:
```
commit abc123 - Initial commit: Project structure
commit def456 - feat: Add authentication system
commit ghi789 - feat: Implement insights module
commit jkl012 - docs: Add formal documentation
```

### branches.txt

Ramas del proyecto:
```
* main
  feature/alerts
  feature/recommendations
```

### contributors.txt

Contribuidores:
```
Carlos Cano <carlos@example.com>
```

## Instrucciones para Tomar Screenshots

### Herramientas Recomendadas

1. **Windows Snipping Tool** (Win + Shift + S)
2. **PowerShell screenshot:**
   ```powershell
   Add-Type -AssemblyName System.Windows.Forms
   [System.Windows.Forms.SendKeys]::SendWait("%{PRTSC}")
   ```

### Proceso

1. **Iniciar servidor backend:**
   ```powershell
   cd c:\Users\car\Desktop\INTEGRADORCARLOSCANO\mood-keeper
   python main.py
   ```

2. **Abrir frontend con Live Server** (VS Code)

3. **Tomar screenshots:**
   - Navegar a cada URL
   - Presionar Win + Shift + S
   - Seleccionar área
   - Guardar con nombre correspondiente

4. **Verificar calidad:**
   - Resolución mínima: 1280x720
   - Formato: PNG
   - Sin información sensible visible

## Checklist de Evidencia

### Primera Entrega (Actual)

- [ ] `01_landing_page.png`
- [ ] `02_login.png`
- [ ] `03_register.png`
- [ ] `04_dashboard.png`
- [ ] `05_profile.png`
- [ ] `06_swagger_api.png`
- [ ] `07_chart_mood_trend.png`
- [ ] `architecture.png` (diagrama conceptual)
- [ ] `commits.txt` (cuando se inicialice Git)

### Segunda Entrega (Futuro)

- [ ] `08_chart_distribution.png`
- [ ] `09_alerts_view.png`
- [ ] `data_flow.png` (diagrama detallado)
- [ ] `er_diagram.png` (si se migra a BD)
- [ ] Screenshots de correlaciones
- [ ] Screenshots de formulario extendido (sleep, appetite, etc.)

### Tercera Entrega (Futuro)

- [ ] Diagramas de casos de uso
- [ ] Screenshots de recomendaciones
- [ ] Screenshots de tests ejecutándose
- [ ] Video demo (opcional)

## Notas Importantes

### Privacidad

- ❌ **NO incluir** contraseñas reales
- ❌ **NO incluir** datos personales sensibles
- ✅ **SÍ usar** datos de prueba (ej: "carlos", "juan@example.com")

### Calidad

- **Resolución:** Mínimo 1280x720
- **Formato:** PNG (sin compresión)
- **Contenido:** Centrado, sin elementos irrelevantes
- **Nombres:** Descriptivos y numerados

### Organización

- Mantener estructura de carpetas
- Actualizar este README cuando se agreguen archivos
- Incluir fecha en commits.txt

---

**Última actualización:** 7 de noviembre de 2025
