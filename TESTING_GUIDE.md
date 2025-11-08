# Guía de Pruebas Manuales - MoodKeeper

## 🚀 Inicio Rápido

### 1. Iniciar Backend

```powershell
cd c:\Users\car\Desktop\INTEGRADORCARLOSCANO\mood-keeper
python main.py
```

**Verificar:** Debe mostrar `Uvicorn running on http://127.0.0.1:8001`

---

### 2. Abrir Frontend

**Opción A - VS Code Live Server:**
1. Abrir `frontend/index.html` en VS Code
2. Click derecho → "Open with Live Server"
3. Navegar a http://127.0.0.1:5500/frontend/

**Opción B - Directamente:**
1. Abrir `frontend/index.html` en Chrome/Edge/Firefox

---

## 🧪 Casos de Prueba

### Test 1: Registro de Usuario

**Pasos:**
1. Ir a http://127.0.0.1:5500/frontend/register.html
2. Llenar formulario:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123`
3. Click "Registrarse"

**Resultado esperado:** ✅ Mensaje "Cuenta creada" y redirección a login

---

### Test 2: Inicio de Sesión

**Pasos:**
1. Ir a http://127.0.0.1:5500/frontend/login.html
2. Introducir credenciales:
   - Username: `testuser`
   - Password: `password123`
3. Click "Iniciar sesión"

**Resultado esperado:** ✅ Redirección a dashboard con nombre de usuario visible

---

### Test 3: Crear Encuesta Básica

**Pasos:**
1. En el dashboard, click en el botón flotante (✏️) abajo a la derecha
2. Mover slider de Mood a 7
3. Escribir comentario: "Me siento bien hoy"
4. Click "Enviar"

**Resultado esperado:** 
- ✅ Modal se cierra
- ✅ Mensaje "Entry saved"
- ✅ Gráficos se actualizan

---

### Test 4: Crear Encuesta con Campos Extendidos

**Pasos:**
1. Click en botón flotante ✏️
2. Configurar:
   - Mood: 8
   - Horas de sueño: 8.0
   - Apetito: 9
   - Concentración: 8
   - Comentario: "Excelente día, dormí bien"
3. Click "Enviar"

**Resultado esperado:** 
- ✅ Encuesta guardada
- ✅ Campos extendidos visibles en alertas (😴 🍽️ 🧠)

---

### Test 5: Generar Alerta de Riesgo

**Pasos:**
1. Crear 3 encuestas con mood bajo:
   - Encuesta 1: Mood 3, Comment: "Me siento triste"
   - Encuesta 2: Mood 2, Comment: "Día difícil"
   - Encuesta 3: Mood 2, Comment: "Necesito ayuda"
2. Refrescar página o esperar actualización

**Resultado esperado:**
- ✅ Alertas visibles en tabla
- ✅ Badge "ALTO" en rojo visible
- ✅ Recomendaciones de nivel ALTO mostradas

---

### Test 6: Verificar Correlaciones

**Prerrequisito:** Tener al menos 10 encuestas con campos extendidos

**Pasos:**
1. Ir al dashboard
2. Scroll hasta la sección "📊 Análisis de Correlaciones"

**Resultado esperado:**
- ✅ Sección visible con tarjetas de correlación
- ✅ Porcentajes y barras de progreso
- ✅ Interpretaciones en texto

---

### Test 7: Probar API con Swagger

**Pasos:**
1. Abrir http://127.0.0.1:8001/docs
2. Probar endpoint `GET /api/insights/summary`
3. Probar endpoint `GET /api/recommendations?risk_level=ALTO`
4. Probar endpoint `GET /api/insights/correlations`

**Resultado esperado:**
- ✅ Respuestas JSON con datos
- ✅ Status 200 OK

---

## 📊 Verificación de Funcionalidades

### Backend

| Funcionalidad | Endpoint | Verificar |
|---------------|----------|-----------|
| ✅ Registro | POST /api/accounts | Crear cuenta nueva |
| ✅ Login | POST /api/sessions | Obtener JWT token |
| ✅ Crear encuesta | POST /api/entries | Mood + campos extendidos |
| ✅ Listar encuestas | GET /api/entries | Ver todas las entradas |
| ✅ Resumen | GET /api/insights/summary | Estadísticas generales |
| ✅ Promedios | GET /api/insights/average | Promedio por usuario |
| ✅ Alertas | GET /api/insights/alerts | Detección de riesgo |
| ✅ Correlaciones | GET /api/insights/correlations | Matriz de correlaciones |
| ✅ Recomendaciones | GET /api/recommendations | Por nivel de riesgo |
| ✅ Gráficos | GET /api/insights/plot/{name} | PNG generado |

### Frontend

| Funcionalidad | Archivo | Verificar |
|---------------|---------|-----------|
| ✅ Landing | index.html | Página principal |
| ✅ Registro | register.html | Formulario funcional |
| ✅ Login | login.html | Autenticación |
| ✅ Dashboard | dashboard.html | Gráficos interactivos |
| ✅ Perfil | profile.html | Info de usuario |
| ✅ Formulario extendido | dashboard.html (modal) | 4 campos adicionales |
| ✅ Alertas con badges | dashboard.html | Nivel de riesgo visible |
| ✅ Recomendaciones | dashboard.html | Dinámicas según riesgo |
| ✅ Correlaciones | dashboard.html | Visualización con tarjetas |

---

## 🐛 Troubleshooting

### Problema: "No se puede conectar al backend"

**Solución:**
1. Verificar que el servidor esté corriendo: `python main.py`
2. Verificar puerto: http://127.0.0.1:8001
3. Verificar CORS en `app/server.py`

### Problema: "Token inválido" o "401 Unauthorized"

**Solución:**
1. Cerrar sesión y volver a iniciar
2. Limpiar localStorage del navegador
3. Verificar que el token no haya expirado

### Problema: "Correlaciones no se muestran"

**Solución:**
1. Crear más encuestas (mínimo 10)
2. Asegurarse de incluir campos extendidos
3. Verificar que pandas esté instalado: `pip install pandas`

### Problema: "Gráficos no cargan"

**Solución:**
1. Verificar que matplotlib esté instalado
2. Verificar endpoint: http://127.0.0.1:8001/api/insights/plot/hist
3. Revisar consola del navegador (F12)

---

## 📸 Screenshots Recomendados

Para la carpeta `EVIDENCE/screenshots/`:

1. **01_landing_page.png** - Página principal
2. **02_login.png** - Formulario de login
3. **03_register.png** - Formulario de registro
4. **04_dashboard_empty.png** - Dashboard sin datos
5. **05_dashboard_with_data.png** - Dashboard con gráficos
6. **06_survey_form.png** - Modal de encuesta extendida
7. **07_alerts_section.png** - Tabla de alertas con badges
8. **08_recommendations.png** - Recomendaciones mostradas
9. **09_correlations.png** - Sección de correlaciones
10. **10_swagger_api.png** - Documentación Swagger
11. **11_chart_mood_trend.png** - Gráfico de tendencias
12. **12_profile_page.png** - Página de perfil

**Herramienta:** Win + Shift + S (Snipping Tool de Windows)

---

## ✅ Checklist de Verificación Final

### Funcionalidades Core
- [ ] Registro de usuarios funciona
- [ ] Login con JWT funciona
- [ ] Crear encuestas básicas funciona
- [ ] Crear encuestas con campos extendidos funciona
- [ ] Dashboard muestra gráficos
- [ ] Alertas se generan correctamente
- [ ] Recomendaciones se muestran por nivel de riesgo
- [ ] Correlaciones se calculan y visualizan

### Algoritmo de Riesgo
- [ ] Score compuesto se calcula correctamente
- [ ] Detección de tendencias funciona
- [ ] Niveles de riesgo (ALTO/MODERADO/BAJO) se asignan bien
- [ ] Badges de riesgo visibles en UI

### Campos Extendidos
- [ ] sleep_hours se guarda en CSV
- [ ] appetite se guarda en CSV
- [ ] concentration se guarda en CSV
- [ ] Campos se muestran en alertas con íconos
- [ ] Validaciones funcionan (rangos correctos)

### Documentación
- [ ] README.md completo y claro
- [ ] CHANGELOG.md actualizado
- [ ] Documentos técnicos creados
- [ ] DATA_DICTIONARY.md preciso

### Git & GitHub
- [ ] Commits con mensajes descriptivos
- [ ] Código subido a GitHub
- [ ] .gitignore configurado correctamente
- [ ] README visible en repositorio

---

## 🎯 Próximos Pasos

1. ✅ Completar pruebas manuales
2. 📸 Tomar screenshots para EVIDENCE
3. 📝 Crear commits adicionales si hay cambios
4. 🚀 Preparar presentación/demo
5. 📦 Empaquetar para entrega

---

**Última actualización:** 8 de noviembre de 2025
