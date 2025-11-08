# Data Dictionary — MoodKeeper

**Proyecto:** MoodKeeper - Plataforma de Monitoreo Emocional  
**Fecha:** 7 de noviembre de 2025  
**Versión:** 1.0

Este documento describe las estructuras de datos utilizadas en el proyecto MoodKeeper, incluyendo esquemas CSV, campos, tipos de datos y relaciones.

---

## Resumen de Tablas/Archivos

| Archivo | Descripción | Registros Aprox. | Relaciones |
|---------|-------------|------------------|------------|
| `accounts.csv` | Usuarios registrados | Variable | → entries |
| `entries.csv` | Encuestas emocionales | Variable | ← accounts |
| `alerts.csv` | Alertas de riesgo (futuro) | Variable | ← accounts |
| `recommendations.csv` | Recomendaciones (futuro) | ~10 | - |

---

## 1. data/accounts.csv

**Descripción:** Almacena información de usuarios registrados en la plataforma.

### Esquema

| Campo | Tipo | Requerido | Único | Descripción | Ejemplo |
|-------|------|-----------|-------|-------------|---------|
| `id` | integer | ✅ | ✅ | Identificador único autoincremental | `1` |
| `handle` | string | ✅ | ✅ | Nombre de usuario (username) | `"juan"` |
| `email` | string | ✅ | ✅ | Correo electrónico validado | `"juan@example.com"` |
| `hashed` | string | ✅ | ❌ | Contraseña hasheada (PBKDF2-SHA256) | `"$pbkdf2-sha256$29000$..."` |
| `created` | datetime | ✅ | ❌ | Fecha y hora de registro (ISO-8601) | `"2025-11-07T10:30:00"` |

### Ejemplo de Registro

```csv
id,handle,email,hashed,created
1,carlos,carlos@example.com,$pbkdf2-sha256$29000$dU6plfJei/H.n7MWYqyVsg$sydUNErzMD84RLdwTbKr40Mu.K2PfopctYOru5gnpZA,2025-10-23T14:19:54.770961
2,juan,juan@example.com,$pbkdf2-sha256$29000$2rv3npNSSikFwDiHsDbGeA$x1DOq47vcwaqHfPvqW6h1GKKTJNSeXQ/dlJ.dy2C6ME,2025-10-23T14:23:56.455381
```

### Restricciones y Validaciones

- **id:** 
  - Generado automáticamente (secuencial)
  - Comienza en 1
  - Calculado por `_next_id()` función

- **handle:**
  - Único en todo el sistema
  - Sin restricción de formato (recomendado: alfanumérico, 3-20 chars)
  - Validado en endpoint con búsqueda de duplicados

- **email:**
  - Único en todo el sistema
  - Validado por Pydantic `EmailStr`
  - Formato RFC 5322

- **hashed:**
  - Resultado de `passlib.pbkdf2_sha256.hash()`
  - Nunca se expone en API
  - Longitud variable (~80-100 caracteres)

- **created:**
  - Formato ISO-8601: `YYYY-MM-DDTHH:MM:SS`
  - Zona horaria: UTC o local (configurar en producción)
  - Generado automáticamente con `datetime.now().isoformat()`

### Índices Recomendados (si se migra a BD)

```sql
CREATE INDEX idx_accounts_handle ON accounts(handle);
CREATE INDEX idx_accounts_email ON accounts(email);
```

---

## 2. data/entries.csv

**Descripción:** Almacena encuestas de estado emocional completadas por los usuarios.

### Esquema

| Campo | Tipo | Requerido | Descripción | Rango/Formato | Ejemplo |
|-------|------|-----------|-------------|---------------|---------|
| `id` | integer | ✅ | ID único de la encuesta | > 0 | `1` |
| `account_id` | integer | ✅ | ID del usuario (FK → accounts.id) | > 0 | `1` |
| `handle` | string | ✅ | Nombre de usuario (copia por conveniencia) | - | `"carlos"` |
| `mood` | integer | ✅ | Puntuación de estado de ánimo | 1-10 | `7` |
| `comment` | string | ❌ | Comentario o nota opcional | max ~500 chars | `"Me siento bien"` |
| `created` | datetime | ✅ | Fecha y hora de la encuesta (ISO-8601) | - | `"2025-11-07T15:30:00"` |

