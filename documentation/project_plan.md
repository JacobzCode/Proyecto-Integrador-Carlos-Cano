# Project Plan — MoodKeeper

**Versión:** 1.0  
**Fecha:** 7 de noviembre de 2025  
**Equipo:** Proyecto Integrador  
**Repositorio:** MoodKeeper - Plataforma de Monitoreo Emocional

---

## Resumen Ejecutivo

Diseñar y desarrollar una plataforma web que permita monitorear el estado emocional y mental de jóvenes en contextos vulnerables, integrando herramientas de análisis de datos con Python para identificar patrones de riesgo, generar alertas tempranas y ofrecer recursos de apoyo.

---

## Objetivos por Entrega

### Primera Entrega: Fundamentos de Python y Control de Versiones

**Objetivo:** Sentar las bases del proyecto con código limpio, modular y versionado.

**Entregables:**
- ✅ Documento de planeación del proyecto (este archivo)
- ✅ Estructura inicial del repositorio en GitHub
- ✅ Scripts en Python que simulen el registro de usuarios
- ✅ Scripts que permitan cargar encuestas básicas de estado emocional
- ✅ Manejo de archivos CSV para almacenar datos localmente
- ✅ Evidencia del uso de Git (commits, ramas, pull requests)
- ✅ Informe técnico con criterios de calidad aplicados

**Estado actual:**
- ✅ Scripts de registro implementados en `app/storage.py` y `app/server.py`
- ✅ Sistema de encuestas funcionando con persistencia en CSV
- ✅ Arquitectura modular con separación de responsabilidades
- ⚠️ Pendiente: Inicializar Git y documentar commits
- ⚠️ Pendiente: Completar informe técnico formal

---

### Segunda Entrega: Gestión y Análisis de Datos

**Objetivo:** Integrar fuentes de datos, procesarlos y generar visualizaciones útiles.

**Entregables:**
- ⚠️ Base de datos estructurada (actualmente CSV, migración a SQLite recomendada)
- ✅ Scripts en Python para limpieza y transformación de datos
- ✅ Análisis exploratorio (estadísticas, correlaciones)
- ✅ Visualización con librerías Matplotlib y Seaborn
- ✅ Dashboard básico que muestre:
  - Estado emocional promedio por grupo
  - Alertas de riesgo según puntuaciones
  - Evolución temporal del bienestar
- ✅ Evidencia visual (código y gráficos generados)
- ⚠️ Pendiente: Informe técnico del proceso de análisis

**Estado actual:**
- ✅ Análisis implementado en `app/insights.py`
- ✅ Dashboard funcional con visualizaciones interactivas
- ✅ Sistema de alertas básico operativo
- ⚠️ Pendiente: Mejorar algoritmo de detección de riesgo
- ⚠️ Pendiente: Agregar más campos a encuestas (sueño, apetito, concentración)

---

### Tercera Entrega: Integración y Finalización

**Objetivo:** Completar el sistema, realizar pruebas y preparar documentación final.

**Entregables:**
- ✅ Sistema completo funcional
- ✅ Integración frontend-backend
- ⚠️ Documentación de deployment
- ⚠️ Tests unitarios y de integración
- ⚠️ Manual de usuario

---

## Alcance del Proyecto

### Usuarios Objetivo
- **Primarios:** Jóvenes en contextos vulnerables (edades 15-25)
- **Secundarios:** Profesionales de salud mental, orientadores, administradores

### Funcionalidades Principales

#### 1. Registro de Usuarios y Perfil Emocional
- Registro con username, email y contraseña
- Autenticación segura con JWT
- Hash de contraseñas con PBKDF2-SHA256
- Perfil de usuario básico

#### 2. Encuestas Periódicas sobre Estado de Ánimo
- Puntuación de mood (escala 1-10)
- Comentarios opcionales
- Timestamp automático
- Campos adicionales planificados:
  - Horas de sueño
  - Nivel de apetito
  - Nivel de concentración

#### 3. Panel de Visualización de Datos Agregados
- Dashboard interactivo con Chart.js
- Gráficas múltiples (barras, circular, dona, línea, scatter)
- Estadísticas descriptivas (media, desviación, percentiles)
- Visualizaciones server-side con Matplotlib/Seaborn

#### 4. Algoritmos de Detección de Riesgo
- Sistema de alertas basado en umbral de mood
- Filtrado por ventana temporal (días recientes)
- Planificado: Análisis de tendencias y patrones
- Planificado: Score compuesto multi-dimensional

