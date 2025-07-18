"""
Dashboard INSS vs Mutua - Análisis de Duración de Bajas Laborales
===============================================================

Aplicación Streamlit para análisis comparativo de duración de bajas
entre INSS y Mutua, con visualización de percentiles y filtros interactivos.

Autor: Equipo Digitalización - Ibermutua
Fecha: 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from io import StringIO
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

# Añadir el directorio actual al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos locales
try:
    from src.data_processor import DataProcessor
    from src.visualizations import VisualizationManager
    from config import CONFIG
    imports_ok = True
except ImportError as e:
    st.error(f"Error al importar módulos: {str(e)}")
    imports_ok = False

# Configuración de página
st.set_page_config(
    page_title="Dashboard INSS vs Mutua",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        color: #2E5BFF;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E5BFF;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Header en área principal
    st.markdown('<h1 class="main-header">🏥 Dashboard INSS vs Mutua</h1>', 
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Análisis comparativo de duración de bajas laborales</p>', 
                unsafe_allow_html=True)
    
    # Verificar que las importaciones funcionaron
    if not imports_ok:
        st.error("❌ Error en las importaciones. Verifica que todos los módulos estén disponibles.")
        return
    
    # Inicializar variables
    df_filtered = None
    
    # Sidebar - Solo upload y filtros
    with st.sidebar:
        st.header("📤 Carga de Datos")
        
        uploaded_file = st.file_uploader(
            "Selecciona archivo Excel",
            type=['xlsx', 'xls'],
            help="Archivo con datos de análisis INSS vs Mutua"
        )
        
        if uploaded_file is not None:
            try:
                # Procesar datos
                processor = DataProcessor()
                df = processor.load_and_process_data(uploaded_file)
                
                if df is not None:
                    st.success(f"✅ Datos cargados: {len(df)} registros")
                    
                    # Filtros dinámicos
                    st.header("🔍 Filtros")
                    
                    # Filtro por diagnóstico
                    diagnosticos = st.multiselect(
                        "Diagnósticos",
                        options=df['Diagnóstico'].unique(),
                        default=df['Diagnóstico'].unique()[:5] if len(df['Diagnóstico'].unique()) >= 5 else df['Diagnóstico'].unique()
                    )
                    
                    # Filtro por género
                    genero = st.selectbox(
                        "Género",
                        options=['Todos'] + list(df['Cod Genero'].unique())
                    )
                    
                    # Filtro por edad
                    edad_grupos = st.multiselect(
                        "Grupos de Edad",
                        options=df['Gr Edad 10'].unique(),
                        default=df['Gr Edad 10'].unique()
                    )
                    
                    # Filtro por número de episodios
                    if 'Count Episodios' in df.columns:
                        episodios_range = st.slider(
                            "Rango de Episodios",
                            min_value=int(df['Count Episodios'].min()),
                            max_value=int(df['Count Episodios'].max()),
                            value=(int(df['Count Episodios'].min()), 
                                   int(df['Count Episodios'].max()))
                        )
                    else:
                        episodios_range = (1, 1000)
                    
                    # Aplicar filtros
                    df_filtered = processor.apply_filters(
                        df, diagnosticos, genero, edad_grupos, episodios_range
                    )
                else:
                    st.error("❌ Error al procesar el archivo")
            
            except Exception as e:
                st.error(f"❌ Error al procesar datos: {str(e)}")
        else:
            st.info("👆 Sube un archivo Excel para comenzar")
            
            # Mostrar datos de ejemplo
            st.subheader("📊 Formato de Datos Esperado")
            st.code("""
            Columnas requeridas:
            - Des Cie9 3dig (Diagnóstico)
            - Gr Ocupac (Grupo Ocupacional)
            - Cod Genero (Código Género)
            - Gr Edad 10 (Grupo Edad)
            - CASO (Caso)
            - Count (Id Episodio) (Número de Episodios)
            - Durestd Inss min (Duración Estándar INSS)
            - Duropt Inss min (Duración Óptima INSS)
            - Minmin, P20min, P40min, P60min, P80min, P99min (Percentiles)
            """)

    # ÁREA PRINCIPAL - Aquí va el dashboard
    if df_filtered is not None:
        if not df_filtered.empty:
            display_dashboard(df_filtered)
        else:
            st.warning("⚠️ No hay datos con los filtros aplicados")
    else:
        # Placeholder cuando no hay datos
        st.info("📁 **Instrucciones de Uso:**")
        st.write("1. Sube tu archivo Excel usando el panel lateral")
        st.write("2. Ajusta los filtros según tus necesidades")
        st.write("3. Visualiza los resultados comparativos")
        
        st.info("📋 **Características del Dashboard:**")
        st.write("• Análisis comparativo INSS vs Mutua")
        st.write("• Visualización de percentiles con gradientes")
        st.write("• Filtros dinámicos por diagnóstico, género y edad")
        st.write("• Métricas resumen y estadísticas detalladas")

def display_dashboard(df):
    """Mostrar dashboard principal con métricas y visualizaciones"""
    
    try:
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📊 Total Registros",
                len(df),
                help="Número total de registros filtrados"
            )
        
        with col2:
            if 'Count Episodios' in df.columns:
                st.metric(
                    "📈 Total Episodios",
                    f"{df['Count Episodios'].sum():,}",
                    help="Suma total de episodios"
                )
        
        with col3:
            if 'Durestd Inss min' in df.columns:
                st.metric(
                    "⏱️ Duración Media INSS",
                    f"{df['Durestd Inss min'].mean():.1f} días",
                    help="Duración promedio estándar INSS"
                )
        
        with col4:
            st.metric(
                "🏥 Diagnósticos",
                df['Diagnóstico'].nunique(),
                help="Número de diagnósticos únicos"
            )
        
        # Visualización principal
        st.header("📈 Visualización Comparativa")
        
        # Crear visualización
        viz_manager = VisualizationManager()
        fig = viz_manager.create_comparative_chart(df)
        
        if fig:
            st.pyplot(fig)
        else:
            st.warning("⚠️ No se pudo generar la visualización")
        
        # Tabla de datos
        with st.expander("📋 Ver Datos Detallados"):
            st.dataframe(df, use_container_width=True)
        
        # Estadísticas adicionales
        st.header("📊 Estadísticas Adicionales")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Diagnósticos")
            top_diagnosticos = df['Diagnóstico'].value_counts().head(10)
            st.bar_chart(top_diagnosticos)
        
        with col2:
            st.subheader("Distribución por Género")
            if 'Cod Genero' in df.columns:
                genero_dist = df['Cod Genero'].value_counts()
                st.bar_chart(genero_dist)
    
    except Exception as e:
        st.error(f"❌ Error al mostrar dashboard: {str(e)}")

if __name__ == "__main__":
    main()