### Campos Planificados (Próxima Versión)

| Campo | Tipo | Requerido | Descripción | Rango | Default |
|-------|------|-----------|-------------|-------|---------|
| `sleep_hours` | float | ❌ | Horas de sueño última noche | 0-24 | `null` |
| `appetite` | integer | ❌ | Nivel de apetito | 1-10 | `null` |
| `concentration` | integer | ❌ | Nivel de concentración | 1-10 | `null` |
| `mood_score` | integer | ❌ | Score compuesto normalizado | 0-100 | calculado |

### Ejemplo de Registro

```csv
id,account_id,handle,mood,comment,created
1,1,carlos,5,estoy maluco,2025-10-23T14:21:25.486635
2,1,carlos,2,No me encuentro bien,2025-10-23T14:23:27.610525
3,2,juan,7,Estoy happy,2025-10-23T14:24:30.665147
4,2,juan,3,,2025-10-23T14:25:14.392717
```

### Restricciones y Validaciones

- **id:**
  - Autoincremental
  - Único en tabla entries

- **account_id:**
  - Debe existir en `accounts.csv`
  - Relación: entries.account_id → accounts.id
  - Validado en endpoint mediante autenticación JWT

- **handle:**
  - Copia denormalizada de `accounts.handle`
  - Facilita queries sin join
  - Debe coincidir con account_id

- **mood:**
  - **Requerido**
  - Rango estricto: 1-10
  - Validado en endpoint:
    ```python
    if not (1 <= entry.mood <= 10):
        raise HTTPException(status_code=400, detail='mood must be 1-10')
    ```
  - Interpretación:
    - 1-3: Muy bajo/Riesgo
    - 4-6: Moderado
    - 7-10: Bueno/Excelente

- **comment:**
  - Opcional (puede ser string vacío o null)
  - Sin validación de longitud actualmente
  - Recomendado: max 500 caracteres
  - Usado para detección de palabras clave (futuro)

- **created:**
  - Timestamp automático
  - Formato ISO-8601
  - Usado para análisis temporal y filtros de alertas

### Análisis y Consultas Comunes

**Promedio de mood por usuario:**
```python
df.groupby('handle')['mood'].mean()
```

**Entradas recientes (últimos 30 días):**
```python
cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
df[df['created'] >= cutoff]
```

**Alertas de riesgo (mood ≤ 3):**
```python
df[df['mood'] <= 3]
```

### Índices Recomendados (si se migra a BD)

```sql
CREATE INDEX idx_entries_account_id ON entries(account_id);
CREATE INDEX idx_entries_created ON entries(created);
CREATE INDEX idx_entries_mood ON entries(mood);
```

---

## 3. data/alerts.csv (Planificado)

**Descripción:** Almacena alertas generadas por el sistema de detección de riesgo.

### Esquema Propuesto

| Campo | Tipo | Requerido | Descripción | Ejemplo |
|-------|------|-----------|-------------|---------|
| `id` | integer | ✅ | ID único de la alerta | `1` |
| `user_id` | integer | ✅ | ID del usuario (FK → accounts.id) | `1` |
| `username` | string | ✅ | Nombre de usuario | `"carlos"` |
| `risk_level` | string | ✅ | Nivel de riesgo | `"ALTO"`, `"MODERADO"`, `"BAJO"` |
| `avg_score` | float | ✅ | Puntuación compuesta promedio | `45.5` |
| `trend_negative` | boolean | ✅ | Tendencia descendente detectada | `true` |
| `generated_at` | datetime | ✅ | Fecha de generación de alerta | `"2025-11-07T16:00:00"` |

### Valores de risk_level

| Valor | Descripción | Criterio |
|-------|-------------|----------|
| `ALTO` | Requiere atención inmediata | avg_score < 60 OR trend_negative = true |
| `MODERADO` | Monitoreo recomendado | 60 ≤ avg_score < 80 |
| `BAJO` | Estado saludable | avg_score ≥ 80 AND trend_negative = false |

### Generación de Alertas

Las alertas se generan mediante la función `compute_risk()` en `app/insights.py`:

