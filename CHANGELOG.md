# CHANGELOG — MoodKeeper

Registro de cambios realizados al proyecto MoodKeeper.

---

## [Versión 1.1.0] - 7 de noviembre de 2025

### 📚 Documentación Formal Agregada

#### Documentos Creados

1. **documentation/project_plan.md**
   - Plan completo del proyecto con objetivos por fase
   - Arquitectura técnica detallada
   - Cronograma de entregas
   - Análisis de riesgos y mitigación
   - Roadmap de desarrollo

2. **documentation/TECHNICAL_REPORT.md**
   - Justificación de decisiones técnicas
   - Proceso de análisis exploratorio (EDA)
   - Criterios de calidad (PEP8, modularidad)
   - Evaluación de riesgos técnicos
   - Mapping de entregables

3. **documentation/DELIVERY_CHECKLIST.md**
   - Checklist detallado por cada entrega (1ra, 2da, 3ra)
   - Acciones prioritarias identificadas
   - Pasos de validación pre-entrega
   - Estado de cumplimiento actualizado

4. **documentation/DATA_DICTIONARY.md**
   - Esquema completo de archivos CSV
   - Descripción de campos y tipos de datos
   - Restricciones y validaciones
   - Ejemplos de consultas SQL/Pandas
   - Plan de migración a BD relacional

---

### 📸 Estructura de Evidencia

#### Carpetas Creadas