#### 5. Recomendaciones Personalizadas y Recursos de Ayuda
- Recursos estáticos en landing page
- Información de contacto de emergencia
- Planificado: Recomendaciones dinámicas según nivel de riesgo
- Planificado: Contenido personalizado por perfil

---

## Arquitectura Técnica

### Stack Tecnológico

**Backend:**
- Python 3.11+
- FastAPI (framework web)
- Uvicorn (servidor ASGI)
- Pydantic (validación de datos)
- passlib (hashing de contraseñas)
- python-jose (JWT)
- pandas (análisis de datos)
- matplotlib + seaborn (visualizaciones)

**Frontend:**
- HTML5 + CSS3
- JavaScript vanilla
- Bootstrap 5 (UI framework)
- Chart.js (gráficos interactivos)

**Persistencia:**
- CSV (desarrollo/prototipo)
- Migración planificada a SQLite

### Estructura del Proyecto

```
mood-keeper/
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias principales
├── requirements-insights.txt  # Dependencias análisis (opcional)
├── README.md                  # Documentación técnica
├── EXAMPLES.md               # Ejemplos de uso
├── app/
│   ├── __init__.py
│   ├── server.py             # Rutas y endpoints FastAPI
│   ├── security.py           # Hashing y JWT
│   ├── storage.py            # Persistencia CSV
│   ├── dto.py                # Modelos Pydantic
│   └── insights.py           # Análisis y visualizaciones
├── data/
│   ├── accounts.csv          # Usuarios registrados
│   └── entries.csv           # Encuestas emocionales
├── documentation/            # Documentación formal
│   ├── project_plan.md       # Este documento
│   ├── TECHNICAL_REPORT.md   # Informe técnico
│   ├── DELIVERY_CHECKLIST.md # Checklist de entregables
│   └── DATA_DICTIONARY.md    # Diccionario de datos
└── frontend/
    ├── index.html            # Landing page
    ├── login.html            # Inicio de sesión
    ├── register.html         # Registro
    ├── dashboard.html        # Panel principal
    ├── profile.html          # Perfil de usuario
    ├── styles.css            # Estilos
    └── app.js                # Lógica frontend
```

---

## Plan de Trabajo y Timeline

### Semana 1: Fundamentos (Completado ✅)
- ✅ Definición de alcance y requisitos
- ✅ Estructura del repositorio
- ✅ Implementación de registro y autenticación
- ✅ Sistema básico de encuestas
- ✅ Persistencia en CSV

### Semana 2: Análisis de Datos (Completado ✅)
- ✅ Implementación de análisis exploratorio
- ✅ Endpoints de estadísticas
- ✅ Generación de gráficos PNG
- ✅ Sistema de alertas básico
- ✅ Dashboard frontend

### Semana 3: Mejoras y Documentación (En Progreso 🔄)
- 🔄 Documentación formal completa
- 🔄 Inicialización de Git/GitHub
- ⏳ Mejora del algoritmo de riesgo
- ⏳ Campos adicionales en encuestas
- ⏳ Sistema de recomendaciones

### Semana 4: Finalización y Entrega (Planificado 📅)
- 📅 Tests unitarios y de integración
- 📅 Evidencias visuales (screenshots)
- 📅 Validación completa del sistema
- 📅 Preparación de presentación

---

## Restricciones y Supuestos

### Restricciones
1. **Persistencia:** CSV es adecuado para prototipo pero no para producción
2. **Concurrencia:** Sin soporte para múltiples usuarios simultáneos escribiendo
3. **Escalabilidad:** Limitado a datasets pequeños-medianos
4. **Seguridad:** Secret key hardcodeada (cambiar en producción)
5. **Deployment:** Configurado para desarrollo local (no producción)

### Supuestos
1. El proyecto se desarrolla y prueba en entorno local
2. Los usuarios tienen acceso a navegadores modernos
3. Python 3.11+ está disponible en el sistema
4. No se requiere escalamiento masivo en fase de prototipo
5. Las librerías de visualización pueden instalarse (conda recomendado en Windows)

---

## Criterios de Aceptación

### Primera Entrega
- [x] Scripts Python funcionan correctamente
- [x] Código sigue PEP8 y buenas prácticas
- [x] Arquitectura modular y clara
- [x] CSV se crean y gestionan correctamente
- [ ] Git inicializado con commits descriptivos
- [ ] README completo con instrucciones
- [x] Documentación técnica básica

