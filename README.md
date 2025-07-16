# 🏥 Dashboard INSS vs Mutua

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📋 Descripción

Dashboard interactivo para análisis comparativo de duración de bajas laborales entre INSS y Mutua. Desarrollado con Streamlit para el equipo de Digitalización de Ibermutua.

### 🎯 Características Principales

- **📤 Carga de datos**: Upload de archivos Excel con validación automática
- **🔍 Filtros dinámicos**: Por diagnóstico, género, edad y número de episodios
- **📊 Visualización comparativa**: Gráficos de percentiles con gradientes de color
- **📈 Métricas resumen**: Estadísticas clave y KPIs
- **🎨 Interfaz responsive**: Diseño adaptativo para diferentes dispositivos
- **⚡ Procesamiento eficiente**: Optimizado para datasets grandes

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.8+
- pip o conda

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/inss-mutua-dashboard.git
cd inss-mutua-dashboard
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en: `http://localhost:8501`

## 📊 Formato de Datos

### Columnas Requeridas

```
- Des Cie9 3dig: Diagnóstico (texto)
- Gr Ocupac: Grupo Ocupacional (texto)
- Cod Genero: Código Género (M/F)
- Gr Edad 10: Grupo Edad (16-25, 26-35, etc.)
- CASO: Identificador de Caso (texto)
- Count (Id Episodio): Número de Episodios (número)
- Durestd Inss min: Duración Estándar INSS (días)
- Duropt Inss min: Duración Óptima INSS (días)
- Minmin, P20min, P40min, P60min, P80min, P99min: Percentiles (días)
```

### Ejemplo de Estructura

| Diagnóstico | Cod Genero | Gr Edad 10 | CASO | Count Episodios | Durestd Inss min | P60min |
|-------------|------------|------------|------|-----------------|-------------------|--------|
| Lumbalgia   | M          | 36-45      | C001 | 15              | 30                | 25     |
| Cervicalgia | F          | 26-35      | C002 | 8               | 20                | 18     |

## 🏗️ Arquitectura del Proyecto

```
inss-mutua-dashboard/
├── 📄 app.py                    # Aplicación principal Streamlit
├── 📄 config.py                 # Configuración global
├── 📄 requirements.txt          # Dependencias Python
├── 📄 .gitignore               # Archivos excluidos de Git
├── 📂 src/
│   ├── 📄 __init__.py
│   ├── 📄 data_processor.py     # Procesamiento de datos
│   └── 📄 visualizations.py    # Generación de gráficos
├── 📂 data/
│   └── 📄 sample_data.xlsx      # Datos de ejemplo
├── 📂 tests/
│   └── 📄 test_data_processor.py
└── 📂 .streamlit/
    └── 📄 config.toml           # Configuración Streamlit
```

## 📈 Funcionalidades

### 1. Carga de Datos
- Validación automática de formato
- Soporte para archivos Excel (.xlsx, .xls)
- Manejo de errores y feedback al usuario

### 2. Filtros Interactivos
- **Diagnósticos**: Multiselección con búsqueda
- **Género**: Selector individual
- **Edad**: Grupos etarios configurables
- **Episodios**: Rango deslizante

### 3. Visualizaciones
- **Gráfico principal**: Comparativa INSS vs Mutua con percentiles
- **Métricas resumen**: KPIs clave del dataset
- **Gráficos adicionales**: Distribuciones por categorías

### 4. Exportación
- Descarga de gráficos en alta resolución
- Exportación de datos filtrados

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` en el directorio raíz:

```env
# Configuración de desarrollo
DEBUG=True
LOG_LEVEL=INFO

# Configuración de datos
MAX_UPLOAD_SIZE=50
DEFAULT_SHEET_NAME="Visualización 1"
```

### Personalización

Modificar `config.py` para ajustar:
- Colores y tema
- Límites de datos
- Configuración de visualización
- Textos y labels

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=src tests/
```

## 🚀 Deploy

### Streamlit Cloud

1. Subir código a GitHub
2. Conectar repositorio en [Streamlit Cloud](https://streamlit.io/cloud)
3. Configurar variables de entorno si es necesario
4. Deploy automático

### Docker (Opcional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## 📝 Changelog

### v1.0.0 (2025-01-XX)
- ✨ Versión inicial del dashboard
- 📊 Visualización comparativa INSS vs Mutua
- 🔍 Filtros dinámicos interactivos
- 📤 Carga de archivos Excel
- 🎨 Interfaz responsive con Streamlit

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto es propiedad de Ibermutua y está destinado para uso interno.

## 👥 Equipo

- **Dirección**: Equipo de Digitalización - Ibermutua
- **Desarrollo**: [Tu Nombre]
- **Contacto**: [email@ibermutua.es]

## 🆘 Soporte

Para soporte técnico o preguntas:
- 📧 Email: [email@ibermutua.es]
- 📱 Teams: Canal #digitalización
- 📝 Issues: GitHub Issues

---

**Hecho con ❤️ por el equipo de Digitalización de Ibermutua**