1. Calcular score compuesto por encuesta
2. Promediar por usuario
3. Detectar tendencias negativas (últimas 3 entradas)
4. Clasificar nivel de riesgo
5. Guardar en `alerts.csv`

### Ejemplo de Registro

```csv
id,user_id,username,risk_level,avg_score,trend_negative,generated_at
1,1,carlos,ALTO,42.3,true,2025-11-07T16:00:00
2,2,juan,MODERADO,65.8,false,2025-11-07T16:00:00
```

### Uso

- Endpoint: `GET /api/alerts` (para admins)
- Dashboard: Mostrar alertas recientes
- Notificaciones: Trigger para emails/SMS (futuro)

---

## 4. data/recommendations.csv (Planificado)

**Descripción:** Catálogo de recomendaciones personalizadas según nivel de riesgo.

### Esquema Propuesto

| Campo | Tipo | Requerido | Descripción | Ejemplo |
|-------|------|-----------|-------------|---------|
| `id` | integer | ✅ | ID único de recomendación | `1` |
| `risk_level` | string | ✅ | Nivel de riesgo asociado | `"ALTO"` |
| `title` | string | ✅ | Título de la recomendación | `"Contacto de Emergencia"` |
| `description` | text | ✅ | Descripción detallada | `"Te recomendamos contactar..."` |
| `url` | string | ❌ | Enlace a recurso externo | `"https://..."` |

### Ejemplo de Registros

```csv
id,risk_level,title,description,url
1,ALTO,Contacto Profesional,Contactar a un profesional de salud mental inmediatamente,https://saludmental.org
2,MODERADO,Monitoreo Semanal,Realiza monitoreo semanal y ejercicios de relajación,https://recursos.org/relax
3,BAJO,Hábitos Saludables,Mantener hábitos saludables actuales,https://recursos.org/habitos
```

### Uso

- Función: `get_recommendation_for_risk(risk_level)`
- Endpoint: `GET /api/recommendations` (usuario autenticado)
- Dashboard: Mostrar recomendaciones personalizadas

---

## 5. Relaciones entre Tablas

### Diagrama de Relaciones

```
accounts (1) ─────< entries (N)
    │
    └─────< alerts (N)

recommendations (catálogo)
```

### Descripción de Relaciones

1. **accounts → entries**
   - Relación: One-to-Many
   - FK: `entries.account_id` → `accounts.id`
   - Un usuario puede tener múltiples encuestas
   - Una encuesta pertenece a un solo usuario

2. **accounts → alerts**
   - Relación: One-to-Many
   - FK: `alerts.user_id` → `accounts.id`
   - Un usuario puede tener múltiples alertas
   - Una alerta pertenece a un solo usuario

3. **recommendations**
   - Tabla de catálogo (no relacional)
   - Consultada por `risk_level`

---

## 6. Convenciones y Estándares

### Nombres de Campos

- **Formato:** snake_case (todo en minúsculas, separado por guiones bajos)
- **IDs:** Siempre terminan en `_id` (ej: `account_id`, `user_id`)
- **Timestamps:** Sufijo `_at` o sin sufijo si obvio (ej: `created`, `updated_at`)
- **Booleanos:** Prefijo `is_` o descripción clara (ej: `trend_negative`)

### Tipos de Datos

| Tipo Python | Tipo CSV | Descripción | Ejemplo |
|-------------|----------|-------------|---------|
| `int` | string | Números enteros | `"42"` |
| `float` | string | Números decimales | `"3.14"` |
| `str` | string | Texto | `"hello"` |
| `datetime` | string | ISO-8601 | `"2025-11-07T10:00:00"` |
| `bool` | string | "true"/"false" o "True"/"False" | `"true"` |

### Formato de Fechas

**Estándar:** ISO-8601

```
YYYY-MM-DDTHH:MM:SS
2025-11-07T15:30:45
```

**Generación en Python:**
```python
from datetime import datetime
datetime.now().isoformat()
```

**Parsing en Python:**
```python
datetime.fromisoformat("2025-11-07T15:30:45")
```

**Parsing en Pandas:**
```python
pd.to_datetime(df['created'], errors='coerce')
```

### Encoding

- **Estándar:** UTF-8
- **Newline:** LF (`\n`) en Linux/Mac, CRLF (`\r\n`) en Windows
- **CSV Delimiter:** Coma (`,`)
- **Quote Character:** Comillas dobles (`"`) cuando necesario