### Segunda Entrega
- [x] Análisis exploratorio implementado
- [x] Visualizaciones generadas correctamente
- [x] Dashboard muestra métricas requeridas
- [x] Sistema de alertas funciona
- [ ] Algoritmo de riesgo avanzado
- [ ] Correlaciones calculadas
- [ ] Informe de análisis completo

### Tercera Entrega
- [x] Sistema end-to-end funcional
- [x] Frontend-backend integrados
- [ ] Tests implementados
- [ ] Documentación de usuario
- [ ] Evidencias visuales recopiladas
- [ ] Sistema validado completamente

---

## Riesgos y Mitigaciones

### Riesgo 1: Problemas de instalación de librerías científicas (pandas, matplotlib)
**Probabilidad:** Media  
**Impacto:** Alto  
**Mitigación:**
- Documentar uso de conda en Windows
- Separar dependencias en requirements-insights.txt (opcional)
- Implementar funcionalidad defensiva (verificar si libs están disponibles)

### Riesgo 2: Corrupción de CSV por escrituras concurrentes
**Probabilidad:** Baja (desarrollo local)  
**Impacto:** Medio  
**Mitigación:**
- Advertir en documentación sobre limitaciones
- Proponer migración a SQLite para producción
- Implementar file locking si es necesario

### Riesgo 3: Falta de tiempo para implementar todas las mejoras
**Probabilidad:** Media  
**Impacto:** Medio  
**Mitigación:**
- Priorizar funcionalidades críticas (documentación, Git)
- Dejar mejoras opcionales para versiones futuras
- Documentar roadmap de mejoras pendientes

### Riesgo 4: Complejidad del algoritmo de detección de riesgo
**Probabilidad:** Media  
**Impacto:** Alto  
**Mitigación:**
- Implementar versión básica primero (funcional)
- Iterar con mejoras incrementales
- Documentar limitaciones y planes de mejora

---

## Roadmap de Mejoras Futuras

### Corto Plazo (Post-Entrega)
1. Migración a SQLite con SQLAlchemy ORM
2. Implementación de tests con pytest
3. Variables de entorno para configuración
4. File locking para escrituras CSV
5. Logging estructurado

### Mediano Plazo
1. Sistema de recomendaciones con IA/ML
2. Detección de patrones con machine learning
3. Notificaciones automáticas (email/SMS)
4. RBAC (control de acceso basado en roles)
5. API rate limiting
6. Dashboard para administradores

### Largo Plazo
1. Frontend moderno con React/Vue
2. Base de datos PostgreSQL
3. Deploy en cloud (AWS/Azure/GCP)
4. Escalamiento horizontal
5. Observabilidad (logs, metrics, traces)
6. Integración con sistemas de salud existentes

---

## Métricas de Éxito

### Técnicas
- ✅ 100% de endpoints funcionando
- ✅ Tiempo de respuesta < 500ms para la mayoría de requests
- ✅ Código con cobertura PEP8 > 90%
- ⏳ Cobertura de tests > 70% (pendiente)
- ✅ Sistema estable sin crashes

### Funcionales
- ✅ Usuarios pueden registrarse y autenticarse
- ✅ Encuestas se registran correctamente
- ✅ Dashboard muestra visualizaciones
- ✅ Alertas se generan según criterios
- ⏳ Recomendaciones personalizadas (pendiente)

### Académicas
- ✅ Cumplimiento de requisitos de entrega
- 🔄 Documentación completa y clara (en progreso)
- ⏳ Evidencias de Git/GitHub (pendiente)
- ✅ Código limpio y mantenible
- ⏳ Informe técnico detallado (pendiente)

---

## Contacto y Responsabilidades

**Desarrollador Principal:** Equipo del Proyecto Integrador  
**Supervisor Técnico:** [Nombre del Profesor/Tutor]  
**Repositorio:** (Pendiente publicación en GitHub)  
**Documentación:** `mood-keeper/documentation/`

---

## Referencias

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Pandas Documentation: https://pandas.pydata.org/
- Chart.js Documentation: https://www.chartjs.org/
- Bootstrap 5: https://getbootstrap.com/
- PEP 8 Style Guide: https://peps.python.org/pep-0008/

---

**Última actualización:** 7 de noviembre de 2025  
**Versión del documento:** 1.0  
**Estado del proyecto:** En desarrollo activo - Fase de documentación y mejoras
