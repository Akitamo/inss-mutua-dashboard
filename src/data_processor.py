"""
Procesador de Datos - Dashboard INSS vs Mutua
=============================================

Módulo para carga, limpieza y procesamiento de datos Excel.
Incluye validación, transformación y aplicación de filtros.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, Tuple, List
import logging
from config import CONFIG, COLUMN_MAPPING, NUMERIC_COLUMNS, PERCENTILE_COLUMNS

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Clase para procesamiento de datos del dashboard"""
    
    def __init__(self):
        self.column_mapping = COLUMN_MAPPING
        self.numeric_columns = NUMERIC_COLUMNS
        self.percentile_columns = PERCENTILE_COLUMNS
        self.edad_orden = CONFIG['EDAD_ORDEN']
    
    def load_and_process_data(self, uploaded_file) -> Optional[pd.DataFrame]:
        """
        Carga y procesa archivo Excel
        
        Args:
            uploaded_file: Archivo subido por Streamlit
            
        Returns:
            DataFrame procesado o None si hay errores
        """
        try:
            # Cargar datos
            df = pd.read_excel(
                uploaded_file,
                sheet_name=CONFIG['SHEET_NAME'],
                skiprows=CONFIG['SKIP_ROWS']
            )
            
            logger.info(f"Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
            
            # Validar columnas requeridas
            if not self._validate_columns(df):
                return None
            
            # Renombrar columnas
            df = self._rename_columns(df)
            
            # Limpiar y transformar datos
            df = self._clean_data(df)
            
            # Ordenar datos
            df = self._sort_data(df)
            
            # Calcular campos adicionales
            df = self._calculate_additional_fields(df)
            
            logger.info(f"Datos procesados exitosamente: {len(df)} registros válidos")
            return df
            
        except Exception as e:
            logger.error(f"Error al procesar datos: {str(e)}")
            st.error(f"Error al procesar archivo: {str(e)}")
            return None
    
    def _validate_columns(self, df: pd.DataFrame) -> bool:
        """Validar que existan las columnas requeridas"""
        missing_columns = []
        for original_col in self.column_mapping.keys():
            if original_col not in df.columns:
                missing_columns.append(original_col)
        
        if missing_columns:
            st.error(f"Columnas faltantes: {missing_columns}")
            return False
        
        return True
    
    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renombrar columnas según mapeo"""
        return df.rename(columns=self.column_mapping)
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpiar y convertir tipos de datos"""
        # Convertir columnas numéricas
        for col in self.numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Eliminar filas con valores nulos en columnas críticas
        df = df.dropna(subset=self.numeric_columns).copy()
        
        # Validar rangos
        df = self._validate_ranges(df)
        
        return df
    
    def _validate_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validar rangos de datos"""
        # Filtrar valores negativos en duraciones
        duration_cols = ['Durestd Inss min', 'Duropt Inss min'] + self.percentile_columns
        for col in duration_cols:
            if col in df.columns:
                df = df[df[col] >= 0]
        
        # Validar episodios
        if 'Count Episodios' in df.columns:
            df = df[
                (df['Count Episodios'] >= CONFIG['MIN_EPISODIOS']) & 
                (df['Count Episodios'] <= CONFIG['MAX_EPISODIOS'])
            ]
        
        return df
    
    def _sort_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ordenar datos por diagnóstico, género y edad"""
        # Crear categoría ordenada para edad
        if 'Gr Edad 10' in df.columns:
            df['Gr Edad 10'] = pd.Categorical(
                df['Gr Edad 10'], 
                categories=self.edad_orden, 
                ordered=True
            )
        
        # Ordenar
        sort_columns = []
        for col in ['Diagnóstico', 'Cod Genero', 'Gr Edad 10']:
            if col in df.columns:
                sort_columns.append(col)
        
        if sort_columns:
            df = df.sort_values(by=sort_columns).reset_index(drop=True)
        
        return df
    
    def _calculate_additional_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcular campos adicionales"""
        # Identificar casos sin variación de percentiles
        percentile_cols = [col for col in self.percentile_columns if col in df.columns]
        if percentile_cols:
            df['percentiles_iguales'] = df[percentile_cols].nunique(axis=1) == 1
        
        # Calcular diferencias INSS vs Mutua
        if 'Durestd Inss min' in df.columns and 'P60min' in df.columns:
            df['diferencia_estandar'] = df['Durestd Inss min'] - df['P60min']
        
        if 'Duropt Inss min' in df.columns and 'P60min' in df.columns:
            df['diferencia_optima'] = df['Duropt Inss min'] - df['P60min']
        
        return df
    
    def apply_filters(self, df: pd.DataFrame, diagnosticos: List[str], 
                     genero: str, edad_grupos: List[str], 
                     episodios_range: Tuple[int, int]) -> pd.DataFrame:
        """
        Aplicar filtros a los datos
        
        Args:
            df: DataFrame original
            diagnosticos: Lista de diagnósticos seleccionados
            genero: Género seleccionado
            edad_grupos: Grupos de edad seleccionados
            episodios_range: Rango de episodios (min, max)
            
        Returns:
            DataFrame filtrado
        """
        df_filtered = df.copy()
        
        # Filtro por diagnóstico
        if diagnosticos:
            df_filtered = df_filtered[df_filtered['Diagnóstico'].isin(diagnosticos)]
        
        # Filtro por género
        if genero != 'Todos':
            df_filtered = df_filtered[df_filtered['Cod Genero'] == genero]
        
        # Filtro por edad
        if edad_grupos:
            df_filtered = df_filtered[df_filtered['Gr Edad 10'].isin(edad_grupos)]
        
        # Filtro por episodios
        if 'Count Episodios' in df_filtered.columns:
            df_filtered = df_filtered[
                (df_filtered['Count Episodios'] >= episodios_range[0]) &
                (df_filtered['Count Episodios'] <= episodios_range[1])
            ]
        
        return df_filtered
    
    def get_summary_stats(self, df: pd.DataFrame) -> dict:
        """Obtener estadísticas resumen"""
        stats = {
            'total_registros': len(df),
            'diagnosticos_unicos': df['Diagnóstico'].nunique() if 'Diagnóstico' in df.columns else 0,
            'total_episodios': df['Count Episodios'].sum() if 'Count Episodios' in df.columns else 0,
            'duracion_media_inss': df['Durestd Inss min'].mean() if 'Durestd Inss min' in df.columns else 0,
            'duracion_media_mutua': df['P60min'].mean() if 'P60min' in df.columns else 0
        }
        
        return stats
    
    def validate_data_quality(self, df: pd.DataFrame) -> dict:
        """Validar calidad de datos"""
        quality_report = {
            'total_rows': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'outliers': {},
            'data_types': df.dtypes.to_dict()
        }
        
        # Detectar outliers en duraciones
        for col in self.numeric_columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                quality_report['outliers'][col] = len(outliers)
        
        return quality_report