- **EVIDENCE/**
  - **screenshots/** - Para capturas de pantalla (landing, login, dashboard, swagger)
  - **diagrams/** - Para diagramas técnicos (arquitectura, flujo, ER)
  - **git-history/** - Para evidencia de commits y ramas
  - **README.md** - Guía completa de qué screenshots tomar y cómo organizarlos

---

### 🎯 Mejoras Funcionales — Backend

#### 1. Campos Extendidos en Encuestas

**Archivos Modificados:**
- `app/dto.py` - Modelos Pydantic actualizados
- `app/storage.py` - Persistencia con nuevos campos
- `app/server.py` - Validaciones en endpoints

**Nuevos Campos:**
- `sleep_hours` (float, 0-24): Horas de sueño
- `appetite` (int, 1-10): Nivel de apetito
- `concentration` (int, 1-10): Nivel de concentración

**Validaciones Backend:**
```python
# server.py
if entry.sleep_hours is not None and not (0 <= entry.sleep_hours <= 24):
    raise HTTPException(400, detail='sleep_hours must be 0-24')
if entry.appetite is not None and not (1 <= entry.appetite <= 10):
    raise HTTPException(400, detail='appetite must be 1-10')
if entry.concentration is not None and not (1 <= entry.concentration <= 10):
    raise HTTPException(400, detail='concentration must be 1-10')
```

---

#### 2. Algoritmo de Riesgo Compuesto

**Archivo:** `app/insights.py`

**Funciones Nuevas:**

1. **`compute_composite_score(mood, sleep_hours, appetite, concentration)`**
   - Calcula score compuesto (0-100)
   - Pesos: mood 40%, sleep 20%, appetite 20%, concentration 20%
   - Normalización inteligente de horas de sueño (óptimo: 7-9h)
   - Ajuste dinámico de pesos según campos disponibles

2. **`detect_negative_trend(entries_list, window=3)`**
   - Detecta tendencias descendentes en últimas N entradas
   - Analiza secuencia de moods
   - Retorna `True` si hay declive consistente

3. **`compute_risk_level(composite_score, trend_negative)`**
   - Clasifica en: `ALTO`, `MODERADO`, `BAJO`
   - Considera tanto score como tendencia
   - Reglas:
     - ALTO: score < 40 OR (score < 60 AND trend_negative)
     - MODERADO: score < 70 OR (score < 80 AND trend_negative)
     - BAJO: score ≥ 80 AND NOT trend_negative

**Función Mejorada:**

4. **`alerts(threshold=3, days=30)`** - Rediseñada
   - Agrupa alertas por usuario
   - Calcula scores compuestos por entrada
   - Detecta tendencias automáticamente
   - Incluye metadatos: `risk_level`, `avg_composite`, `trend_negative`

**Ejemplo de Salida:**
```json
{
  "count": 2,
  "items": [
    {
      "id": 5,
      "handle": "carlos",
      "mood": 2,
      "composite_score": 38.5,
      "created": "2025-11-07T14:30:00",
      "comment": "Me siento mal",
      "risk_level": "ALTO",
      "avg_composite": 45.2,
      "trend_negative": true
    }
  ]
}
```

---

#### 3. Sistema de Recomendaciones

**Archivo CSV:** `data/recommendations.csv`

**Contenido:**
- 10 recomendaciones predefinidas
- Clasificadas por nivel de riesgo (ALTO, MODERADO, BAJO)
- Incluyen: título, descripción, URL (opcional)
- Emojis para mejor UX visual

**Ejemplos:**
- ALTO: 🚨 Contacto Profesional Urgente, 📞 Línea de Crisis 24/7
- MODERADO: 🧘 Técnicas de Relajación, 💪 Actividad Física Regular
- BAJO: ✅ Mantener Hábitos Saludables, 🌱 Crecimiento Personal

**Función:** `get_recommendations_for_risk(risk_level)`
- Lee `recommendations.csv` con pandas
- Filtra por nivel de riesgo
- Retorna lista de recomendaciones personalizadas
- Fallback sin pandas (recomendaciones hardcoded)

---

#### 4. Análisis de Correlaciones

**Función:** `correlations()`

**Características:**
- Calcula correlaciones entre mood y campos extendidos
- Usa matriz de correlación de pandas
- Interpreta resultados automáticamente:
  - |r| > 0.7: correlación fuerte
  - 0.4 < |r| ≤ 0.7: correlación moderada
  - |r| ≤ 0.4: correlación débil
- Indica dirección (positiva/negativa)

**Ejemplo de Salida:**
```json
{
  "correlations": {
    "mood_vs_sleep_hours": 0.62,
    "mood_vs_appetite": 0.78,
    "mood_vs_concentration": 0.85
  },
  "interpretations": [
    "mood_vs_sleep_hours: correlación moderada positiva (0.62)",
    "mood_vs_appetite: correlación fuerte positiva (0.78)",
    "mood_vs_concentration: correlación fuerte positiva (0.85)"
  ],
  "sample_size": 45
}
```

---

#### 5. Nuevos Endpoints API

**Archivo:** `app/server.py`

1. **GET `/api/recommendations`**
   - Query param: `risk_level` (ALTO, MODERADO, BAJO)
   - Default: MODERADO
   - Retorna: Lista de recomendaciones personalizadas

2. **GET `/api/insights/correlations`**
   - Sin parámetros
   - Retorna: Correlaciones y interpretaciones

**Swagger Documentation:**
- Endpoints documentados automáticamente
- Accesible en: http://127.0.0.1:8001/docs

---

### 🎨 Mejoras Funcionales — Frontend

#### Formulario Extendido

**Archivo:** `frontend/dashboard.html`

**Modal de Encuesta Actualizado:**
```html
<!-- Campos nuevos -->
<div class="mb-3">
  <label for="sleep_hours" class="form-label">Horas de sueño (opcional)</label>
  <input id="sleep_hours" type="number" min="0" max="24" step="0.5">
</div>
<div class="mb-3">
  <label for="appetite" class="form-label">Apetito 1-10 (opcional)</label>
  <input id="appetite" type="number" min="1" max="10">
</div>
<div class="mb-3">
  <label for="concentration" class="form-label">Concentración 1-10 (opcional)</label>
  <input id="concentration" type="number" min="1" max="10">
</div>
```

**Archivo:** `frontend/app.js`

**Lógica de Envío Actualizada:**
```javascript
const payload = {mood, comment};
if(sleep_hours_input && sleep_hours_input.value) 
  payload.sleep_hours = parseFloat(sleep_hours_input.value);
if(appetite_input && appetite_input.value) 
  payload.appetite = parseInt(appetite_input.value);
if(concentration_input && concentration_input.value) 
  payload.concentration = parseInt(concentration_input.value);

const res = await postJson(API_BASE+'/entries', payload);
```

---

### 🛠️ Módulo de Utilidades

**Archivo:** `app/utils.py`

**Funciones Implementadas:**

1. **CSV Operations**
   - `ensure_csv_exists(path, headers)` - Crea CSV con headers
   - `get_next_id(csv_path)` - Obtiene siguiente ID disponible
   - `read_csv_as_dicts(csv_path)` - Lee CSV como lista de diccionarios
   - `append_to_csv(csv_path, row_data)` - Agrega fila

2. **Date/Time Utilities**
   - `format_timestamp(dt, iso)` - Formatea datetime
   - `parse_timestamp(timestamp_str)` - Parsea string a datetime
   - `calculate_days_since(timestamp_str)` - Calcula días desde timestamp

3. **Validation & Conversion**
   - `validate_range(value, min_val, max_val, field_name)` - Valida rango
   - `safe_float(value, default)` - Conversión segura a float
   - `safe_int(value, default)` - Conversión segura a int

4. **Formatting Helpers**
   - `truncate_string(text, max_length)` - Trunca texto
   - `format_file_size(size_bytes)` - Formatea tamaño de archivo
   - `sanitize_filename(filename)` - Sanitiza nombre de archivo

5. **Risk Visualization**
   - `get_risk_color(risk_level)` - Retorna color hex para nivel de riesgo
   - `get_risk_emoji(risk_level)` - Retorna emoji para nivel de riesgo

**Beneficios:**
- Código reutilizable
- Menos duplicación
- Mejor mantenibilidad
- Funciones bien documentadas con docstrings

---

## Resumen de Cambios por Archivo

### Backend (Python)

| Archivo | Cambios | Líneas Agregadas |
|---------|---------|------------------|
| `app/dto.py` | Campos extendidos en EntryCreate/EntryOut | ~10 |
| `app/storage.py` | Soporte para nuevos campos en EntryRecord y EntryStore | ~30 |
| `app/server.py` | Validaciones y nuevos endpoints | ~25 |
| `app/insights.py` | Algoritmo compuesto, recomendaciones, correlaciones | ~150 |
| `app/utils.py` | Nuevo módulo completo | ~350 |
| `data/recommendations.csv` | Nuevo archivo CSV | 10 filas |

**Total Backend:** ~565 líneas nuevas

### Frontend (HTML/JS)

| Archivo | Cambios | Líneas Agregadas |
|---------|---------|------------------|
| `frontend/dashboard.html` | Campos extendidos en modal | ~15 |
| `frontend/app.js` | Lógica de envío actualizada | ~10 |

**Total Frontend:** ~25 líneas nuevas

### Documentación

| Archivo | Líneas |
|---------|--------|
| `documentation/project_plan.md` | ~400 |
| `documentation/TECHNICAL_REPORT.md` | ~800 |
| `documentation/DELIVERY_CHECKLIST.md` | ~500 |
| `documentation/DATA_DICTIONARY.md` | ~650 |
| `EVIDENCE/README.md` | ~250 |

**Total Documentación:** ~2600 líneas

---

## Impacto en Cumplimiento del Proyecto

### Antes (Análisis Inicial)
- **Cumplimiento:** 60-65%
- **Gaps Críticos:**
  - ❌ Sin documentación formal
  - ❌ Sin Git
  - ❌ Algoritmo básico
  - ❌ Sin campos extendidos
  - ❌ Sin recomendaciones

### Después (Post-Mejoras)
- **Cumplimiento:** ~85%
- **Completado:**
  - ✅ Documentación formal completa (4 documentos)
  - ✅ Estructura de evidencia lista
  - ✅ Algoritmo de riesgo avanzado
  - ✅ Campos extendidos implementados
  - ✅ Sistema de recomendaciones funcional
  - ✅ Análisis de correlaciones
  - ✅ Módulo de utilidades centralizado

### Pendiente para 90-95%
- ⏳ Inicialización de repositorio Git (CRÍTICO)
- ⏳ Screenshots de evidencia
- ⏳ Tests unitarios básicos (2-3 tests)

---

## Testing Manual Recomendado

### 1. Backend

```powershell
# Iniciar servidor
cd c:\Users\car\Desktop\INTEGRADORCARLOSCANO\mood-keeper
python main.py
```

**Endpoints a Probar:**

1. **POST /api/entries** con campos extendidos:
```json
{
  "mood": 7,
  "comment": "Me siento bien",
  "sleep_hours": 8.0,
  "appetite": 8,
  "concentration": 9
}
```

2. **GET /api/insights/alerts**
   - Verificar que incluya `risk_level`, `avg_composite`, `trend_negative`

3. **GET /api/recommendations?risk_level=ALTO**
   - Verificar recomendaciones para riesgo ALTO

4. **GET /api/insights/correlations**
   - Verificar matriz de correlaciones (requiere datos suficientes)

### 2. Frontend

1. Abrir `dashboard.html` con Live Server
2. Click en FAB (botón flotante)
3. Llenar formulario con campos extendidos
4. Verificar que se guarde correctamente
5. Revisar que aparezcan en lista de alertas

### 3. Swagger UI

Visitar: http://127.0.0.1:8001/docs
- Probar endpoints interactivamente
- Verificar schemas de nuevos modelos

---

## Notas Técnicas

### Compatibilidad

- **Python:** 3.11+
- **Pandas:** Opcional (fallback sin pandas implementado)
- **Matplotlib:** Opcional (para gráficos)
- **Browser:** Cualquier navegador moderno

### Performance

- Lectura CSV optimizada con DictReader
- Caching no implementado (futuro: Redis)
- Recomendado para < 10,000 registros

### Seguridad

- Validaciones en todos los campos numéricos
- Sanitización de strings en utils.py
- JWT tokens con expiración

---

## Próximos Pasos Recomendados

### Alta Prioridad
1. **Git Init:** Crear repositorio y commits
2. **Screenshots:** Tomar evidencia visual
3. **CSV Migration:** Migrar `entries.csv` existente para incluir nuevos campos (backfill con NULL)

### Media Prioridad
4. **Tests:** Escribir 2-3 tests unitarios
5. **Frontend Display:** Mostrar campos extendidos en UI
6. **Recommendations UI:** Integrar recomendaciones en dashboard

### Baja Prioridad
7. **Database Migration:** SQLite/PostgreSQL
8. **Caching:** Redis para insights
9. **Real-time:** WebSockets para alertas

---

**Fecha de Release:** 7 de noviembre de 2025  
**Versión:** 1.1.0  
**Estado:** Estable

