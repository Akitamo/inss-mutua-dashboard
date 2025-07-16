# 📋 CONTEXTO DEL PROYECTO - Dashboard INSS vs Mutua

## 🎯 INFORMACIÓN GENERAL

**Nombre del Proyecto**: Dashboard INSS vs Mutua - Análisis de Duración de Bajas Laborales
**Ubicación**: C:\dev\projects\inss-mutua-dashboard\
**Tecnología Principal**: Python + Streamlit
**Objetivo**: Migrar código Jupyter a dashboard web interactivo para análisis comparativo INSS vs Mutua

## 👤 CONTEXTO DEL USUARIO

**Perfil**: Profesional senior en transformación digital healthcare
- Director de Digitalización y AI en Ibermutua
- Especialista en interoperabilidad Seguridad Social (CMISS)
- Doctor en Psicología con programa formativo "Liderar con Consciencia"
- Experto en Python, Excel, VBA, automatización y análisis de datos

**Estilo de Trabajo**:
- Respuestas claras, estructuradas y argumentadas
- Iteración progresiva para afinar soluciones
- Enfoque práctico para ambiente productivo
- Evitar complejidad innecesaria

## 🏗️ ARQUITECTURA DEL PROYECTO

### Estructura de Directorios
```
C:\dev\projects\inss-mutua-dashboard\
├── 📄 app.py                    # Aplicación principal Streamlit
├── 📄 config.py                 # Configuración centralizada
├── 📄 requirements.txt          # Dependencias Python
├── 📄 README.md                 # Documentación completa
├── 📄 .gitignore               # Exclusiones Git
├── 📂 src/
│   ├── 📄 __init__.py          # Módulo Python
│   ├── 📄 data_processor.py     # Procesamiento de datos
│   └── 📄 visualizations.py    # Generación gráficos
├── 📂 data/                     # Datos de ejemplo
├── 📂 tests/
│   └── 📄 test_data_processor.py # Tests unitarios
└── 📂 .streamlit/
    └── 📄 config.toml           # Configuración Streamlit
```

### Componentes Principales

#### 1. **app.py** - Aplicación Principal
- Framework: Streamlit
- Funcionalidades:
  - Upload de archivos Excel
  - Sidebar con filtros dinámicos
  - Visualización comparativa
  - Métricas resumen
  - Interfaz responsive

#### 2. **config.py** - Configuración
- Mapeo de columnas (nombres originales → internos)
- Constantes de visualización
- Configuración de colores y tema
- Parámetros de validación

#### 3. **src/data_processor.py** - Procesamiento
- Clase `DataProcessor`
- Validación de columnas requeridas
- Limpieza y transformación de datos
- Aplicación de filtros
- Cálculo de campos adicionales
- Estadísticas resumen

#### 4. **src/visualizations.py** - Visualizaciones
- Clase `VisualizationManager`
- Gráfico comparativo principal (matplotlib)
- Gráficos resumen (plotly)
- Configuración de estilos y leyendas
- Personalización de colormap

## 📊 FUNCIONALIDADES IMPLEMENTADAS

### 1. Carga de Datos
- Upload de archivos Excel (.xlsx, .xls)
- Validación automática de formato
- Mapeo de columnas originales
- Manejo de errores y feedback

### 2. Procesamiento de Datos
- Limpieza y conversión de tipos
- Validación de rangos
- Ordenamiento por diagnóstico/género/edad
- Cálculo de campos derivados
- Identificación de casos sin variación

### 3. Filtros Interactivos
- **Diagnósticos**: Multiselect con opciones dinámicas
- **Género**: Selector individual (Todos/M/F)
- **Grupos de Edad**: Multiselect con orden categórico
- **Episodios**: Slider de rango numérico

### 4. Visualizaciones
- **Gráfico Principal**: Barras de percentiles con gradiente de color
- **Líneas INSS**: Duración estándar (línea negra) y óptima (punto azul)
- **Sombreado**: Alternado por diagnóstico
- **Leyenda**: Detallada con todos los elementos
- **Métricas**: KPIs principales en columnas

