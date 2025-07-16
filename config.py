"""
Configuración del Dashboard INSS vs Mutua
=========================================

Archivo de configuración centralizada para el proyecto.
Incluye constantes, mapeos de columnas, configuración de visualización y parámetros globales.
"""

# Configuración principal
CONFIG = {
    # Información del proyecto
    'PROJECT_NAME': 'Dashboard INSS vs Mutua',
    'PROJECT_VERSION': '1.0.0',
    'AUTHOR': 'Equipo Digitalización - Ibermutua',
    
    # Configuración de Streamlit
    'PAGE_TITLE': 'Dashboard INSS vs Mutua',
    'PAGE_ICON': '🏥',
    'LAYOUT': 'wide',
    
    # Parámetros de visualización
    'FIGURE_SIZE': (16, 12),
    'MIN_BAR_HEIGHT': 0.2,
    'MAX_BAR_HEIGHT': 0.6,
    'LEFT_MARGIN': 40,
    'RIGHT_MARGIN': 40,
    
    # Colores
    'COLORS': {
        'primary': '#2E5BFF',
        'secondary': '#6C757D',
        'success': '#28A745',
        'warning': '#FFC107',
        'danger': '#DC3545',
        'light_gray': 'lightgray',
        'dark_gray': 'dimgray',
        'blue': 'blue',
        'black': 'black'
    },
    
    # Configuración de datos
    'SHEET_NAME': 'Visualización 1',
    'SKIP_ROWS': 2,
    'EDAD_ORDEN': ['16-25', '26-35', '36-45', '46-55', '56-65'],
    
    # Límites y validaciones
    'MAX_RECORDS': 10000,
    'MIN_EPISODIOS': 1,
    'MAX_EPISODIOS': 1000
}

# Mapeo de columnas (nombres originales -> nombres internos)
COLUMN_MAPPING = {
    'Des Cie9 3dig': 'Diagnóstico',
    'Gr Ocupac': 'Gr Ocupac',
    'Cod Genero': 'Cod Genero',
    'Gr Edad 10': 'Gr Edad 10',
    'CASO': 'Caso',
    'Count (Id Episodio)': 'Count Episodios',
    'Durestd Inss min': 'Durestd Inss min',
    'Duropt Inss min': 'Duropt Inss min',
    'Minmin': 'Minmin',
    'P20min': 'P20min',
    'P40min': 'P40min',
    'P60min': 'P60min',
    'P80min': 'P80min',
    'P99min': 'P99min'
}

# Columnas numéricas para procesamiento
NUMERIC_COLUMNS = [
    'Durestd Inss min', 'Duropt Inss min', 'Minmin', 'P20min', 'P40min',
    'P60min', 'P80min', 'P99min', 'Count Episodios'
]

# Columnas de percentiles
PERCENTILE_COLUMNS = ['Minmin', 'P20min', 'P40min', 'P60min', 'P80min', 'P99min']

# Configuración de matplotlib
MATPLOTLIB_CONFIG = {
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 16,
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
}

# Configuración de colormap
COLORMAP_CONFIG = {
    'name': 'RdYlGn_r',
    'percentile_colors': {
        'min': 0.0,
        'p20': 0.2,
        'p40': 0.4,
        'p60': 0.6,
        'p80': 0.8,
        'p99': 1.0
    }
}

# Textos y labels
TEXTS = {
    'main_title': 'Comparativa INSS vs Historial Mutua',
    'subtitle': 'Diagnóstico a izquierda, caso + nº episodios a derecha',
    'xlabel': 'Duración (días)',
    'no_variation': 'sin variación',
    'legend_labels': {
        'min': 'Min',
        'p20': 'P20',
        'p40': 'P40',
        'p60': 'P60',
        'p80': 'P80',
        'p99': 'P99',
        'constant': 'Distribución constante',
        'standard': 'Duración estándar INSS',
        'optimal': 'Duración óptima INSS'
    }
}

# Configuración de validación de datos
VALIDATION_CONFIG = {
    'required_columns': list(COLUMN_MAPPING.keys()),
    'min_rows': 1,
    'max_rows': 10000,
    'allowed_file_types': ['xlsx', 'xls'],
    'max_file_size_mb': 50
}

# Configuración de filtros
FILTER_CONFIG = {
    'max_multiselect_items': 20,
    'default_diagnosticos_limit': 5,
    'edad_groups': ['16-25', '26-35', '36-45', '46-55', '56-65'],
    'genero_options': ['Todos', 'M', 'F']
}

# Configuración de exportación
EXPORT_CONFIG = {
    'formats': ['png', 'pdf', 'svg'],
    'default_format': 'png',
    'quality': 'high',
    'filename_template': 'inss_mutua_dashboard_{timestamp}'
}

# Configuración de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/dashboard.log'
}