---

## 7. Migración a Base de Datos Relacional

### Esquema SQLite Propuesto

```sql
-- Tabla de usuarios
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de encuestas
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    mood INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 10),
    comment TEXT,
    sleep_hours REAL CHECK (sleep_hours BETWEEN 0 AND 24),
    appetite INTEGER CHECK (appetite BETWEEN 1 AND 10),
    concentration INTEGER CHECK (concentration BETWEEN 1 AND 10),
    mood_score INTEGER,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- Tabla de alertas
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    risk_level TEXT NOT NULL CHECK (risk_level IN ('BAJO', 'MODERADO', 'ALTO')),
    avg_score REAL NOT NULL,
    trend_negative BOOLEAN DEFAULT 0,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES accounts(id) ON DELETE CASCADE
);

-- Tabla de recomendaciones
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    risk_level TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    url TEXT
);

-- Índices
CREATE INDEX idx_entries_account_id ON entries(account_id);
CREATE INDEX idx_entries_created ON entries(created);
CREATE INDEX idx_entries_mood ON entries(mood);
CREATE INDEX idx_alerts_user_id ON alerts(user_id);
CREATE INDEX idx_alerts_generated_at ON alerts(generated_at);
```

### Ventajas de Migración

1. **Integridad referencial** con FOREIGN KEY
2. **Validaciones** a nivel de BD con CHECK
3. **Transacciones** ACID
4. **Índices** para búsquedas rápidas
5. **Concurrencia** segura
6. **Backups** más robustos

---

## 8. Consultas de Ejemplo

### SQL (si se migra a BD)

```sql
-- Promedio de mood por usuario
SELECT handle, AVG(mood) as avg_mood
FROM entries
GROUP BY handle
ORDER BY avg_mood DESC;

-- Usuarios con mood bajo en últimos 7 días
SELECT DISTINCT e.handle, e.mood, e.created
FROM entries e
WHERE e.mood <= 3
  AND e.created >= DATE('now', '-7 days')
ORDER BY e.created DESC;

-- Conteo de encuestas por usuario
SELECT a.handle, COUNT(e.id) as num_entries
FROM accounts a
LEFT JOIN entries e ON a.id = e.account_id
GROUP BY a.id, a.handle
ORDER BY num_entries DESC;
```

### Python/Pandas

```python
import pandas as pd

# Cargar datos
df = pd.read_csv('data/entries.csv', parse_dates=['created'])

# Promedio de mood por usuario
avg_mood = df.groupby('handle')['mood'].mean().sort_values(ascending=False)

# Usuarios con mood bajo en últimos 7 días
cutoff = pd.Timestamp.now() - pd.Timedelta(days=7)
at_risk = df[(df['mood'] <= 3) & (df['created'] >= cutoff)]

# Serie temporal de promedio diario
daily_avg = df.set_index('created').resample('D')['mood'].mean()
```

---

## 9. Notas de Implementación

### Generación de IDs

**Función actual:**
```python
def _next_id(path):
    if not os.path.exists(path):
        return 1
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        maxid = 0
        for row in r:
            try:
                v = int(row.get('id', 0))
                if v > maxid:
                    maxid = v
            except:
                continue
    return maxid + 1
```

**Limitación:** No es concurrency-safe.

**Mejora recomendada:** Usar UUID o migrar a BD con AUTOINCREMENT.

### Manejo de CSV

**Lectura:**
```python
with open(path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # procesar row
```

**Escritura:**
```python
with open(path, 'a', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([id, handle, email, hashed, created])
```

**Recomendación:** Usar pandas para operaciones complejas.

---

## 10. Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2025-11-07 | Versión inicial del diccionario de datos |

---

## Referencias

- CSV Format: RFC 4180 (https://tools.ietf.org/html/rfc4180)
- ISO 8601 DateTime: https://en.wikipedia.org/wiki/ISO_8601
- Pandas DataFrame: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- SQLite Documentation: https://www.sqlite.org/docs.html

---

**Documento preparado por:** Equipo del Proyecto MoodKeeper  
**Fecha:** 7 de noviembre de 2025  
**Versión:** 1.0  
**Estado:** Completo