### 5. Características Técnicas
- Entorno virtual local (venv/)
- Dependencias definidas en requirements.txt
- Tests unitarios con pytest
- Configuración Git preparada
- Documentación completa

## 📋 FORMATO DE DATOS

### Columnas Requeridas (Excel)
```
- Des Cie9 3dig → Diagnóstico
- Gr Ocupac → Gr Ocupac
- Cod Genero → Cod Genero (M/F)
- Gr Edad 10 → Gr Edad 10 (16-25, 26-35, 36-45, 46-55, 56-65)
- CASO → Caso
- Count (Id Episodio) → Count Episodios
- Durestd Inss min → Durestd Inss min
- Duropt Inss min → Duropt Inss min
- Minmin, P20min, P40min, P60min, P80min, P99min → Percentiles
```

### Configuración de Carga
- Hoja: "Visualización 1"
- Saltar filas: 2
- Columnas numéricas: Duraciones y percentiles
- Validación: Valores no negativos

## 🎨 CONFIGURACIÓN VISUAL

### Colores y Tema
- **Primario**: #2E5BFF
- **Secundario**: #6C757D
- **Colormap**: RdYlGn_r (rojo-amarillo-verde invertido)
- **Fondo**: #FFFFFF con alternancia gris claro

### Parámetros de Visualización
- Tamaño figura: (16, 12)
- Altura barras: 0.2 - 0.6 (proporcional a episodios)
- Márgenes: 40 píxeles izquierda/derecha
- Fuente: Sans serif, tamaños configurables

## 🔧 CONFIGURACIÓN TÉCNICA

### Dependencias Principales
- streamlit>=1.28.0
- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
- plotly>=5.15.0
- openpyxl>=3.1.0

### Configuración Streamlit
- Puerto: 8501
- Tema personalizado con colores corporativos
- Upload máximo: 50MB
- Modo desarrollo: Configurable

### Variables de Entorno
- DEBUG: Para modo desarrollo
- LOG_LEVEL: Nivel de logging
- MAX_UPLOAD_SIZE: Límite de archivos

## 🚀 ESTADO ACTUAL DEL PROYECTO

### ✅ Completado
- [x] Estructura de proyecto creada
- [x] Aplicación principal Streamlit
- [x] Procesador de datos con validación
- [x] Gestor de visualizaciones
- [x] Configuración centralizada
- [x] Tests unitarios básicos
- [x] Documentación completa
- [x] Configuración Git y deploy

### 🔄 Pendiente
- [ ] Pruebas con datos reales
- [ ] Optimización de rendimiento
- [ ] Funcionalidades adicionales
- [ ] Deploy en Streamlit Cloud
- [ ] Configuración CI/CD

## 📝 COMANDOS ÚTILES

### Desarrollo Local
```bash
# Activar entorno
cd C:\dev\projects\inss-mutua-dashboard
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py

# Ejecutar tests
pytest tests/
```

### Git y Deploy
```bash
# Inicializar Git
git init
git add .
git commit -m "Initial commit"

# Conectar a GitHub
git remote add origin https://github.com/usuario/inss-mutua-dashboard.git
git push -u origin main

# Deploy automático en Streamlit Cloud
```

## 🎯 PRÓXIMOS PASOS SUGERIDOS

1. **Validación**: Probar con archivo Excel real
2. **Optimización**: Mejorar rendimiento con datos grandes
3. **Funcionalidades**: Exportación de gráficos, más filtros
4. **Deploy**: Configurar en Streamlit Cloud
5. **Integración**: Conectar con sistemas existentes

## 🔗 RECURSOS ADICIONALES

- **Documentación Streamlit**: https://docs.streamlit.io/
- **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Plotly Documentation**: https://plotly.com/python/

---

**Última actualización**: 2025-01-16
**Versión**: 1.0.0
**Mantenedor**: Equipo Digitalización - Ibermutua
